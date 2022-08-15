#!/usr/bin/env python3

# grep "INFO:root:{'domain'" app.log > sshfp_certstream.txt
# sed -e 's/INFO:root://' sshfp_certstream.txt > sshfp_certstream.json
import json
import re
import csv
from libsshfp import SSHFP

INPUTFILE="../data/sshfp_certstream.json"
OUTFILE="../data/sshfp_certstream.csv"

class DomainSSHFP:
    def __init__(self, domain, records, timestamp):
        self.domain = domain
        self.records = records
        self.timestamp = timestamp

SSHFPDOMAINS = []
with open(INPUTFILE) as f:
    for line in f:
        line = line.strip()
        line = line.replace("'", '"')
        data = json.loads(line)
        dfp = DomainSSHFP(data['domain'], set([]), data['tstmp'])
        for record in data['records']:
            try:
                fp = SSHFP.from_string(record)
                dfp.records.add(fp)
            except Exception as e:
                pass
                #print(f"!! Invalid FP for domain {data['domain']}: {e}")
        SSHFPDOMAINS.append(dfp)

dupes = 0
csv_records = set()
for d in SSHFPDOMAINS:
    for fp in d.records:
        csv_record = f"{d.timestamp},{d.domain},{fp.algo_stringified()},{fp.type_stringified()},{fp.fingerprint}"
        if csv_record in csv_records:
            dupes += 1
        else:
            csv_records.add(csv_record)
#            print(csv_record)
with open(OUTFILE, "w") as of:
    csvw = csv.writer(of)
    csvw.writerow(['timestamp', 'domain', 'algo', 'type', 'fingerprint'])
    for csv_record in csv_records:
        csvw.writerow(csv_record.split(","))