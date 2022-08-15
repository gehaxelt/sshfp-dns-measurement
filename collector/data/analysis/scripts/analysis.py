import sys
import statistics
import tldextract
import json
import os
import ast
import time
import matplotlib.pyplot as pyplot

from collections import Counter

from config import config
import utils
from libsshfp import SSHFP

# pyplot.style.use(['bright'])
# pyplot.rcParams['text.usetex'] = True
# pyplot.rcParams['font.size'] = 9
# pyplot.rcParams['legend.fontsize'] = 9
# pyplot.rcParams['xtick.direction'] = 'out'
# pyplot.rcParams['ytick.direction'] = 'out'

# def getColor(c, N, idx):
#     import matplotlib as mpl
#     cmap = mpl.cm.get_cmap(c)
#     norm = mpl.colors.Normalize(vmin=0.0, vmax=N - 1)
#     return cmap(norm(idx))

def domainfile_general_numbers_scanned_domains():
	TOTAL_COUNTER = 0
	DOMAIN_COUNTER = 0

	SCAN_CLASSES_COUNTER = Counter()
	FLD_COUNTER = Counter()
	UNIQUE_DOMAIN_COUNTER = Counter()
	
	OUTPUT_STR = ""

	with open(config.DOMAINFILE_COUNTED_UNIQUE_DOMAINS + "_unique_domains.csv") as f:
		next(f) # Skip header: Count,UniqueDomain
		for line in f:
			line = line.strip()
			lsplit = line.split(",")
			count = int(lsplit[0])
			domain = lsplit[1].replace('"', '')

			UNIQUE_DOMAIN_COUNTER.update([domain] * count)

			d = tldextract.extract(domain)
			fld = f"{d.domain}.{d.suffix}"
			FLD_COUNTER.update([fld])

			SCAN_CLASSES_COUNTER.update([count])

			TOTAL_COUNTER += count
			DOMAIN_COUNTER += 1

		average_SCAN_v = statistics.mean(SCAN_CLASSES_COUNTER.values())
		median_SCAN_v = statistics.median(SCAN_CLASSES_COUNTER.values())
		min_SCAN_v = min(SCAN_CLASSES_COUNTER.values())
		max_SCAN_v = max(SCAN_CLASSES_COUNTER.values())

		average_SCAN_k = statistics.mean(SCAN_CLASSES_COUNTER.keys())
		median_SCAN_k = statistics.median(SCAN_CLASSES_COUNTER.keys())
		min_SCAN_k = min(SCAN_CLASSES_COUNTER.keys())
		max_SCAN_k = max(SCAN_CLASSES_COUNTER.keys())

		average_flds = statistics.mean(FLD_COUNTER.values())
		median_flds = statistics.median(FLD_COUNTER.values())
		total_flds = sum(FLD_COUNTER.values())
		most_common_flds = FLD_COUNTER.most_common(10) 

		average_unique_domains = statistics.mean(UNIQUE_DOMAIN_COUNTER.values())
		median_unique_domains = statistics.median(UNIQUE_DOMAIN_COUNTER.values())
		total_unique_domains = sum(UNIQUE_DOMAIN_COUNTER.values())
		most_common_unique_domains = UNIQUE_DOMAIN_COUNTER.most_common(10) 


	OUTPUT_STR += f"TOTAL # OF SCANS: {TOTAL_COUNTER}\n"
	OUTPUT_STR += f"SCANNED # OF DOMAINS: {DOMAIN_COUNTER}\n"
	OUTPUT_STR += f"AVERAGE SCANS per Domain: {TOTAL_COUNTER/DOMAIN_COUNTER}\n"
	OUTPUT_STR += f"SCAN CLASSES VALUES (avg, median, min, max): {average_SCAN_v}, {median_SCAN_v}, {min_SCAN_v}, {max_SCAN_v}\n"
	OUTPUT_STR += f"SCAN CLASSES KEYS (avg, median, min, max): {average_SCAN_k}, {median_SCAN_k}, {min_SCAN_k}, {max_SCAN_k}\n"

	OUTPUT_STR += f"FLD COUNTER values (unique flds, total count, avg, median, 10 most_common): {len(FLD_COUNTER.keys())}, {total_flds}, {average_flds}, {median_flds}, {most_common_flds} \n"
	
	OUTPUT_STR += f"UNIQUE DOMAIN COUNTER values (unique domains, total count, avg, median, 10 most_common): {len(UNIQUE_DOMAIN_COUNTER.keys())}, {total_unique_domains}, {average_unique_domains}, {median_unique_domains}, {most_common_unique_domains} \n"
	
	with open(config.DOMAINFILE_ANALYSIS_SCANNED_OUTFILE, "w") as f:
		f.write(OUTPUT_STR)


def cerstream_general_numbers_skipped():
	TOTAL_COUNTER = 0
	SKIP_COUNTER = 0
	
	SKIP_CLASSES_COUNTER = Counter()
	FLD_COUNTER = Counter()
	UNIQUE_DOMAIN_COUNTER = Counter()

	OUTPUT_STR = ""

	with open(config.CERTSTREAM_COUNTED_UNIQUE_DOMAINS + "_skipped_domains.csv") as f:
		next(f) # Skip header: Count,SkippedDomain
		for line in f:
			lsplit = line.split(",")
			count = int(lsplit[0])
			domain = lsplit[1].replace('"', '')
			UNIQUE_DOMAIN_COUNTER.update([domain]* count)


			d = tldextract.extract(domain)
			fld = f"{d.domain}.{d.suffix}"
			FLD_COUNTER.update([fld])

			SKIP_CLASSES_COUNTER.update([count])

			TOTAL_COUNTER += count
			SKIP_COUNTER += 1

		average_skips_v = statistics.mean(SKIP_CLASSES_COUNTER.values())
		median_skips_v = statistics.median(SKIP_CLASSES_COUNTER.values())
		min_skips_v = min(SKIP_CLASSES_COUNTER.values())
		max_skips_v = max(SKIP_CLASSES_COUNTER.values())

		average_skips_k = statistics.mean(SKIP_CLASSES_COUNTER.keys())
		median_skips_k = statistics.median(SKIP_CLASSES_COUNTER.keys())
		min_skips_k = min(SKIP_CLASSES_COUNTER.keys())
		max_skips_k = max(SKIP_CLASSES_COUNTER.keys())

		average_flds = statistics.mean(FLD_COUNTER.values())
		median_flds = statistics.median(FLD_COUNTER.values())
		total_flds = sum(FLD_COUNTER.values())
		most_common_flds = FLD_COUNTER.most_common(10) 
		
		average_unique_domains = statistics.mean(UNIQUE_DOMAIN_COUNTER.values())
		median_unique_domains = statistics.median(UNIQUE_DOMAIN_COUNTER.values())
		total_unique_domains = sum(UNIQUE_DOMAIN_COUNTER.values())
		most_common_unique_domains = UNIQUE_DOMAIN_COUNTER.most_common(10) 

	OUTPUT_STR += f"TOTAL # OF SKIPS: {TOTAL_COUNTER}\n"
	OUTPUT_STR += f"SKIPPED # OF DOMAINS: {SKIP_COUNTER}\n"
	OUTPUT_STR += f"AVERAGE SKIPS: {TOTAL_COUNTER/SKIP_COUNTER}\n"
	OUTPUT_STR += f"SKIP CLASSES VALUES (avg, median, min, max): {average_skips_v}, {median_skips_v}, {min_skips_v}, {max_skips_v}\n"
	OUTPUT_STR += f"SKIP CLASSES KEYS (avg, median, min, max): {average_skips_k}, {median_skips_k}, {min_skips_k}, {max_skips_k}\n"

	OUTPUT_STR += f"FLD COUNTER values (unique flds, total count, avg, median, 10 most_common): {len(FLD_COUNTER.keys())}, {total_flds}, {average_flds}, {median_flds}, {most_common_flds} \n"
	
	OUTPUT_STR += f"UNIQUE DOMAIN COUNTER values (unique domains, total count, avg, median, 10 most_common): {len(UNIQUE_DOMAIN_COUNTER.keys())}, {total_unique_domains}, {average_unique_domains}, {median_unique_domains}, {most_common_unique_domains} \n"
	
	with open(config.CERTSTREAM_ANALYSIS_SKIPPED_OUTFILE, "w") as f:
		f.write(OUTPUT_STR)


def cerstream_general_numbers_scanned_domains():
	TOTAL_COUNTER = 0
	DOMAIN_COUNTER = 0

	SCAN_CLASSES_COUNTER = Counter()
	FLD_COUNTER = Counter()
	UNIQUE_DOMAIN_COUNTER = Counter()
	
	OUTPUT_STR = ""

	with open(config.CERTSTREAM_COUNTED_UNIQUE_DOMAINS + "_unique_domains.csv") as f:
		next(f) # Skip header: Count,UniqueDomain
		for line in f:
			lsplit = line.split(",")
			count = int(lsplit[0])
			domain = lsplit[1].replace('"', '')
			UNIQUE_DOMAIN_COUNTER.update([domain]* count)

			d = tldextract.extract(domain)
			fld = f"{d.domain}.{d.suffix}"
			FLD_COUNTER.update([fld])

			SCAN_CLASSES_COUNTER.update([count])

			TOTAL_COUNTER += count
			DOMAIN_COUNTER += 1

		average_SCAN_v = statistics.mean(SCAN_CLASSES_COUNTER.values())
		median_SCAN_v = statistics.median(SCAN_CLASSES_COUNTER.values())
		min_SCAN_v = min(SCAN_CLASSES_COUNTER.values())
		max_SCAN_v = max(SCAN_CLASSES_COUNTER.values())

		average_SCAN_k = statistics.mean(SCAN_CLASSES_COUNTER.keys())
		median_SCAN_k = statistics.median(SCAN_CLASSES_COUNTER.keys())
		min_SCAN_k = min(SCAN_CLASSES_COUNTER.keys())
		max_SCAN_k = max(SCAN_CLASSES_COUNTER.keys())

		average_flds = statistics.mean(FLD_COUNTER.values())
		median_flds = statistics.median(FLD_COUNTER.values())
		total_flds = sum(FLD_COUNTER.values())
		most_common_flds = FLD_COUNTER.most_common(10) 

		average_unique_domains = statistics.mean(UNIQUE_DOMAIN_COUNTER.values())
		median_unique_domains = statistics.median(UNIQUE_DOMAIN_COUNTER.values())
		total_unique_domains = sum(UNIQUE_DOMAIN_COUNTER.values())
		most_common_unique_domains = UNIQUE_DOMAIN_COUNTER.most_common(10) 

	OUTPUT_STR += f"TOTAL # OF SCANS: {TOTAL_COUNTER}\n"
	OUTPUT_STR += f"SCANNED # OF DOMAINS: {DOMAIN_COUNTER}\n"
	OUTPUT_STR += f"AVERAGE SCANS per Domain: {TOTAL_COUNTER/DOMAIN_COUNTER}\n"
	OUTPUT_STR += f"SCAN CLASSES VALUES (avg, median, min, max): {average_SCAN_v}, {median_SCAN_v}, {min_SCAN_v}, {max_SCAN_v}\n"
	OUTPUT_STR += f"SCAN CLASSES KEYS (avg, median, min, max): {average_SCAN_k}, {median_SCAN_k}, {min_SCAN_k}, {max_SCAN_k}\n"

	OUTPUT_STR += f"FLD COUNTER values (unique flds, total count, avg, median, 10 most_common): {len(FLD_COUNTER.keys())}, {total_flds}, {average_flds}, {median_flds}, {most_common_flds} \n"
	
	OUTPUT_STR += f"UNIQUE DOMAIN COUNTER values (unique domains, total count, avg, median, 10 most_common): {len(UNIQUE_DOMAIN_COUNTER.keys())}, {total_unique_domains}, {average_unique_domains}, {median_unique_domains}, {most_common_unique_domains} \n"
	
	with open(config.CERTSTREAM_ANALYSIS_SCANNED_OUTFILE, "w") as f:
		f.write(OUTPUT_STR)

