#!/usr/bin/env python3
import os
import logging
import sys
import csv
import socket
import dns.resolver
import dns.exception
import time
import io
import subprocess
import re
import certstream
from mpipe import Pipeline, OrderedStage, UnorderedStage
from datetime import datetime
from libsshfp import SSHFP, SSHFPDomain, SSHFPComparison
from config import QUERY_WORKERS, PARSER_WORKERS, SERVER_WORKERS, LOGS_FOLDER


if not os.path.exists(LOGS_FOLDER):
    os.mkdir(LOGS_FOLDER)

LOG_SYMLINK = os.path.join(LOGS_FOLDER, 'current')
if os.path.exists(LOG_SYMLINK):
    os.unlink(LOG_SYMLINK)

LOG_DIR_NAME = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
os.mkdir(os.path.join(LOGS_FOLDER, LOG_DIR_NAME))
os.symlink(LOG_DIR_NAME, LOG_SYMLINK)

with open(os.path.join(LOG_SYMLINK, "README"), "w") as f:
    f.write(f"""
DOMAINSOURCE: {os.environ['DOMAINSOURCE'] if 'DOMAINSOURCE' in os.environ else ''} 
DOMAINFILE: {os.environ['DOMAINFILE'] if 'DOMAINFILE' in os.environ else ''}
QUERY_WORKERS: {QUERY_WORKERS}
PARSER_WORKERS: {PARSER_WORKERS}
SERVER_WORKERS: {SERVER_WORKERS}
        """)


query_logger = logging.getLogger('query')
parser_logger = logging.getLogger('parser')
server_logger = logging.getLogger('server')
certstream_logger = logging.getLogger('certstream')
domainfile_logger = logging.getLogger('domainfile')

query_logger.setLevel(getattr(logging, os.environ['LOGLEVEL']))
parser_logger.setLevel(getattr(logging, os.environ['LOGLEVEL']))
server_logger.setLevel(getattr(logging, os.environ['LOGLEVEL']))
certstream_logger.setLevel(getattr(logging, os.environ['LOGLEVEL']))
domainfile_logger.setLevel(getattr(logging, os.environ['LOGLEVEL']))

query_logger.addHandler(logging.FileHandler(os.path.join(LOG_SYMLINK, "query.log")))
parser_logger.addHandler(logging.FileHandler(os.path.join(LOG_SYMLINK, "parser.log")))
server_logger.addHandler(logging.FileHandler(os.path.join(LOG_SYMLINK, "server.log")))
certstream_logger.addHandler(logging.FileHandler(os.path.join(LOG_SYMLINK, "certstream.log")))
domainfile_logger.addHandler(logging.FileHandler(os.path.join(LOG_SYMLINK, "domainfile.log")))

recursor_ip = socket.gethostbyname('recursor')

dnssec_recursor_ip = socket.gethostbyname('dnssecrecursor')

dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers = [f"{recursor_ip}"]

######
#
# Pipeline
#
######

def query_sshfp(task):
    domain = task
    try:
        timestamp = int(time.time())
        answer = dns.resolver.resolve(domain, 'sshfp')
        records = [sshfp.to_text() for sshfp in answer]
        query_logger.info(f"Found SSHFP RRs: {domain} => {records}")
    except dns.exception.DNSException as e:
        query_logger.error(f"DNSException for {domain} -> {e}")
        return None
    except Exception as e:
        query_logger.error(f"An error occured: {domain} -> {e}")
        return None

    return {'domain': domain, 'records': records, 'timestamp': timestamp}

def parse_sshfp(task):
    if task is None:
        return None

    csv_out = io.StringIO()
    csv_writer = csv.writer(csv_out)
    sshfpd = SSHFPDomain(domain=task['domain'], timestamp=task['timestamp'])

    for record in task['records']:
        try:
            sshfp = SSHFP.from_string(record)
            sshfp.domain = task['domain']
            sshfp.timestamp = task['timestamp']
            
            csv_writer.writerow([sshfp.timestamp, sshfp.domain, sshfp.algo_stringified(), sshfp.type_stringified(), sshfp.fingerprint])
            sshfpd.records.append(sshfp)
        except Exception as e:
            parser_logger.error(f"An error occured: {task} -> {e}")

    for row in csv_out.getvalue().split('\n'):
        if not len(row):
            continue
        parser_logger.info(row)

    return sshfpd.to_json()

