#!/usr/bin/env python3

#import paramiko
# import socket
import subprocess
import time
import re
import csv
from libsshfp import SSHFP, SSHFPDomain, SSHFPComparison

INPUTFILE = "../data/logs/results.log"

SSHFPDOMAINS = {}

with open(INPUTFILE) as inf:
    csvr = csv.reader(inf)
    for row in csvr:
        try:
            timestamp = int(row[0])
            domain = row[1]
            fpalgo = row[2]
            fptype = row[3]
            fphash = row[4]

            if not domain in SSHFPDOMAINS:
                SSHFPDOMAINS[domain] = {}
                SSHFPDOMAINS[domain]['dns'] = SSHFPDomain(timestamp, domain, [])

            sshfp = SSHFP(SSHFP.algo_to_id(fpalgo), SSHFP.type_to_id(fptype), fphash, domain=domain, timestamp=timestamp)
            SSHFPDOMAINS[domain]['dns'].records.append(sshfp)
        except Exception as e:
            print(e)

for domain in SSHFPDOMAINS:
    try:
        proc = subprocess.run(['ssh-keyscan', '-D', domain], capture_output=True)
        if proc.returncode > 0:
            raise Exception(f"SSH-Keyscan failed for {domain}")

        server_records = set(filter(lambda x: len(x)>0, proc.stdout.decode().split('\n')))

        dns_sshfpd = SSHFPDOMAINS[domain]['dns']
        server_sshfpd = SSHFPDomain(int(time.time()), dns_sshfpd.domain, [])
        dns_records = set(filter(lambda x: len(x)>0 and 'IN SSHFP' in x, dns_sshfpd.to_dns().split('\n')))
        for record in dns_records:
            record = re.sub(r'.*?IN SSHFP\s+','', record)
            sshfp = SSHFP.from_string(record)
            sshfp.timestamp = server_sshfpd.timestamp
            sshfp.domain = server_sshfpd.domain
            server_sshfpd.records.append(sshfp)

        sshfp_comp = SSHFPComparison(dns_sshfpd, server_sshfpd)
        print(sshfp_comp.to_json())
    except Exception as e:
        sshfp_comp = SSHFPComparison(None, None, error=str(e))
    print(sshfp_comp.to_json())

# for record in RECORDS:
#     try:
#         proc = subprocess.run(['ssh-keyscan', '-D', record.domain], capture_output=True)
#         if proc.returncode > 0:
#             raise Exception(f"SSH-Keyscan failed for {record.domain}")

#         for line in proc.stdout.decode().split('\n'):
#             print(line)
#     except Exception as e:
#         print(e)
# PORT = 22
# CONN_TIMEOUT = 10
# BANN_TIMEOUT = 10
# dummyclient = paramiko.client.SSHClient()

# for record in RECORDS:
#     hostname = record.domain
#     # From https://github.com/paramiko/paramiko/blob/main/paramiko/client.py#L340
#     for af, addr in list(dummyclient._families_and_addresses(hostname, PORT)):
#         try:
#             sock = socket.socket(af, socket.SOCK_STREAM)
#             print(f"[{hostname}] Connecting to {addr}")
#             sock.settimeout(CONN_TIMEOUT)
#             sock.connect(addr)

#             # From https://github.com/paramiko/paramiko/blob/main/paramiko/client.py#L406
#             t = paramiko.transport.Transport(sock)
#             t.banner_timeout = BANN_TIMEOUT
#             t.start_client(timeout=CONN_TIMEOUT)
#             hkey = t.get_remote_server_key()
#             hkey_type = hkey.get_name()
#             hkey_fp = hkey.get_fingerprint().hex()
#             #import ipdb; ipdb.set_trace()

#             print(f"{hkey_type}, {hkey_fp} vs. {record.algo_stringified()} - {record.type_stringified()} - {record.fingerprint}")
#         except Exception as e:
#             print(e)