def query_log_analysis():
	# https://dnspython.readthedocs.io/en/latest/exceptions.html
	# DNS_ERR_NO_SSHFP -> The DNS response does not contain an answer to the question => No SSHFP record is set.
	# DNS_ERR_NO_ANSWER -> All nameservers failed to answer the query => SERVFAIL from our DNS-Resolver and/or timeout or simply no SSHFP record (stichprobenweise getestet mit Dig). // Response was a delegation not an answer (?) / https://stackoverflow.com/a/20459494
		# -> ;; flags: qr rd ra; QUERY: 1, ANSWER: 0, AUTHORITY: 0, ADDITIONAL: 1 -> NO SSHFP
	# DNS_ERR_NO_QUERYNAME -> The DNS query name does not exist => NXDOMAIN, domain does not exist.
		# -> Stichproben zeigen: Kein SSHFP record returned
		# ;; flags: qr rd ra; QUERY: 1, ANSWER: 0, AUTHORITY: 1, ADDITIONAL: 1
	# DNS_ERR_TIMEOUT -> The DNS operation timed out after => Timeout of 5 seconds, i.e. reaching a nameserver during recursion?
	# DNS_ERR_LABEL -> 'A DNS label is > 63 octets long' => Label is invalid or too long.
	
	NO_SSHFP_TOTAL_COUNTER = 0
	NO_SSHFP_DOMAIN_COUNTER = 0

	NO_SSHFP_CLASSES_COUNTER = Counter()
	NO_SSHFP_FLD_COUNTER = Counter()
	UNIQUE_DOMAIN_COUNTER = Counter()
	
	NO_SSHFP_OUTPUT_STR = ""

	with open(config.QUERY_LOG_COUNTED_MESSAGES + "_err_no_sshfp.csv") as f:
		next(f) # Skip header: Count,DomainWithErrNoSSHFP
		for line in f:
			line = line.strip()
			lsplit = line.split(",")
			count = int(lsplit[0])
			domain = lsplit[1].replace('"', '')
			UNIQUE_DOMAIN_COUNTER.update([domain]* count)

			d = tldextract.extract(domain)
			fld = f"{d.domain}.{d.suffix}"
			NO_SSHFP_FLD_COUNTER.update([fld])

			NO_SSHFP_CLASSES_COUNTER.update([count])

			NO_SSHFP_TOTAL_COUNTER += count
			NO_SSHFP_DOMAIN_COUNTER += 1
		
		average_NO_SSHFP_v = statistics.mean(NO_SSHFP_CLASSES_COUNTER.values())
		median_NO_SSHFP_v = statistics.median(NO_SSHFP_CLASSES_COUNTER.values())
		min_NO_SSHFP_v = min(NO_SSHFP_CLASSES_COUNTER.values())
		max_NO_SSHFP_v = max(NO_SSHFP_CLASSES_COUNTER.values())

		average_NO_SSHFP_k = statistics.mean(NO_SSHFP_CLASSES_COUNTER.keys())
		median_NO_SSHFP_k = statistics.median(NO_SSHFP_CLASSES_COUNTER.keys())
		min_NO_SSHFP_k = min(NO_SSHFP_CLASSES_COUNTER.keys())
		max_NO_SSHFP_k = max(NO_SSHFP_CLASSES_COUNTER.keys())

		average_NO_SSHFP_flds = statistics.mean(NO_SSHFP_FLD_COUNTER.values())
		median_NO_SSHFP_flds = statistics.median(NO_SSHFP_FLD_COUNTER.values())
		total_NO_SSHFP_flds = sum(NO_SSHFP_FLD_COUNTER.values())
		most_common_NO_SSHFP_flds = NO_SSHFP_FLD_COUNTER.most_common(10) 

		average_unique_domains = statistics.mean(UNIQUE_DOMAIN_COUNTER.values())
		median_unique_domains = statistics.median(UNIQUE_DOMAIN_COUNTER.values())
		total_unique_domains = sum(UNIQUE_DOMAIN_COUNTER.values())
		most_common_unique_domains = UNIQUE_DOMAIN_COUNTER.most_common(10) 

	NO_SSHFP_OUTPUT_STR += f"TOTAL # OF NO SSHFP ERRORS: {NO_SSHFP_TOTAL_COUNTER}\n"
	NO_SSHFP_OUTPUT_STR += f"NO SSHFP ERRORS # OF DOMAINS: {NO_SSHFP_DOMAIN_COUNTER}\n"
	NO_SSHFP_OUTPUT_STR += f"AVERAGE NO SSHFP ERRORS per Domain: {NO_SSHFP_TOTAL_COUNTER/NO_SSHFP_DOMAIN_COUNTER}\n"
	NO_SSHFP_OUTPUT_STR += f"NO SSHFP CLASSES VALUES (avg, median, min, max): {average_NO_SSHFP_v}, {median_NO_SSHFP_v}, {min_NO_SSHFP_v}, {max_NO_SSHFP_v}\n"
	NO_SSHFP_OUTPUT_STR += f"NO SSHFP CLASSES KEYS (avg, median, min, max): {average_NO_SSHFP_k}, {median_NO_SSHFP_k}, {min_NO_SSHFP_k}, {max_NO_SSHFP_k}\n"

	NO_SSHFP_OUTPUT_STR += f"NO SSHFP FLD COUNTER values (unique flds, total count, avg, median, 10 most_common): {len(NO_SSHFP_FLD_COUNTER.keys())}, {total_NO_SSHFP_flds}, {average_NO_SSHFP_flds}, {median_NO_SSHFP_flds}, {most_common_NO_SSHFP_flds} \n"
	
	NO_SSHFP_OUTPUT_STR += f"NO SSHFP UNIQUE DOMAIN COUNTER values (unique domains, total count, avg, median, 10 most_common): {len(UNIQUE_DOMAIN_COUNTER.keys())}, {total_unique_domains}, {average_unique_domains}, {median_unique_domains}, {most_common_unique_domains} \n"
	
	print(NO_SSHFP_OUTPUT_STR)
	with open(config.QUERYLOG_ANALYSIS_OUTFILE_NO_SSHFP, "w") as f:
		f.write(NO_SSHFP_OUTPUT_STR)



	NO_ANSWER_TOTAL_COUNTER = 0
	NO_ANSWER_DOMAIN_COUNTER = 0

	NO_ANSWER_CLASSES_COUNTER = Counter()
	NO_ANSWER_FLD_COUNTER = Counter()
	UNIQUE_DOMAIN_COUNTER = Counter()
	
	NO_ANSWER_OUTPUT_STR = ""

	with open(config.QUERY_LOG_COUNTED_MESSAGES + "_err_no_answer.csv") as f:
		next(f) # Skip header: Count,DomainWithErrNoAnswer
		for line in f:
			line = line.strip()
			lsplit = line.split(",")
			count = int(lsplit[0])
			domain = lsplit[1].replace('"', '')
			UNIQUE_DOMAIN_COUNTER.update([domain]* count)

			d = tldextract.extract(domain)
			fld = f"{d.domain}.{d.suffix}"
			NO_ANSWER_FLD_COUNTER.update([fld])

			NO_ANSWER_CLASSES_COUNTER.update([count])

			NO_ANSWER_TOTAL_COUNTER += count
			NO_ANSWER_DOMAIN_COUNTER += 1
		
		average_NO_ANSWER_v = statistics.mean(NO_ANSWER_CLASSES_COUNTER.values())
		median_NO_ANSWER_v = statistics.median(NO_ANSWER_CLASSES_COUNTER.values())
		min_NO_ANSWER_v = min(NO_ANSWER_CLASSES_COUNTER.values())
		max_NO_ANSWER_v = max(NO_ANSWER_CLASSES_COUNTER.values())

		average_NO_ANSWER_k = statistics.mean(NO_ANSWER_CLASSES_COUNTER.keys())
		median_NO_ANSWER_k = statistics.median(NO_ANSWER_CLASSES_COUNTER.keys())
		min_NO_ANSWER_k = min(NO_ANSWER_CLASSES_COUNTER.keys())
		max_NO_ANSWER_k = max(NO_ANSWER_CLASSES_COUNTER.keys())

		average_NO_ANSWER_flds = statistics.mean(NO_ANSWER_FLD_COUNTER.values())
		median_NO_ANSWER_flds = statistics.median(NO_ANSWER_FLD_COUNTER.values())
		total_NO_ANSWER_flds = sum(NO_ANSWER_FLD_COUNTER.values())
		most_common_NO_ANSWER_flds = NO_ANSWER_FLD_COUNTER.most_common(10) 

		average_unique_domains = statistics.mean(UNIQUE_DOMAIN_COUNTER.values())
		median_unique_domains = statistics.median(UNIQUE_DOMAIN_COUNTER.values())
		total_unique_domains = sum(UNIQUE_DOMAIN_COUNTER.values())
		most_common_unique_domains = UNIQUE_DOMAIN_COUNTER.most_common(10) 

	NO_ANSWER_OUTPUT_STR += f"TOTAL # OF NO ANSWER ERRORS: {NO_ANSWER_TOTAL_COUNTER}\n"
	NO_ANSWER_OUTPUT_STR += f"NO ANSWER ERRORS # OF DOMAINS: {NO_ANSWER_DOMAIN_COUNTER}\n"
	NO_ANSWER_OUTPUT_STR += f"AVERAGE NO ANSWER ERRORS per Domain: {NO_ANSWER_TOTAL_COUNTER/NO_ANSWER_DOMAIN_COUNTER}\n"
	NO_ANSWER_OUTPUT_STR += f"NO ANSWER CLASSES VALUES (avg, median, min, max): {average_NO_ANSWER_v}, {median_NO_ANSWER_v}, {min_NO_ANSWER_v}, {max_NO_ANSWER_v}\n"
	NO_ANSWER_OUTPUT_STR += f"NO ANSWER CLASSES KEYS (avg, median, min, max): {average_NO_ANSWER_k}, {median_NO_ANSWER_k}, {min_NO_ANSWER_k}, {max_NO_ANSWER_k}\n"

	NO_ANSWER_OUTPUT_STR += f"NO ANSWER FLD COUNTER values (unique flds, total count, avg, median, 10 most_common): {len(NO_ANSWER_FLD_COUNTER.keys())}, {total_NO_ANSWER_flds}, {average_NO_ANSWER_flds}, {median_NO_ANSWER_flds}, {most_common_NO_ANSWER_flds} \n"
	
	NO_ANSWER_OUTPUT_STR += f"NO ANSWER UNIQUE DOMAIN COUNTER values (unique domains, total count, avg, median, 10 most_common): {len(UNIQUE_DOMAIN_COUNTER.keys())}, {total_unique_domains}, {average_unique_domains}, {median_unique_domains}, {most_common_unique_domains} \n"
	
	print(NO_ANSWER_OUTPUT_STR)
	with open(config.QUERYLOG_ANALYSIS_OUTFILE_NO_ANSWER, "w") as f:
		f.write(NO_ANSWER_OUTPUT_STR)


	NO_QUERYNAME_TOTAL_COUNTER = 0
	NO_QUERYNAME_DOMAIN_COUNTER = 0

	NO_QUERYNAME_CLASSES_COUNTER = Counter()
	NO_QUERYNAME_FLD_COUNTER = Counter()
	UNIQUE_DOMAIN_COUNTER = Counter()
	
	NO_QUERYNAME_OUTPUT_STR = ""

	with open(config.QUERY_LOG_COUNTED_MESSAGES + "_err_no_queryname.csv") as f:
		next(f) # Skip header: Count,DomainWithErrNoAnswer
		for line in f:
			line = line.strip()
			lsplit = line.split(",")
			count = int(lsplit[0])
			domain = lsplit[1].replace('"', '')
			UNIQUE_DOMAIN_COUNTER.update([domain]* count)

			d = tldextract.extract(domain)
			fld = f"{d.domain}.{d.suffix}"
			NO_QUERYNAME_FLD_COUNTER.update([fld])

			NO_QUERYNAME_CLASSES_COUNTER.update([count])

			NO_QUERYNAME_TOTAL_COUNTER += count
			NO_QUERYNAME_DOMAIN_COUNTER += 1
		
		average_NO_QUERYNAME_v = statistics.mean(NO_QUERYNAME_CLASSES_COUNTER.values())
		median_NO_QUERYNAME_v = statistics.median(NO_QUERYNAME_CLASSES_COUNTER.values())
		min_NO_QUERYNAME_v = min(NO_QUERYNAME_CLASSES_COUNTER.values())
		max_NO_QUERYNAME_v = max(NO_QUERYNAME_CLASSES_COUNTER.values())

		average_NO_QUERYNAME_k = statistics.mean(NO_QUERYNAME_CLASSES_COUNTER.keys())
		median_NO_QUERYNAME_k = statistics.median(NO_QUERYNAME_CLASSES_COUNTER.keys())
		min_NO_QUERYNAME_k = min(NO_QUERYNAME_CLASSES_COUNTER.keys())
		max_NO_QUERYNAME_k = max(NO_QUERYNAME_CLASSES_COUNTER.keys())

		average_NO_QUERYNAME_flds = statistics.mean(NO_QUERYNAME_FLD_COUNTER.values())
		median_NO_QUERYNAME_flds = statistics.median(NO_QUERYNAME_FLD_COUNTER.values())
		total_NO_QUERYNAME_flds = sum(NO_QUERYNAME_FLD_COUNTER.values())
		most_common_NO_QUERYNAME_flds = NO_QUERYNAME_FLD_COUNTER.most_common(10) 

		average_unique_domains = statistics.mean(UNIQUE_DOMAIN_COUNTER.values())
		median_unique_domains = statistics.median(UNIQUE_DOMAIN_COUNTER.values())
		total_unique_domains = sum(UNIQUE_DOMAIN_COUNTER.values())
		most_common_unique_domains = UNIQUE_DOMAIN_COUNTER.most_common(10) 

	NO_QUERYNAME_OUTPUT_STR += f"TOTAL # OF NO QUERYNAME ERRORS: {NO_QUERYNAME_TOTAL_COUNTER}\n"
	NO_QUERYNAME_OUTPUT_STR += f"NO QUERYNAME ERRORS # OF DOMAINS: {NO_QUERYNAME_DOMAIN_COUNTER}\n"
	NO_QUERYNAME_OUTPUT_STR += f"AVERAGE NO QUERYNAME ERRORS per Domain: {NO_QUERYNAME_TOTAL_COUNTER/NO_QUERYNAME_DOMAIN_COUNTER}\n"
	NO_QUERYNAME_OUTPUT_STR += f"NO QUERYNAME CLASSES VALUES (avg, median, min, max): {average_NO_QUERYNAME_v}, {median_NO_QUERYNAME_v}, {min_NO_QUERYNAME_v}, {max_NO_QUERYNAME_v}\n"
	NO_QUERYNAME_OUTPUT_STR += f"NO QUERYNAME CLASSES KEYS (avg, median, min, max): {average_NO_QUERYNAME_k}, {median_NO_QUERYNAME_k}, {min_NO_QUERYNAME_k}, {max_NO_QUERYNAME_k}\n"

	NO_QUERYNAME_OUTPUT_STR += f"NO QUERYNAME FLD COUNTER values (unique flds, total count, avg, median, 10 most_common): {len(NO_QUERYNAME_FLD_COUNTER.keys())}, {total_NO_QUERYNAME_flds}, {average_NO_QUERYNAME_flds}, {median_NO_QUERYNAME_flds}, {most_common_NO_QUERYNAME_flds} \n"
	
	NO_QUERYNAME_OUTPUT_STR += f"NO QUERYNAME UNIQUE DOMAIN COUNTER values (unique domains, total count, avg, median, 10 most_common): {len(UNIQUE_DOMAIN_COUNTER.keys())}, {total_unique_domains}, {average_unique_domains}, {median_unique_domains}, {most_common_unique_domains} \n"
	
	print(NO_QUERYNAME_OUTPUT_STR)
	with open(config.QUERYLOG_ANALYSIS_OUTFILE_NO_QUERYNAME, "w") as f:
		f.write(NO_QUERYNAME_OUTPUT_STR)

	TIMEOUT_TOTAL_COUNTER = 0
	TIMEOUT_DOMAIN_COUNTER = 0

	TIMEOUT_CLASSES_COUNTER = Counter()
	TIMEOUT_FLD_COUNTER = Counter()
	UNIQUE_DOMAIN_COUNTER = Counter()
	
	TIMEOUT_OUTPUT_STR = ""

	with open(config.QUERY_LOG_COUNTED_MESSAGES + "_err_timeout.csv") as f:
		next(f) # Skip header: Count,DomainWithErrNoAnswer
		for line in f:
			line = line.strip()
			lsplit = line.split(",")
			count = int(lsplit[0])
			domain = lsplit[1].replace('"', '')
			UNIQUE_DOMAIN_COUNTER.update([domain]* count)

			d = tldextract.extract(domain)
			fld = f"{d.domain}.{d.suffix}"
			TIMEOUT_FLD_COUNTER.update([fld])

			TIMEOUT_CLASSES_COUNTER.update([count])

			TIMEOUT_TOTAL_COUNTER += count
			TIMEOUT_DOMAIN_COUNTER += 1
		
		average_TIMEOUT_v = statistics.mean(TIMEOUT_CLASSES_COUNTER.values())
		median_TIMEOUT_v = statistics.median(TIMEOUT_CLASSES_COUNTER.values())
		min_TIMEOUT_v = min(TIMEOUT_CLASSES_COUNTER.values())
		max_TIMEOUT_v = max(TIMEOUT_CLASSES_COUNTER.values())

		average_TIMEOUT_k = statistics.mean(TIMEOUT_CLASSES_COUNTER.keys())
		median_TIMEOUT_k = statistics.median(TIMEOUT_CLASSES_COUNTER.keys())
		min_TIMEOUT_k = min(TIMEOUT_CLASSES_COUNTER.keys())
		max_TIMEOUT_k = max(TIMEOUT_CLASSES_COUNTER.keys())

		average_TIMEOUT_flds = statistics.mean(TIMEOUT_FLD_COUNTER.values())
		median_TIMEOUT_flds = statistics.median(TIMEOUT_FLD_COUNTER.values())
		total_TIMEOUT_flds = sum(TIMEOUT_FLD_COUNTER.values())
		most_common_TIMEOUT_flds = TIMEOUT_FLD_COUNTER.most_common(10) 

		average_unique_domains = statistics.mean(UNIQUE_DOMAIN_COUNTER.values())
		median_unique_domains = statistics.median(UNIQUE_DOMAIN_COUNTER.values())
		total_unique_domains = sum(UNIQUE_DOMAIN_COUNTER.values())
		most_common_unique_domains = UNIQUE_DOMAIN_COUNTER.most_common(10) 

	TIMEOUT_OUTPUT_STR += f"TOTAL # OF ERR TIMEOUT ERRORS: {TIMEOUT_TOTAL_COUNTER}\n"
	TIMEOUT_OUTPUT_STR += f"ERR TIMEOUT ERRORS # OF DOMAINS: {TIMEOUT_DOMAIN_COUNTER}\n"
	TIMEOUT_OUTPUT_STR += f"AVERAGE ERR TIMEOUT ERRORS per Domain: {TIMEOUT_TOTAL_COUNTER/TIMEOUT_DOMAIN_COUNTER}\n"
	TIMEOUT_OUTPUT_STR += f"ERR TIMEOUT CLASSES VALUES (avg, median, min, max): {average_TIMEOUT_v}, {median_TIMEOUT_v}, {min_TIMEOUT_v}, {max_TIMEOUT_v}\n"
	TIMEOUT_OUTPUT_STR += f"ERR TIMEOUT CLASSES KEYS (avg, median, min, max): {average_TIMEOUT_k}, {median_TIMEOUT_k}, {min_TIMEOUT_k}, {max_TIMEOUT_k}\n"

	TIMEOUT_OUTPUT_STR += f"ERR TIMEOUT FLD COUNTER values (unique flds, total count, avg, median, 10 most_common): {len(TIMEOUT_FLD_COUNTER.keys())}, {total_TIMEOUT_flds}, {average_TIMEOUT_flds}, {median_TIMEOUT_flds}, {most_common_TIMEOUT_flds} \n"
	
	TIMEOUT_OUTPUT_STR += f"ERR TIMEOUT UNIQUE DOMAIN COUNTER values (unique domains, total count, avg, median, 10 most_common): {len(UNIQUE_DOMAIN_COUNTER.keys())}, {total_unique_domains}, {average_unique_domains}, {median_unique_domains}, {most_common_unique_domains} \n"
	
	print(TIMEOUT_OUTPUT_STR)
	with open(config.QUERYLOG_ANALYSIS_OUTFILE_TIMEOUT, "w") as f:
		f.write(TIMEOUT_OUTPUT_STR)


	LABEL_TOTAL_COUNTER = 0
	LABEL_DOMAIN_COUNTER = 0

	LABEL_CLASSES_COUNTER = Counter()
	LABEL_FLD_COUNTER = Counter()
	UNIQUE_DOMAIN_COUNTER = Counter()
	
	LABEL_OUTPUT_STR = ""

	with open(config.QUERY_LOG_COUNTED_MESSAGES + "_err_label.csv") as f:
		next(f) # Skip header: Count,DomainWithErrNoAnswer
		for line in f:
			line = line.strip()
			lsplit = line.split(",")
			count = int(lsplit[0])
			domain = lsplit[1].replace('"', '')
			UNIQUE_DOMAIN_COUNTER.update([domain]* count)

			d = tldextract.extract(domain)
			fld = f"{d.domain}.{d.suffix}"
			LABEL_FLD_COUNTER.update([fld])

			LABEL_CLASSES_COUNTER.update([count])

			LABEL_TOTAL_COUNTER += count
			LABEL_DOMAIN_COUNTER += 1
		
		if LABEL_CLASSES_COUNTER.values():
			average_LABEL_v = statistics.mean(LABEL_CLASSES_COUNTER.values())
			median_LABEL_v = statistics.median(LABEL_CLASSES_COUNTER.values())
			min_LABEL_v = min(LABEL_CLASSES_COUNTER.values())
			max_LABEL_v = max(LABEL_CLASSES_COUNTER.values())

			average_LABEL_k = statistics.mean(LABEL_CLASSES_COUNTER.keys())
			median_LABEL_k = statistics.median(LABEL_CLASSES_COUNTER.keys())
			min_LABEL_k = min(LABEL_CLASSES_COUNTER.keys())
			max_LABEL_k = max(LABEL_CLASSES_COUNTER.keys())

			average_LABEL_flds = statistics.mean(LABEL_FLD_COUNTER.values())
			median_LABEL_flds = statistics.median(LABEL_FLD_COUNTER.values())
			total_LABEL_flds = sum(LABEL_FLD_COUNTER.values())
			most_common_LABEL_flds = LABEL_FLD_COUNTER.most_common(10) 

			average_unique_domains = statistics.mean(UNIQUE_DOMAIN_COUNTER.values())
			median_unique_domains = statistics.median(UNIQUE_DOMAIN_COUNTER.values())
			total_unique_domains = sum(UNIQUE_DOMAIN_COUNTER.values())
			most_common_unique_domains = UNIQUE_DOMAIN_COUNTER.most_common(10) 

	if LABEL_CLASSES_COUNTER.values():
		LABEL_OUTPUT_STR += f"TOTAL # OF ERR LABEL ERRORS: {LABEL_TOTAL_COUNTER}\n"
		LABEL_OUTPUT_STR += f"ERR LABEL ERRORS # OF DOMAINS: {LABEL_DOMAIN_COUNTER}\n"
		LABEL_OUTPUT_STR += f"AVERAGE ERR LABEL ERRORS per Domain: {LABEL_TOTAL_COUNTER/LABEL_DOMAIN_COUNTER}\n"
		LABEL_OUTPUT_STR += f"ERR LABEL CLASSES VALUES (avg, median, min, max): {average_LABEL_v}, {median_LABEL_v}, {min_LABEL_v}, {max_LABEL_v}\n"
		LABEL_OUTPUT_STR += f"ERR LABEL CLASSES KEYS (avg, median, min, max): {average_LABEL_k}, {median_LABEL_k}, {min_LABEL_k}, {max_LABEL_k}\n"

		LABEL_OUTPUT_STR += f"ERR LABEL FLD COUNTER values (unique flds, total count, avg, median, 10 most_common): {len(LABEL_FLD_COUNTER.keys())}, {total_LABEL_flds}, {average_LABEL_flds}, {median_LABEL_flds}, {most_common_LABEL_flds} \n"
	
		LABEL_OUTPUT_STR += f"ERR LABEL UNIQUE DOMAIN COUNTER values (unique domains, total count, avg, median, 10 most_common): {len(UNIQUE_DOMAIN_COUNTER.keys())}, {total_unique_domains}, {average_unique_domains}, {median_unique_domains}, {most_common_unique_domains} \n"
	

	print(LABEL_OUTPUT_STR)
	with open(config.QUERYLOG_ANALYSIS_OUTFILE_LABEL, "w") as f:
		f.write(LABEL_OUTPUT_STR)


	FOUND_SSHFP_TOTAL_COUNTER = 0
	FOUND_SSHFP_DOMAIN_COUNTER = 0

	FOUND_SSHFP_CLASSES_COUNTER = Counter()
	FOUND_SSHFP_FLD_COUNTER = Counter()
	UNIQUE_DOMAIN_COUNTER = Counter()
	
	FOUND_SSHFP_OUTPUT_STR = ""

	with open(config.QUERY_LOG_COUNTED_MESSAGES + "_found_sshfp.csv") as f:
		next(f) # Skip header: Count,DomainWithErrNoAnswer
		for line in f:
			line = line.strip()
			lsplit = line.split(",")
			count = int(lsplit[0])
			domain = lsplit[1].replace('"', '')
			UNIQUE_DOMAIN_COUNTER.update([domain]* count)

			d = tldextract.extract(domain)
			fld = f"{d.domain}.{d.suffix}"
			FOUND_SSHFP_FLD_COUNTER.update([fld])

			FOUND_SSHFP_CLASSES_COUNTER.update([count])

			FOUND_SSHFP_TOTAL_COUNTER += count
			FOUND_SSHFP_DOMAIN_COUNTER += 1
		
		average_FOUND_SSHFP_v = statistics.mean(FOUND_SSHFP_CLASSES_COUNTER.values())
		median_FOUND_SSHFP_v = statistics.median(FOUND_SSHFP_CLASSES_COUNTER.values())
		min_FOUND_SSHFP_v = min(FOUND_SSHFP_CLASSES_COUNTER.values())
		max_FOUND_SSHFP_v = max(FOUND_SSHFP_CLASSES_COUNTER.values())

		average_FOUND_SSHFP_k = statistics.mean(FOUND_SSHFP_CLASSES_COUNTER.keys())
		median_FOUND_SSHFP_k = statistics.median(FOUND_SSHFP_CLASSES_COUNTER.keys())
		min_FOUND_SSHFP_k = min(FOUND_SSHFP_CLASSES_COUNTER.keys())
		max_FOUND_SSHFP_k = max(FOUND_SSHFP_CLASSES_COUNTER.keys())

		average_FOUND_SSHFP_flds = statistics.mean(FOUND_SSHFP_FLD_COUNTER.values())
		median_FOUND_SSHFP_flds = statistics.median(FOUND_SSHFP_FLD_COUNTER.values())
		total_FOUND_SSHFP_flds = sum(FOUND_SSHFP_FLD_COUNTER.values())
		most_common_FOUND_SSHFP_flds = FOUND_SSHFP_FLD_COUNTER.most_common(10) 

		average_unique_domains = statistics.mean(UNIQUE_DOMAIN_COUNTER.values())
		median_unique_domains = statistics.median(UNIQUE_DOMAIN_COUNTER.values())
		total_unique_domains = sum(UNIQUE_DOMAIN_COUNTER.values())
		most_common_unique_domains = UNIQUE_DOMAIN_COUNTER.most_common(10) 

	FOUND_SSHFP_OUTPUT_STR += f"TOTAL # OF FOUND_SSHFP: {FOUND_SSHFP_TOTAL_COUNTER}\n"
	FOUND_SSHFP_OUTPUT_STR += f"FOUND_SSHFP # OF DOMAINS: {FOUND_SSHFP_DOMAIN_COUNTER}\n"
	FOUND_SSHFP_OUTPUT_STR += f"AVERAGE FOUND_SSHFP per Domain: {FOUND_SSHFP_TOTAL_COUNTER/FOUND_SSHFP_DOMAIN_COUNTER}\n"
	FOUND_SSHFP_OUTPUT_STR += f"FOUND_SSHFP CLASSES VALUES (avg, median, min, max): {average_FOUND_SSHFP_v}, {median_FOUND_SSHFP_v}, {min_FOUND_SSHFP_v}, {max_FOUND_SSHFP_v}\n"
	FOUND_SSHFP_OUTPUT_STR += f"FOUND_SSHFP CLASSES KEYS (avg, median, min, max): {average_FOUND_SSHFP_k}, {median_FOUND_SSHFP_k}, {min_FOUND_SSHFP_k}, {max_FOUND_SSHFP_k}\n"

	FOUND_SSHFP_OUTPUT_STR += f"FOUND_SSHFP FLD COUNTER values (unique flds, total count, avg, median, 10 most_common): {len(FOUND_SSHFP_FLD_COUNTER.keys())}, {total_FOUND_SSHFP_flds}, {average_FOUND_SSHFP_flds}, {median_FOUND_SSHFP_flds}, {most_common_FOUND_SSHFP_flds} \n"
	
	FOUND_SSHFP_OUTPUT_STR += f"FOUND_SSHFP UNIQUE DOMAIN COUNTER values (unique domains, total count, avg, median, 10 most_common): {len(UNIQUE_DOMAIN_COUNTER.keys())}, {total_unique_domains}, {average_unique_domains}, {median_unique_domains}, {most_common_unique_domains} \n"
	
	print(FOUND_SSHFP_OUTPUT_STR)
	with open(config.QUERYLOG_ANALYSIS_OUTFILE_FOUND_SSHFP, "w") as f:
		f.write(FOUND_SSHFP_OUTPUT_STR)