def server_sshfp(dns_sshfpd_json):
    try:
        if dns_sshfpd_json is None:
            return
        dns_sshfpd = SSHFPDomain.from_json(dns_sshfpd_json)
    except Exception as e:
        sshfp_comp = SSHFPComparison(domain=dns_sshfpd.domain, dns_sshfp=None, server_sshfp=None, errors=[str(e)])
        server_logger.info(sshfp_comp.to_json())
        return None

    try:
        answer = dns.resolver.resolve(dns_sshfpd.domain, 'A')
        a_records = [a.to_text() for a in answer]
    except dns.exception.DNSException as e:
        sshfp_comp = SSHFPComparison(domain=dns_sshfpd.domain, dns_sshfp=dns_sshfpd, server_sshfp=None, errors=[str(e)])
        server_logger.info(sshfp_comp.to_json())
        return None
    except Exception as e:
        sshfp_comp = SSHFPComparison(domain=dns_sshfpd.domain, dns_sshfp=dns_sshfpd, server_sshfp=None, errors=[str(e)])
        server_logger.info(sshfp_comp.to_json())
        return None

    server_sshfpd = SSHFPDomain(timestamp=int(time.time()), domain=dns_sshfpd.domain)
    sshfp_comp = SSHFPComparison(domain=dns_sshfpd.domain, dns_sshfp=dns_sshfpd, server_sshfp=server_sshfpd)
    errors = []
    for ip in a_records:
        try:
            # https://linux.die.net/man/1/ssh-keyscan
            proc = subprocess.run(['ssh-keyscan', '-D', '-4','-t', 'dsa,rsa,ecdsa,ed25519','-T','5', ip], capture_output=True)
            if proc.returncode > 0:
                raise Exception(f"SSH-Keyscan failed for domain={dns_sshfpd.domain} and ip={ip}")

            server_records = set(filter(lambda x: len(x)>0 and 'IN SSHFP' in x, proc.stdout.decode().split('\n')))
            if len(server_records) == 0:
                raise Exception(f"SSH-Keyscan returned no fingerprints")

            for record in server_records:
                record = re.sub(r'.*?IN SSHFP\s+','', record)
                sshfp = SSHFP.from_string(record)
                sshfp.timestamp = int(time.time())
                sshfp.domain = ip
                server_sshfpd.records.append(sshfp)
        except Exception as e:
            errors.append(f"ip={ip},e={e}")
    sshfp_comp.errors=errors

    try:
        # Check DNSSec validation
        # From https://stackoverflow.com/a/26137120
        req = dns.message.make_query(dns_sshfpd.domain, dns.rdatatype.SSHFP, want_dnssec=True)
        resp = dns.query.udp(req, where=dnssec_recursor_ip) # , timeout=5 ?

        rcode = resp.rcode()
        if rcode != 0:
            raise Exception(f"{dns.rcode.to_text(rcode)}")

        is_authentic = 'AD' in dns.flags.to_text(resp.flags)

        #print(f"Domain: {domain}: is_authentic={is_authentic}")
    except Exception as e:
        is_authentic = False
        sshfp_comp.errors.append(f"{e}")

    sshfp_comp.is_authentic = is_authentic

    server_logger.info(sshfp_comp.to_json())

def test_dnssec(task):
    domain = task 
    try:
        # From https://stackoverflow.com/a/26137120
        req = dns.message.make_query(domain, dns.rdatatype.SSHFP, want_dnssec=True)
        resp = dns.query.udp(req, where=dnssec_recursor_ip) # , timeout=5 ?

        rcode = resp.rcode()
        if rcode != 0:
            raise Exception(f"Failed to query {domain}: rcode={rcode} -> {dns.rcode.to_text(rcode)}")

        is_authentic = 'AD' in dns.flags.to_text(resp.flags)

        #print(f"Domain: {domain}: is_authentic={is_authentic}")
    except Exception as e:
        pass
        print(f"Domain failed: {domain}, {e}")

def init_pipeline():
    global PIPELINE
    query_stage = UnorderedStage(query_sshfp, QUERY_WORKERS)
    parse_stage = UnorderedStage(parse_sshfp, PARSER_WORKERS)
    server_stage = UnorderedStage(server_sshfp, SERVER_WORKERS, disable_result=True)

    query_stage.link(parse_stage)
    parse_stage.link(server_stage)

    PIPELINE = Pipeline(query_stage)

    # dnssec_stage = UnorderedStage(test_dnssec, 10, disable_result=True)
    # PIPELINE = Pipeline(dnssec_stage)

######
#
# Certstream
#
######
def certstream_callback(message, context):
    global PIPELINE

    if not message['message_type'] == "certificate_update":
        return

    all_domains = message['data']['leaf_cert']['all_domains']

    if len(all_domains) == 0:
        return

    for domain in all_domains:
        if domain[0] == '*':
            certstream_logger.info(f"Skipping Wildcard domain: {domain}")
            continue
        certstream_logger.info(f"Queueing domain {domain}")
        PIPELINE.put(domain)

def init_certstream():
    certstream.core.certstream_logger = certstream_logger
    certstream.listen_for_events(certstream_callback, url='wss://certstream.calidog.io/')
    print("Done")

######
#
# Domainfile
#
######

def init_domainfile():
    global PIPELINE
    domainfile_logger.info(f"Reading from file: {os.environ['DOMAINFILE']}")
    with open(os.environ['DOMAINFILE']) as csvfile:
        domainreader = csv.reader(csvfile, delimiter=',')
        for row in domainreader:
            try:
                domain = row[1]
            except:
                domain = row[0]
            domainfile_logger.info(f"Queueing domain {domain}")
            PIPELINE.put(domain)
            time.sleep(1/(1*1000))

def main():
    init_pipeline()

    if os.environ['DOMAINSOURCE'].lower() == 'domainfile':
        init_domainfile()
    elif os.environ['DOMAINSOURCE'].lower() == 'certstream':
        init_certstream()
    else:
        print("Unknown DOMAINSOURCE. Please specify!")
        sys.exit(1)

    PIPELINE.put(None)

if __name__ == "__main__":
    main()