def parserlog_analysis():
	data = json.load(open(config.PARSER_LOG_STRUCTED_DATA + "_structued_data.json"))
	
	#print(data.keys())
	ERROR_INCOMPLETE_SSHFP = []
	ERROR_INVALID_ALGO = []
	ERROR_INVALID_TYPE = []
	ERROR_HASH_NOT_SHA1 = []
	ERROR_HASH_NOT_SHA256 = []

	PROCESSED_FLDS = Counter()

	OUTPUT_STR = ""

	error_dict = {
		'invalid_algo': [],
		'invalid_type': [],
		'hash_not_sha1': [],
		'hash_not_sha256': []
	}

	for line in data['PARSER_ERR_NO_MATCH']:
		# line  -> 1642333166,www.kulturmel.ch,No match found,"1 1 c1e9072e81b77adfc6e5ed03ed0cb321cf6844ebc1e9072e81b77adfc6e5ed03ed0cb321cf6844eb"
		lsplit = line.split(",")
		tstmp = lsplit[0]
		domain = lsplit[1]
		errtype = lsplit[2]
		sshfp = lsplit[3].replace('"', '')

		key = f"{tstmp},{domain}"

		sshfp_split = sshfp.split(" ")
		if len(sshfp_split) != 3:
			ERROR_INCOMPLETE_SSHFP.append(key)
			continue

		sshfp_algo = int(sshfp_split[0])
		sshfp_type = int(sshfp_split[1])
		sshfp_fp = sshfp_split[2].strip()

		if sshfp_algo not in [SSHFP.ALGO_RESERVED, SSHFP.ALGO_RSA, SSHFP.ALGO_RSA, SSHFP.ALGO_DSA, SSHFP.ALGO_ECDSA, SSHFP.ALGO_ED25519, SSHFP.ALGO_ED448]:
			ERROR_INVALID_ALGO.append(key)
			error_dict['invalid_algo'].append(line)
			continue

		elif sshfp_type not in [SSHFP.TYPE_RESERVED, SSHFP.TYPE_SHA1, SSHFP.TYPE_SHA256]:
			ERROR_INVALID_TYPE.append(key)
			error_dict['invalid_type'].append(line)
			continue

		elif sshfp_type == SSHFP.TYPE_SHA1 and len(sshfp_fp) != 48:
			ERROR_HASH_NOT_SHA1.append(key)
			error_dict['hash_not_sha1'].append(line)
			continue

		elif sshfp_type == SSHFP.TYPE_SHA256 and len(sshfp_fp) != 80:
			ERROR_HASH_NOT_SHA256.append(key)
			error_dict['hash_not_sha256'].append(line)
			continue

		else:
			raise Exception(f"Unknown error: {line}")

	for line in data['PARSER_ERR_WRONG_FP']:
		lsplit = line.split(",")
		tstmp = lsplit[0]
		domain = lsplit[1]
		errtype = lsplit[2]
		fp = lsplit[3].replace('"', '')

		key = f"{tstmp},{domain}"


		if len(sshfp_fp) == 48:
			# should be SHA256 instead of SHA1
			ERROR_HASH_NOT_SHA256.append(key)
			error_dict['hash_not_sha256'].append(line)
			continue

		elif len(sshfp_fp) == 80:
			# Should be SHA1 instead of SHA256
			ERROR_HASH_NOT_SHA1.append(key)
			error_dict['hash_not_sha1'].append(line)
			continue

		else:
			raise Exception(f"Unknown error: {line}")

	total_error_sshpfs = len(data['PARSER_ERR_WRONG_FP']) + len(data['PARSER_ERR_NO_MATCH'])


	TOTAL_FLD_COUNTER = Counter()
	for entry in ERROR_INCOMPLETE_SSHFP + ERROR_INVALID_ALGO + ERROR_INVALID_TYPE + ERROR_HASH_NOT_SHA1 + ERROR_HASH_NOT_SHA256:
		_,domain = entry.split(",")
		d = tldextract.extract(domain)
		fld = f"{d.domain}.{d.suffix}"
		TOTAL_FLD_COUNTER.update([fld])
		PROCESSED_FLDS.update([fld])

	INCOMPLETE_SSHFP_FLD_COUNTER = Counter()
	for entry in ERROR_INCOMPLETE_SSHFP:
		_,domain = entry.split(",")
		d = tldextract.extract(domain)
		fld = f"{d.domain}.{d.suffix}"
		INCOMPLETE_SSHFP_FLD_COUNTER.update([fld])

	INVALID_ALGO_FLD_COUNTER = Counter()
	for entry in ERROR_INVALID_ALGO:
		_,domain = entry.split(",")
		d = tldextract.extract(domain)
		fld = f"{d.domain}.{d.suffix}"
		INVALID_ALGO_FLD_COUNTER.update([fld])

	INVALID_TYPE_FLD_COUNTER = Counter()
	for entry in ERROR_INVALID_TYPE:
		_,domain = entry.split(",")
		d = tldextract.extract(domain)
		fld = f"{d.domain}.{d.suffix}"
		INVALID_TYPE_FLD_COUNTER.update([fld])

	HASH_NOT_SHA1_FLD_COUNTER = Counter()
	for entry in ERROR_HASH_NOT_SHA1:
		_,domain = entry.split(",")
		d = tldextract.extract(domain)
		fld = f"{d.domain}.{d.suffix}"
		HASH_NOT_SHA1_FLD_COUNTER.update([fld])

	HASH_NOT_SHA256_FLD_COUNTER = Counter()
	for entry in ERROR_HASH_NOT_SHA256:
		_,domain = entry.split(",")
		d = tldextract.extract(domain)
		fld = f"{d.domain}.{d.suffix}"
		HASH_NOT_SHA256_FLD_COUNTER.update([fld])

	with open(config.PARSERLOG_ANALYSIS_OUTFILE + "_errors.txt", "w") as f:
		f.write(json.dumps(error_dict))

	OUTPUT_STR += "\n\n"
	OUTPUT_STR += f"Total errors (total/unique domains/unique flds): {total_error_sshpfs} / {len(set(ERROR_INCOMPLETE_SSHFP) | set(ERROR_INVALID_ALGO) | set(ERROR_INVALID_TYPE) | set(ERROR_HASH_NOT_SHA1) | set(ERROR_HASH_NOT_SHA256))} / {len(TOTAL_FLD_COUNTER.keys())}\n"
	OUTPUT_STR += f"Incomplete SSHFP (total/unique domains/unique flds): {len(ERROR_INCOMPLETE_SSHFP)} / {len(set(ERROR_INCOMPLETE_SSHFP))} / {len(INCOMPLETE_SSHFP_FLD_COUNTER.keys())}\n"
	OUTPUT_STR += f"Error invalid Algo (total/unique domains/unique flds): {len(ERROR_INVALID_ALGO)} / {len(set(ERROR_INVALID_ALGO))} / {len(INVALID_ALGO_FLD_COUNTER.keys())}\n"
	OUTPUT_STR += f"Error invalid Type (total/unique domains/unique flds): {len(ERROR_INVALID_TYPE)} / {len(set(ERROR_INVALID_TYPE))} / {len(INVALID_TYPE_FLD_COUNTER.keys())}\n"
	OUTPUT_STR += f"Error not SHA1 (total/unique domains/unique flds): {len(ERROR_HASH_NOT_SHA1)} / {len(set(ERROR_HASH_NOT_SHA1))} / {len(HASH_NOT_SHA1_FLD_COUNTER.keys())}\n"
	OUTPUT_STR += f"Error not SHA256 (total/unique domains/unique flds): {len(ERROR_HASH_NOT_SHA256)} / {len(set(ERROR_HASH_NOT_SHA256))} / {len(HASH_NOT_SHA256_FLD_COUNTER.keys())}\n"


	total_domains = len(data['STRUCTURED_DOMAINS'].keys())
	total_domains_unique = len(set(data['STRUCTURED_DOMAINS'].keys()))

	OUTPUT_STR += f"Total structured domains: {total_domains} (unique: {total_domains_unique})\n"

	SSHFP_FLDs = Counter()
	DNS_SCAN_INTERVAL_TIMES = Counter()
	SSHFP_UPDATES = Counter()
	SSHFP_UPDATE_TYPES = Counter()

	LIST_OF_SSHFP_RECORD_SETS = Counter()
	LIST_OF_SSHFP_RECORD_SINGLE = Counter()

	for domain in data['STRUCTURED_DOMAINS']:
		domain_sshfps = data['STRUCTURED_DOMAINS'][domain]

		d = tldextract.extract(domain)
		fld = f"{d.domain}.{d.suffix}"

		SSHFP_FLDs.update([fld])
		PROCESSED_FLDS.update([fld])

		if len(domain_sshfps) > 1:
			# print(domain_sshfps)
			# we scanned it multiple times:
			timestamps = sorted(list(map(lambda x: int(x), domain_sshfps.keys())))
			for i in range(0, len(timestamps)-1):
				diff_time = (timestamps[i+1] - timestamps[i])
				DNS_SCAN_INTERVAL_TIMES.update([diff_time])

			sshfp_list = sorted(domain_sshfps[str(timestamps[0])])
			sshfp_set = set(sshfp_list)

			LIST_OF_SSHFP_RECORD_SETS.update(['|'.join(sorted(sshfp_set))])
			LIST_OF_SSHFP_RECORD_SINGLE.update(sorted(sshfp_list))

			for i in range(1, len(timestamps)):
				other_list = sorted(domain_sshfps[str(timestamps[i])])
				other_set = set(other_list)

				LIST_OF_SSHFP_RECORD_SETS.update(['|'.join(sorted(other_set))])
				LIST_OF_SSHFP_RECORD_SINGLE.update(sorted(other_list))
				if sshfp_set != other_set:
					# print("SSHFPs have changed!")
					SSHFP_UPDATES.update([fld])


					# print("a", sshfp_set)
					# print("b", other_set)
					overlap_set = sshfp_set & other_set
					if not (overlap_set):
						SSHFP_UPDATE_TYPES.update(["All keys changed."])
						continue

					# Partial overlap, only a few keys changed.

					# SSHFP_UPDATE_TYPES.update(["No keys changed"])						
					added_keys = (sshfp_set | other_set) - sshfp_set						
					removed_keys = (sshfp_set | other_set) - other_set

					if len(added_keys) and len(removed_keys):
						 SSHFP_UPDATE_TYPES.update(["Partial update: Keys added and removed."])
					elif len(added_keys):
						SSHFP_UPDATE_TYPES.update(["Partial update: Keys added."])
					elif len(removed_keys):
						SSHFP_UPDATE_TYPES.update(["Partial update: Keys removed."])
					else:
						raise Exception("Should never happen.")


					sshfp_set = other_set
		else:
			# Only 1 domain_sshfp entry
			record_set = sorted(domain_sshfps[list(domain_sshfps.keys())[0]])
			LIST_OF_SSHFP_RECORD_SETS.update(['|'.join(sorted(record_set))])
			LIST_OF_SSHFP_RECORD_SINGLE.update(sorted(record_set))


	# print(SSHFP_UPDATES)
	OUTPUT_STR += "\n\n"
	OUTPUT_STR += f"SSHFP FLDs: (unique: {len(SSHFP_FLDs)} / total: {sum(SSHFP_FLDs.values())})\n"
	OUTPUT_STR += f"SSHFP Updates (unique: {len(SSHFP_UPDATES)} / total: {sum(SSHFP_UPDATE_TYPES.values())}): {SSHFP_UPDATES}\n"
	OUTPUT_STR += f"SSHFP Update Types: {SSHFP_UPDATE_TYPES}\n"
	OUTPUT_STR += f"SSHFP Record sets (unique: {len(LIST_OF_SSHFP_RECORD_SETS)} /  total: {sum(LIST_OF_SSHFP_RECORD_SETS.values())})\n"
	OUTPUT_STR += f"SSHFP Record sets top 10: {LIST_OF_SSHFP_RECORD_SETS.most_common(10)}\n"

	OUTPUT_STR += f"SSHFP Record single (unique: {len(LIST_OF_SSHFP_RECORD_SINGLE)}/ total: {sum(LIST_OF_SSHFP_RECORD_SINGLE.values())})\n"
	OUTPUT_STR += f"SSHFP Record single top 10: {LIST_OF_SSHFP_RECORD_SINGLE.most_common(10)}\n"
	#print(LIST_OF_SSHFP_RECORD_SETS)
	#print(LIST_OF_SSHFP_RECORD_SETS.most_common(10))


	SSHFP_ALGO_COUNTER = Counter()
	SSHFP_TYPE_COUNTER = Counter()
	SSHFP_ALGO_TYPE_PAIRS = Counter()

	for sshfp in LIST_OF_SSHFP_RECORD_SINGLE.keys():
		sshfp_split = sshfp.split(",")
		sshfp_algo = sshfp_split[0]
		sshfp_type = sshfp_split[1]
		factor = LIST_OF_SSHFP_RECORD_SINGLE[sshfp]

		SSHFP_ALGO_COUNTER.update([sshfp_algo])
		SSHFP_TYPE_COUNTER.update([sshfp_type]) 
		SSHFP_ALGO_TYPE_PAIRS.update([f"{sshfp_algo},{sshfp_type}"])

	OUTPUT_STR += "\n\n"
	OUTPUT_STR += f"SSHFP ALGOs (total: {sum(SSHFP_ALGO_COUNTER.values())}): {SSHFP_ALGO_COUNTER}\n"
	OUTPUT_STR += f"SSHFP TYPEs (total: {sum(SSHFP_TYPE_COUNTER.values())}): {SSHFP_TYPE_COUNTER}\n"
	OUTPUT_STR += f"SSHFP ALGO/TYPE Pairs (total: {sum(SSHFP_ALGO_TYPE_PAIRS.values())}): {SSHFP_ALGO_TYPE_PAIRS}\n"

	DNS_SCAN_INTERVAL_TIME_CLASSES = {}
	for k in DNS_SCAN_INTERVAL_TIMES:
		count = DNS_SCAN_INTERVAL_TIMES[k]
		minutes = k // 60
		hours = minutes // 60
		days = hours // 24

		if not days in DNS_SCAN_INTERVAL_TIME_CLASSES:
			DNS_SCAN_INTERVAL_TIME_CLASSES[days] = 0
		DNS_SCAN_INTERVAL_TIME_CLASSES[days] += count

	sorted_scan_intervals_classes = {}
	for k in sorted(DNS_SCAN_INTERVAL_TIME_CLASSES.keys()):
		sorted_scan_intervals_classes[k] = DNS_SCAN_INTERVAL_TIME_CLASSES[k]

	# print(DNS_SCAN_INTERVAL_TIME_CLASSES) 

	OUTPUT_STR += "\n\n"
	OUTPUT_STR += f"DNS_SCAN_INTERVAL_TIME_CLASSES: {DNS_SCAN_INTERVAL_TIME_CLASSES}\n"
	OUTPUT_STR += f"DNS_SCAN_INTERVAL_TIME_CLASSES (sorted): {sorted_scan_intervals_classes}\n"

	# unique_flds = set(TOTAL_FLD_COUNTER.keys()) | set(SSHFP_FLDs.keys())
	OUTPUT_STR += f"processed: {len(PROCESSED_FLDS), sum(PROCESSED_FLDS.values())}\n"

	with open(config.PARSERLOG_ANALYSIS_OUTFILE, "w") as f:
		f.write(OUTPUT_STR)

def serverlog_analysis():
	data = json.load(open(config.SERVER_LOG_STRUCTURED_DATA + "_structued_data.json"))

	#print(data.keys())
	OUTPUT_STR = ""

	counters = {		
		'ERROR_DNS_NO_A_RECORD': Counter(),
		'ERROR_DNS_SERVFAIL': Counter(),
		'ERROR_DNS_TIMEOUT': Counter(),
		'ERROR_DNS_NOT_EXIST': Counter(),
		'ERROR_SERVER_NO_FP': Counter(),
		'ERROR_SERVER_SERVFAIL': Counter(),
		'ERROR_SERVER_NXDOMAIN': Counter(),
		'ERROR_SERVER_WRONGRESPONSE': Counter(),
		'DNSSEC_YES': Counter(),
		'DNSSEC_NO': Counter(),
	}

	PROCESSED_FLDS = Counter()

	for key in counters:
		for entry in data[key]:
			lsplit = entry.split(",")
			tstmp = lsplit[0]
			domain = lsplit[1]

			d = tldextract.extract(domain)
			fld = f"{d.domain}.{d.suffix}"

			counters[key].update([fld])

			PROCESSED_FLDS.update([fld])

		OUTPUT_STR += f"{key} top 10 (unique: {len(counters[key])} / total: {sum(counters[key].values())}): {counters[key].most_common(10)}\n"

	OUTPUT_STR += "\n\n"
	#print(data['BOTH_SSHFP_DATA'][0].keys())

	OUTPUT_STR += f"Total of both-sshfp-data entries: {len(data['BOTH_SSHFP_DATA'])}\n"
	IDENTICAL_DNS_SERVER_RECORDS_COUNTED = Counter()
	domain_counter = Counter()
	for entry in data['BOTH_SSHFP_DATA']:
		domain = entry['domain']
		timestamp = entry['dns']['timestamp']
		is_authentic = entry['is_authentic']
		dns_records = '|'.join(sorted([f"{x['algo']}_{x['type']}_{x['fingerprint']}" for x in entry['dns']['records']]))
		server_records = '|'.join(sorted([f"{x['algo']}_{x['type']}_{x['fingerprint']}_{x['domain']}" for x in entry['server']['records']]))
		
		key = f"{domain},{dns_records},{server_records},{is_authentic}"
		
		domain_counter.update([domain])
		IDENTICAL_DNS_SERVER_RECORDS_COUNTED.update([key])

	OUTPUT_STR += f"DOMAINS unique: {len(domain_counter)} / total: {sum(domain_counter.values())}\n"
	# print("DOMAINS COUNTER: ", len(domain_counter), sum(domain_counter.values()))
	OUTPUT_STR += f"DNS-SERVER-PAIRS (unique: {len(IDENTICAL_DNS_SERVER_RECORDS_COUNTED)}/ total: {sum(IDENTICAL_DNS_SERVER_RECORDS_COUNTED.values())})\n"
	
	OK_DNS_SERVER_PAIRS = dict()
	OK_DNS_SERVER_PAIRS['ok'] = Counter()
	OK_DNS_SERVER_PAIRS['not ok'] = Counter()

	SSHFP_MATCHES = dict()
	SSHFP_MATCH_RATIO = Counter()
	host_counter = 0
	host_sshfps_counter = 0
	host_mapping_sshpfs = 0
	host_mapping_ips = 0

	AUTHENTIC_SSHFPS = set()
	UNAUTHENTIC_SSHFPS = set()

	for entry_id, entry in enumerate(IDENTICAL_DNS_SERVER_RECORDS_COUNTED.keys()):
		# Now we have each interesting case only once.
		domain, dns_records_str, server_records_str, is_authentic = entry.split(",")
		is_authentic = ast.literal_eval(is_authentic) # bool("False") -> True, so take care of that.
		dns_records = set(map(lambda x: x.replace("_",","),dns_records_str.split("|")))
		server_records = set(server_records_str.split("|"))



		d = tldextract.extract(domain)
		fld = f"{d.domain}.{d.suffix}"
		
		host_mapping = dict()
		for srecord in server_records:
			sshfp_algo,sshfp_type,sshfp_fp,ip = srecord.split("_")

			if not ip in host_mapping:
				host_mapping[ip] = set()
			host_mapping[ip].add(f"{sshfp_algo},{sshfp_type},{sshfp_fp}") # Add sshfp to IP

			if is_authentic:
				AUTHENTIC_SSHFPS.add(f"{entry_id},{ip},{sshfp_algo},{sshfp_type},{sshfp_fp}")
			else:
				UNAUTHENTIC_SSHFPS.add(f"{entry_id},{ip},{sshfp_algo},{sshfp_type},{sshfp_fp}")

		
		host_mapping_ips += len(host_mapping)
		host_mapping_sshpfs += sum([ len(host_mapping[ip]) for ip in host_mapping.keys() ]) # Sum of SSHFP counts per IP

		#print("host mapping: ", host_mapping_sshpfs)

		#if domain in SSHFP_MATCHES:
		#	raise Exception(f"Double entry: {domain}")

		SSHFP_MATCHES[str(entry_id)] = dict()
		SSHFP_MATCHES[str(entry_id)]["domain"] = domain
		SSHFP_MATCHES[str(entry_id)]["hosts"] = list()

		for host in host_mapping: # host equals ip
			host_counter += 1
			SSHFP_MATCHES[str(entry_id)]["hosts"].append(host)			
			SSHFP_MATCHES[str(entry_id)][host] = dict()
			SSHFP_MATCHES[str(entry_id)][host]["ok"] = list()
			SSHFP_MATCHES[str(entry_id)][host]["not ok"] = list()
			SSHFP_MATCHES[str(entry_id)][host]["not ok: correct algo AND type, wrong fp"] = list()
			SSHFP_MATCHES[str(entry_id)][host]["not ok: correct fp AND type, wrong algo"] = list()
			SSHFP_MATCHES[str(entry_id)][host]["not ok: correct fp AND algo, wrong type"] = list()
			SSHFP_MATCHES[str(entry_id)][host]["not ok: correct fp, wrong algo OR type"] = list()

			for host_sshfp in host_mapping[host]:
				host_sshfps_counter += 1
				if host_sshfp in dns_records:
					# We got a match!
					SSHFP_MATCHES[str(entry_id)][host]["ok"].append(host_sshfp)
				else:
					# No match	
					SSHFP_MATCHES[str(entry_id)][host]["not ok"].append(host_sshfp)
					
					sshfp_algo,sshfp_type,sshfp_fp = host_sshfp.split(",")
					if any([ f"{sshfp_algo},{sshfp_type}" in record for record in dns_records]):
						# Algo-Type combo exists, but fingerprint is different.
						SSHFP_MATCHES[str(entry_id)][host]["not ok: correct algo AND type, wrong fp"].append(host_sshfp)
					elif any([sshfp_fp in record for record in dns_records]):
						# Fingerprint exists, but algo/type combo is different.
						SSHFP_MATCHES[str(entry_id)][host]["not ok: correct fp, wrong algo OR type"].append(host_sshfp)
						if any([sshfp_type in record and sshfp_fp in record for record in dns_records]):
							# Fingerprint+Type exists, but algo is different.
							SSHFP_MATCHES[str(entry_id)][host]["not ok: correct fp AND type, wrong algo"].append(host_sshfp)
						elif any([sshfp_algo in record and sshfp_fp in record for record in dns_records]):
							# Fingerprint+Algo exists, but type is different.
							SSHFP_MATCHES[str(entry_id)][host]["not ok: correct fp AND algo, wrong type"].append(host_sshfp)
					else:
						# Wrong FP, wrong Algo and Wrong Type 
						#raise Exception(f"SSHFP: {host_sshfp}; Records: {[record for record in dns_records]}")
						pass
			if 	len(SSHFP_MATCHES[str(entry_id)][host]['ok']) > 0:
				OK_DNS_SERVER_PAIRS['ok'].update([fld])

			if 	len(SSHFP_MATCHES[str(entry_id)][host]['not ok']) > 0:
				OK_DNS_SERVER_PAIRS['not ok'].update([fld])

			ratio_ok_keys = len(SSHFP_MATCHES[str(entry_id)][host]["ok"]) / len(host_mapping[host])
			SSHFP_MATCH_RATIO.update([ratio_ok_keys])

	# pyplot.axis("equal")
	# pyplot.title("Match ratio of the DNS and server fingerprints")
	# pyplot.pie([float(v) for v in SSHFP_MATCH_RATIO.values()], labels=[f"{int(round(k,2) * 100)}\%" for k in SSHFP_MATCH_RATIO], autopct=lambda x: f"{round(x,2)}\%",pctdistance=0.8)
	# pyplot.savefig(config.FIGURES_DIR + os.path.sep + "_serverlog_match_ratio.pdf")

	OUTPUT_STR += f"host_mapping SSHFPs: {host_mapping_sshpfs}\n"
	OUTPUT_STR += f"host_mapping IPs: {host_mapping_ips}\n"

	OUTPUT_STR += f"host loop counter: {host_counter}\n"
	OUTPUT_STR += f"host loop sshfps: {host_sshfps_counter}\n"

	num_hosts = 0
	num_domains = 0

	num_ok_sshfps = 0
	num_notok_sshfps = 0
	num_notok_catwfp_sshfps = 0
	num_notok_cfpwat_sshfps = 0
	num_notok_ctfpwa_sshfps = 0
	num_notok_cafpwt_sshfps = 0

	host_instances_ok_sshfps = []
	host_instances_notok_sshfps = []
	host_instances_notok_catwfp_sshfps = []
	host_instances_notok_cfpwat_sshfps = []
	host_instances_notok_ctfpwa_sshfps = []
	host_instances_notok_cafpwt_sshfps = []


	for entry_id in SSHFP_MATCHES.keys():
		for host in SSHFP_MATCHES[entry_id]["hosts"]:
			ok_sshfps = len(SSHFP_MATCHES[entry_id][host]["ok"])
			notok_sshfps = len(SSHFP_MATCHES[entry_id][host]["not ok"])
			notok_catwfp_sshfps = len(SSHFP_MATCHES[entry_id][host]["not ok: correct algo AND type, wrong fp"])
			notok_cfpwat_sshfps = len(SSHFP_MATCHES[entry_id][host]["not ok: correct fp, wrong algo OR type"])
			notok_ctfpwa_sshfps = len(SSHFP_MATCHES[entry_id][host]["not ok: correct fp AND type, wrong algo"])
			notok_cafpwt_sshfps = len(SSHFP_MATCHES[entry_id][host]["not ok: correct fp AND algo, wrong type"])
			
			num_ok_sshfps += ok_sshfps
			num_notok_sshfps += notok_sshfps
			num_notok_catwfp_sshfps += notok_catwfp_sshfps
			num_notok_cfpwat_sshfps += notok_cfpwat_sshfps
			num_notok_ctfpwa_sshfps += notok_ctfpwa_sshfps
			num_notok_cafpwt_sshfps += notok_cafpwt_sshfps


			host_instances_ok_sshfps.append(len(SSHFP_MATCHES[entry_id][host]["ok"]) > 0)
			host_instances_notok_sshfps.append(len(SSHFP_MATCHES[entry_id][host]["not ok"]) > 0)
			host_instances_notok_catwfp_sshfps.append(len(SSHFP_MATCHES[entry_id][host]["not ok: correct algo AND type, wrong fp"]) > 0)
			host_instances_notok_cfpwat_sshfps.append(len(SSHFP_MATCHES[entry_id][host]["not ok: correct fp, wrong algo OR type"]) > 0)
			host_instances_notok_ctfpwa_sshfps.append(len(SSHFP_MATCHES[entry_id][host]["not ok: correct fp AND type, wrong algo"]) > 0)
			host_instances_notok_cafpwt_sshfps.append(len(SSHFP_MATCHES[entry_id][host]["not ok: correct fp AND algo, wrong type"]) > 0)

			# print(domain, host, a,b,c,d)
			num_hosts += 1
		num_domains += 1
	# print(num_domains, num_hosts, num_a)
	# print(host_counter, host_sshfps_counter)	

	OUTPUT_STR += f"Num domains: {num_domains}, Num hosts: {num_hosts}\n"
	OUTPUT_STR += f"SSHFP matches ok: {num_ok_sshfps} / hosts: {sum(host_instances_ok_sshfps)}\n"
	OUTPUT_STR += f"SSHFP matches not ok: {num_notok_sshfps} / hosts: {sum(host_instances_notok_sshfps)}\n"
	OUTPUT_STR += f"SSHFP matches not ok, correct algo AND type, wrong fp: {num_notok_catwfp_sshfps} / hosts: {sum(host_instances_notok_catwfp_sshfps)}\n"
	OUTPUT_STR += f"SSHFP matches not ok, correct fp, wrong algo OR type: {num_notok_cfpwat_sshfps} / hosts: {sum(host_instances_notok_cfpwat_sshfps)}\n"
	OUTPUT_STR += f"-> of that correct fp AND type, wrong algo: {num_notok_ctfpwa_sshfps} / hosts: {sum(host_instances_notok_ctfpwa_sshfps)}\n"
	OUTPUT_STR += f"-> of that correct fp AND algo, wrong type: {num_notok_cafpwt_sshfps} / hosts: {sum(host_instances_notok_cafpwt_sshfps)}\n"
	
	OK_SSHFP_ALGO_COUNTER = Counter()
	OK_SSHFP_TYPE_COUNTER = Counter()
	OK_SSHFP_ALGO_TYPE_PAIRS = Counter()

	NOTOK_SSHFP_ALGO_COUNTER = Counter()
	NOTOK_SSHFP_TYPE_COUNTER = Counter()
	NOTOK_SSHFP_ALGO_TYPE_PAIRS = Counter()

	AUTH_SSHFPS = Counter()
	UNAUTH_SSHFPS = Counter()

	AUTH_SSHFPS_HOSTS = {
		"OK": Counter(),
		"NOT OK": Counter(),
	}
	UNAUTH_SSHFPS_HOSTS = {
		"OK": Counter(),
		"NOT OK": Counter(),
	}
	ok_set = set()
	notok_set = set()

	AUTH_SSHFPS_DOMAINS = {
		"OK": Counter(),
		"NOT OK": Counter(),
	}
	UNAUTH_SSHFPS_DOMAINS = {
		"OK": Counter(),
		"NOT OK": Counter(),
	}

	MATCHING_HOSTS = {
		"secure": Counter(),
		'insecure': Counter(),
		'nomatch': Counter()
	}
	MATCHING_DOMAINS = {
		"secure": Counter(),
		'insecure': Counter(),
		'nomatch': Counter()
	}

	only_first_domain_measurement = True
	first_domains = set()


	for entry_id in SSHFP_MATCHES.keys():
		domain = SSHFP_MATCHES[entry_id]['domain']

		if only_first_domain_measurement and domain in first_domains:
			continue
		else:
			first_domains.add(domain)

		domain_has_matching_secure_record = False
		domain_has_matching_insecure_record = False
		for host in SSHFP_MATCHES[entry_id]["hosts"]:
			host_has_matching_secure_record = False
			host_has_matching_insecure_record = False

			for ok_sshfp in SSHFP_MATCHES[entry_id][host]["ok"]:
				sshfp_split = ok_sshfp.split(",")
				sshfp_algo = sshfp_split[0]
				sshfp_type = sshfp_split[1]
				sshfp_fp = sshfp_split[2]

				#if ok_sshfp not in ok_set:
				OK_SSHFP_ALGO_COUNTER.update([sshfp_algo])
				OK_SSHFP_TYPE_COUNTER.update([sshfp_type]) 
				OK_SSHFP_ALGO_TYPE_PAIRS.update([f"{sshfp_algo},{sshfp_type}"])
				ok_set.add(ok_sshfp)

				key = f"{entry_id},{host},{sshfp_algo},{sshfp_type},{sshfp_fp}"
				if key in AUTHENTIC_SSHFPS:
					AUTH_SSHFPS.update(["OK"])
					host_has_matching_secure_record = True
					#AUTH_SSHFPS_HOSTS["OK"].update([host])
					#AUTH_SSHFPS_DOMAINS["OK"].update([domain])
				elif key in UNAUTHENTIC_SSHFPS:
					UNAUTH_SSHFPS.update(["OK"])
					host_has_matching_insecure_record = True
					#UNAUTH_SSHFPS_HOSTS["OK"].update([host])
					#UNAUTH_SSHFPS_DOMAINS["OK"].update([domain])
				else:
					raise Exception(f"Should never happen: {key}")


			for notok_sshfp in SSHFP_MATCHES[entry_id][host]["not ok"]:
				sshfp_split = notok_sshfp.split(",")
				sshfp_algo = sshfp_split[0]
				sshfp_type = sshfp_split[1]
				sshfp_fp = sshfp_split[2]

				#if notok_sshfp not in notok_set:
				NOTOK_SSHFP_ALGO_COUNTER.update([sshfp_algo])
				NOTOK_SSHFP_TYPE_COUNTER.update([sshfp_type]) 
				NOTOK_SSHFP_ALGO_TYPE_PAIRS.update([f"{sshfp_algo},{sshfp_type}"])
				notok_set.add(notok_sshfp)

				key = f"{entry_id},{host},{sshfp_algo},{sshfp_type},{sshfp_fp}"
				if key in AUTHENTIC_SSHFPS:
					AUTH_SSHFPS.update(["NOT OK"])
					#AUTH_SSHFPS_HOSTS["NOT OK"].update([host])
					#AUTH_SSHFPS_DOMAINS["NOT OK"].update([domain])
				elif key in UNAUTHENTIC_SSHFPS:
					UNAUTH_SSHFPS.update(["NOT OK"])
					#UNAUTH_SSHFPS_HOSTS["NOT OK"].update([host])
					#UNAUTH_SSHFPS_DOMAINS["NOT OK"].update([domain])
				else:
					#pass
					# This can indeed happen, i.e. when the server's host key is not 
					raise Exception(f"Should never happen: {key}")

			if host_has_matching_secure_record:
				MATCHING_HOSTS["secure"].update([host])
				domain_has_matching_secure_record = True


			elif host_has_matching_insecure_record:
				MATCHING_HOSTS["insecure"].update([host])
				domain_has_matching_insecure_record = True

			elif not host_has_matching_secure_record and not host_has_matching_insecure_record:
				MATCHING_HOSTS['nomatch'].update([host])
			else:
				raise Exception("Should never happen.")

		if domain_has_matching_secure_record:
			MATCHING_DOMAINS["secure"].update([domain])
		elif domain_has_matching_insecure_record:
			MATCHING_DOMAINS["insecure"].update([domain])
		elif not domain_has_matching_secure_record and not domain_has_matching_insecure_record:
			MATCHING_DOMAINS['nomatch'].update([domain])
		else:
			raise Exception("Should never happen.")

	total_hosts = MATCHING_HOSTS['secure']+MATCHING_HOSTS['insecure']+MATCHING_HOSTS['nomatch']
	total_domains = MATCHING_DOMAINS['secure']+MATCHING_DOMAINS['insecure']+MATCHING_DOMAINS['nomatch']

	OUTPUT_STR += "\n\n"
	OUTPUT_STR += f"#### ONLY FIRST DOMAIN MEASUREMENT: {only_first_domain_measurement}\n"
	OUTPUT_STR += f"OK SSHFP ALGOs (total: {sum(OK_SSHFP_ALGO_COUNTER.values())}): {OK_SSHFP_ALGO_COUNTER}\n"
	OUTPUT_STR += f"OK SSHFP TYPEs (total: {sum(OK_SSHFP_TYPE_COUNTER.values())}): {OK_SSHFP_TYPE_COUNTER}\n"
	OUTPUT_STR += f"OK SSHFP ALGO/TYPE Pairs (total: {sum(OK_SSHFP_ALGO_TYPE_PAIRS.values())}): {OK_SSHFP_ALGO_TYPE_PAIRS}\n"

	OUTPUT_STR += f"NOT OK SSHFP ALGOs (total: {sum(NOTOK_SSHFP_ALGO_COUNTER.values())}): {NOTOK_SSHFP_ALGO_COUNTER}\n"
	OUTPUT_STR += f"NOT OK SSHFP TYPEs (total: {sum(NOTOK_SSHFP_TYPE_COUNTER.values())}): {NOTOK_SSHFP_TYPE_COUNTER}\n"
	OUTPUT_STR += f"NOT OK SSHFP ALGO/TYPE Pairs (total: {sum(NOTOK_SSHFP_ALGO_TYPE_PAIRS.values())}): {NOTOK_SSHFP_ALGO_TYPE_PAIRS}\n"

	OUTPUT_STR += "\n\n"
	OUTPUT_STR += f"AUTHENTIC SSHFPS records (total: {sum(AUTH_SSHFPS.values())}): {AUTH_SSHFPS}\n"
	OUTPUT_STR += f"UNAUTHENTIC SSHFPS records (total: {sum(UNAUTH_SSHFPS.values())}): {UNAUTH_SSHFPS}\n"
	OUTPUT_STR += f"\n"

	OUTPUT_STR += f"Matching hosts - secure: (unique: {len(MATCHING_HOSTS['secure'])}/ total: {sum(MATCHING_HOSTS['secure'].values())}): {MATCHING_HOSTS['secure'].most_common(10)}\n"
	OUTPUT_STR += f"Matching hosts - insecure: (unique: {len(MATCHING_HOSTS['insecure'])}/ total: {sum(MATCHING_HOSTS['insecure'].values())}): {MATCHING_HOSTS['insecure'].most_common(10)}\n"
	OUTPUT_STR += f"Matching hosts - nomatch: (unique: {len(MATCHING_HOSTS['nomatch'])}/ total: {sum(MATCHING_HOSTS['nomatch'].values())}): {MATCHING_HOSTS['nomatch'].most_common(10)}\n"
	OUTPUT_STR += f"Total unique: {len(total_hosts)}, total: {sum(total_hosts.values())}"
	OUTPUT_STR += f"\n\n"
	OUTPUT_STR += f"Matching domain - secure: (unique: {len(MATCHING_DOMAINS['secure'])}/ total: {sum(MATCHING_DOMAINS['secure'].values())}): {MATCHING_DOMAINS['secure'].most_common(10)}\n"
	OUTPUT_STR += f"Matching domain - insecure: (unique: {len(MATCHING_DOMAINS['insecure'])}/ total: {sum(MATCHING_DOMAINS['insecure'].values())}): {MATCHING_DOMAINS['insecure'].most_common(10)}\n"
	OUTPUT_STR += f"Matching domain - nomatch: (unique: {len(MATCHING_DOMAINS['nomatch'])}/ total: {sum(MATCHING_DOMAINS['nomatch'].values())}): {MATCHING_DOMAINS['nomatch'].most_common(10)}\n"
	OUTPUT_STR += f"Total unique: {len(total_domains)}, total: {sum(total_domains.values())}"
	OUTPUT_STR += f"\n\n"
	# OUTPUT_STR += f"OK AUTHENTIC HOSTS (unique: {len(AUTH_SSHFPS_HOSTS['OK'])}/ total: {sum(AUTH_SSHFPS_HOSTS['OK'].values())}): {AUTH_SSHFPS_HOSTS['OK'].most_common(10)}\n"
	# OUTPUT_STR += f"OK UNAUTHENTIC HOSTS (unique: {len(UNAUTH_SSHFPS_HOSTS['OK'])}/ total: {sum(UNAUTH_SSHFPS_HOSTS['OK'].values())}): {UNAUTH_SSHFPS_HOSTS['OK'].most_common(10)}\n"
	# OUTPUT_STR += f"NOT OK AUTHENTIC HOSTS (unique: {len(AUTH_SSHFPS_HOSTS['NOT OK'])}/ total: {sum(AUTH_SSHFPS_HOSTS['NOT OK'].values())}): {AUTH_SSHFPS_HOSTS['NOT OK'].most_common(10)}\n"
	# OUTPUT_STR += f"NOT OK UNAUTHENTIC HOSTS (unique: {len(UNAUTH_SSHFPS_HOSTS['NOT OK'])}/ total: {sum(UNAUTH_SSHFPS_HOSTS['NOT OK'].values())}): {UNAUTH_SSHFPS_HOSTS['NOT OK'].most_common(10)}\n"
	# OUTPUT_STR += f"\n"
	# OUTPUT_STR += f"OK AUTHENTIC DOMAINS (unique: {len(AUTH_SSHFPS_DOMAINS['OK'])}/ total: {sum(AUTH_SSHFPS_DOMAINS['OK'].values())}): {AUTH_SSHFPS_DOMAINS['OK'].most_common(10)}\n"
	# OUTPUT_STR += f"OK UNAUTHENTIC DOMAINS (unique: {len(UNAUTH_SSHFPS_DOMAINS['OK'])}/ total: {sum(UNAUTH_SSHFPS_DOMAINS['OK'].values())}): {UNAUTH_SSHFPS_DOMAINS['OK'].most_common(10)}\n"
	# OUTPUT_STR += f"NOT OK AUTHENTIC DOMAINS (unique: {len(AUTH_SSHFPS_DOMAINS['NOT OK'])}/ total: {sum(AUTH_SSHFPS_DOMAINS['NOT OK'].values())}): {AUTH_SSHFPS_DOMAINS['NOT OK'].most_common(10)}\n"
	# OUTPUT_STR += f"NOT OK UNAUTHENTIC DOMAINS (unique: {len(UNAUTH_SSHFPS_DOMAINS['NOT OK'])}/ total: {sum(UNAUTH_SSHFPS_DOMAINS['NOT OK'].values())}): {UNAUTH_SSHFPS_DOMAINS['NOT OK'].most_common(10)}\n"
	# OUTPUT_STR += "\n\n"
	#OUTPUT_STR += f"a: {num_a}, b: {num_b}, c: {num_c}, d: {num_d}\n"

	# host_ok = [ len(SSHFP_MATCHES[entry_id][host]["ok"])  for entry_id in SSHFP_MATCHES.keys() for host in SSHFP_MATCHES[entry_id]["hosts"] ]
	# host_notok = [ len(SSHFP_MATCHES[entry_id][host]["not ok"])  for entry_id in SSHFP_MATCHES.keys() for host in SSHFP_MATCHES[entry_id]["hosts"] ]
	# host_notok_catwfp = [ len(SSHFP_MATCHES[entry_id][host]["not ok: correct algo AND type, wrong fp"])  for entry_id in SSHFP_MATCHES.keys() for host in SSHFP_MATCHES[entry_id]["hosts"] ]
	# host_notok_cfpwat = [ len(SSHFP_MATCHES[entry_id][host]["not ok: correct fp, wrong algo OR type"])  for entry_id in SSHFP_MATCHES.keys() for host in SSHFP_MATCHES[entry_id]["hosts"] ]

	# OUTPUT_STR += f"a: {sum(host_ok)}, b: {sum(host_notok)}, c: {sum(host_notok_catwfp)}, d: {sum(host_notok_cfpwat)}\n"
	# 
	# print(len(host_ok), sum(host_ok), len(host_ok) - sum(host_ok))
	# print(len(host_notok), sum(host_notok))
	# print(len(host_notok_catwfp), sum(host_notok_catwfp))
	# print(len(host_notok_cfpwat), sum(host_notok_cfpwat))

	
	OUTPUT_STR += f"DNS SERVER PAIRS (FLDs) DNS-Check: OK (unique: {len(OK_DNS_SERVER_PAIRS['ok'])} / total: {sum(OK_DNS_SERVER_PAIRS['ok'].values())}), NOT OK (unique: {len(OK_DNS_SERVER_PAIRS['not ok'])}, total: {sum(OK_DNS_SERVER_PAIRS['not ok'].values())})\n"
	# OUTPUT_STR += f"SSHFP matches ok: {len(SSHFP_MATCHES[domain][host]['ok'])}\n"
	# OUTPUT_STR += f"SSHFP matches not ok: {len(SSHFP_MATCHES[domain][host]['not ok'])}\n"
	# OUTPUT_STR += f"SSHFP matches not ok, correct algo/type, wrong fp: {len(SSHFP_MATCHES[domain][host]["not ok: correct algo AND type, wrong fp"])}\n"
	# OUTPUT_STR += f"SSHFP matches not ok, correct fp, wrong algo/type: {len(SSHFP_MATCHES[domain][host]["not ok: correct fp, wrong algo OR type"])}\n"
	
	OUTPUT_STR += f"\n\n"
	OUTPUT_STR += f"SSHFP Match Ratio (host-basis): total: {sum(SSHFP_MATCH_RATIO.values())}, {SSHFP_MATCH_RATIO}\n"
	#print(OK_DNS_SERVER_PAIRS['ok'])
#	print(interesting.most_common(10))
#	print(domains.most_common(10))
	OUTPUT_STR += f"PROCESSED_FLDS: {len(PROCESSED_FLDS)}, {sum(PROCESSED_FLDS.values())}\n"
	
	with open(config.SERVERLOG_ANALYSIS_OUTFILE, "w") as f:
		f.write(OUTPUT_STR)

def serverlog_ptr_analysis(mode=0):

	OUTPUT_STR = ""
	if mode <= 0:
		raise Exception("Wrong mode")

	# Scan PTR records
	elif mode == 1:
		import dns.resolver, dns.reversename
		data = json.load(open(config.SERVER_LOG_STRUCTURED_DATA + "_structued_data.json"))

		#print(data.keys())

		host_ips = set()

		host_ips.update([ x['domain'] for entry in data['BOTH_SSHFP_DATA'] for x in entry['server']['records'] ])


		host_ptr_mapping = {}

		for host_ip in host_ips:
			try:		
				qname = dns.reversename.from_address(host_ip)
				answer = dns.resolver.resolve(qname, 'ptr')
				records = [ptr.to_text() for ptr in answer]
				
				ptr = records[0]

				answer = dns.resolver.resolve(ptr, 'A')
				records = [a.to_text() for a in answer]

				if host_ip not in records:
					raise Exception(f"IP {host_ip} not found in {records} for {ptr}.")

				host_ptr_mapping[host_ip] = {
					'ptr': ptr,
					'A': records,
				}
			except Exception as e:
				host_ptr_mapping[host_ip] = {
					"error": f"ERROR: {e}"
				}
			print(qname, host_ptr_mapping[host_ip])
			time.sleep(1. / 100) # max 100 queries per second

		with open(config.SERVERLOG_ANALYSIS_PTR_MAPPING, "w") as f:
			f.write(json.dumps(host_ptr_mapping))

	elif mode == 2:
		data = json.load(open(config.SERVER_LOG_STRUCTURED_DATA + "_structued_data.json"))
		host_ptr_mapping =  json.load(open(config.SERVERLOG_ANALYSIS_PTR_MAPPING))

		ptrs = set()
		err_counter = 0
		for ip, ptr in host_ptr_mapping.items():
			if 'error' in ptr.keys():
				err_counter += 1
				continue
			ptrs.add(ptr['ptr'].rstrip("."))


		OUTPUT_STR += f"Total Errors querying PTR/A records: {err_counter}\n"
		OUTPUT_STR += f"Total of IPs in PTR Mapping {len(host_ptr_mapping)}, unique PTR names: {len(ptrs)}\n"

		first_match = set()
		num_ptr_matches = 0
		num_skipped_no_ptr = 0
		num_skipped_no_match = 0
		num_has_match = 0
		dnssec_ok = 0
		dnssec_notok = 0
		for entry in data['BOTH_SSHFP_DATA']:
			domain = entry['domain']

			# TODO: Maybe remove?
			if domain in first_match:
				continue
			else:
				first_match.add(domain)

			# Skip domains that we do not have a PTR record for.
			if not domain in ptrs:
				num_skipped_no_ptr += 1
				continue

			num_ptr_matches += 1

			host_ips = [ x['domain'] for x in entry['server']['records'] ]
			if not all([ ip in host_ptr_mapping.keys() for ip in host_ips]):
				raise Exception(f"Not all IPs in host_ptr_mapping for {domain}")


			dns_sshfp = set([f"{x['algo']}_{x['type']}_{x['fingerprint']}" for x in entry['dns']['records']])
			server_sshfp = set([f"{x['algo']}_{x['type']}_{x['fingerprint']}" for x in entry['server']['records']])

			intersection = dns_sshfp & server_sshfp
			if not intersection:
				num_skipped_no_match += 1
				continue

			num_has_match += 1

			is_authentic = entry['is_authentic']

			if is_authentic:
				dnssec_ok += 1
			else:
				dnssec_notok += 1

		OUTPUT_STR += "\n\n"
		OUTPUT_STR += f"Num skipped no PTR: {num_skipped_no_ptr}\n"
		OUTPUT_STR += f"Num PTR matches: {num_ptr_matches}\n"
		OUTPUT_STR += f"Num skipped no SSHFP match: {num_skipped_no_match}\n"
		OUTPUT_STR += f"Num has match: {num_has_match}\n"
		OUTPUT_STR += f"Domains with DNSSEC OK: {dnssec_ok}\n"
		OUTPUT_STR += f"Domains with DNSSEC NOT OK: {dnssec_notok}\n"


		with open(config.SERVERLOG_ANALYSIS_PTR_OUT, "w") as f:
			f.write(OUTPUT_STR)

def parserlog_domain_v6_analysis(mode=0):
	OUTPUT_STR = ""
	if mode == 0 or mode > 2:
		raise Exception("Wrong mode")
	elif mode == 1:
		import dns.resolver
		data = json.load(open(config.PARSER_LOG_STRUCTED_DATA + "_structued_data.json"))
		domains = set()
		domains.update(data['STRUCTURED_DOMAINS'].keys())

		domain_record_mapping = {}
		for domain in domains:
			try:
				answer = dns.resolver.resolve(domain, 'AAAA')
				records = [aaaa.to_text() for aaaa in answer]

				if records:
					has_v6 = True
				else:
					has_v6 = False
				
				domain_record_mapping[domain] = {
					'v6_records': records,
					'has_v6': has_v6,
				}
				
			except Exception as e:
				domain_record_mapping[domain] = {
					"v6_error": f"ERROR: {e}",
					'has_v6': False
				}

			try:
				answer = dns.resolver.resolve(domain, 'A')
				records = [a.to_text() for a in answer]

				if records:
					has_v4 = True
				else:
					has_v4 = False
				
				domain_record_mapping[domain].update({
					'v4_records': records,
					'has_v4': has_v4,
				})
				
			except Exception as e:
				domain_record_mapping[domain].update({
					"v4_error": f"ERROR: {e}",
					'has_v4': False
				})
			print(domain, domain_record_mapping[domain])
			time.sleep(1. / 100) # max 100 queries per second

		with open(config.PARSERLOG_ANALYSIS_V6, "w") as f:
			f.write(json.dumps(domain_record_mapping))
		pass
	elif mode == 2:
		data = json.load(open(config.PARSERLOG_ANALYSIS_V6))

		num_only_v6 = 0
		num_only_v4 = 0
		num_both = 0
		num_nothing = 0

		for domain in data.keys():
			has_v6 = data[domain]['has_v6']
			has_v4 = data[domain]['has_v4']

			if has_v4 and has_v6:
				num_both += 1
			elif has_v4 and not has_v6:
				num_only_v4 += 1
			elif not has_v4 and has_v6:
				num_only_v6 += 1
			elif not has_v4 and not has_v4:
				num_nothing += 1
			else:
				raise Exception("Should never happen.")
		
		OUTPUT_STR += f"Total domains: {len(data.keys())}\n"
		OUTPUT_STR += f"Has v4 AND v6: {num_both}\n"
		OUTPUT_STR += f"Has only v4: {num_only_v4}\n"
		OUTPUT_STR += f"Has only v6: {num_only_v6}\n"
		OUTPUT_STR += f"Has nothing: {num_nothing}\n"
		
		with open(config.PARSERLOG_ANALYSIS_V6_OUT, "w") as f:
			f.write(OUTPUT_STR)