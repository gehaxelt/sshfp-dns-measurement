import gzip
import json
from collections import Counter


from config import config
import utils

def domainfile_log_to_unique_domainlist_with_count():
	UNIQUE_DOMAINS = Counter()
	OTHERLINES = Counter()
	with gzip.open(config.DOMAINFILE_LOG_GZ) as f:
		for line in f:
			line = line.decode().strip()
			if 'Queueing domain' in line:
				domain = utils.cut_left(line, "Queueing domain ")
				UNIQUE_DOMAINS.update([domain])
			elif 'Reading from file' in line:
				OTHERLINES.update([line])
			else:
				raise Exception(f"Unknown line: {line}")

	data_out = {
		'counted_unique_domains_len': len(UNIQUE_DOMAINS),
		'counted_otherlines_len': len(OTHERLINES),
		'counted_unique_domains': UNIQUE_DOMAINS,
		'counted_otherlines': OTHERLINES,
	}
	with open(config.DOMAINFILE_COUNTED_UNIQUE_DOMAINS + ".json", "w") as f:
		f.write(json.dumps(data_out))

	with open(config.DOMAINFILE_COUNTED_UNIQUE_DOMAINS + "_unique_domains.csv", "w") as f:
		f.write("Count,UniqueDomain\n")
		for l in UNIQUE_DOMAINS:
			f.write(f"{UNIQUE_DOMAINS[l]},\"{l}\"\n")

def cerstream_log_to_unique_domainlist_with_count():
	UNIQUE_DOMAINS = Counter()
	SKIPPED_DOMAINS = Counter()
	OTHERLINES = Counter()
	with gzip.open(config.CERTSTREAM_LOG_GZ) as f:
		for line in f:
			line = line.decode().strip()
			if 'Skipping Wildcard' in line:
				domain = utils.cut_left(line, "Skipping Wildcard domain: ")
				SKIPPED_DOMAINS.update([domain])
			elif 'Queueing domain' in line:
				domain = utils.cut_left(line, "Queueing domain ")
				UNIQUE_DOMAINS.update([domain])
			elif 'Connection established' in line:
				OTHERLINES.update([line])
			elif 'Error connecting to CertStream' in line:
				OTHERLINES.update([line])
			else:
				raise Exception(f"Unknown line: {line}")

	data_out = {
		'counted_unique_domains_len': len(UNIQUE_DOMAINS),
		'counted_skipped_domains_len': len(SKIPPED_DOMAINS),
		'counted_otherlines_len': len(OTHERLINES),
		'counted_unique_domains': UNIQUE_DOMAINS,
		'counted_skipped_domains': SKIPPED_DOMAINS,
		'counted_otherlines': OTHERLINES,
	}
	with open(config.CERTSTREAM_COUNTED_UNIQUE_DOMAINS + ".json", "w") as f:
		f.write(json.dumps(data_out))

	with open(config.CERTSTREAM_COUNTED_UNIQUE_DOMAINS + "_unique_domains.csv", "w") as f:
		f.write("Count,UniqueDomain\n")
		for l in UNIQUE_DOMAINS:
			f.write(f"{UNIQUE_DOMAINS[l]},\"{l}\"\n")

	with open(config.CERTSTREAM_COUNTED_UNIQUE_DOMAINS + "_skipped_domains.csv", "w") as f:
		f.write("Count,SkippedDomain\n")
		for l in SKIPPED_DOMAINS:
			f.write(f"{SKIPPED_DOMAINS[l]},\"{l}\"\n")

	with open(config.CERTSTREAM_COUNTED_UNIQUE_DOMAINS + "_otherlines.csv", "w") as f:
		f.write("Count,Line\n")
		for l in OTHERLINES:
			f.write(f"{OTHERLINES[l]},\"{l}\"\n")


def querylog_to_counted_messages():
	DNS_ERR_NO_SSHFP = Counter()
	DNS_ERR_NO_ANSWER = Counter()
	DNS_ERR_NO_QUERYNAME = Counter()
	DNS_ERR_TIMEOUT = Counter()
	DNS_ERR_LABEL = Counter()
	FOUND_RRs = Counter()

	with gzip.open(config.QUERY_LOG_GZ) as f:
		for line in f:
			line = line.decode().strip()
			if 'The DNS response does not contain an answer to the question' in line:
				domain = utils.cut_right(utils.cut_left(line, "Exception for "), " -> ")
				DNS_ERR_NO_SSHFP.update([domain])
			elif 'All nameservers failed to answer the query' in line:
				domain = utils.cut_right(utils.cut_left(line, "Exception for "), " -> ")
				DNS_ERR_NO_ANSWER.update([domain])
			elif 'The DNS query name does not exist' in line:
				domain = utils.cut_right(utils.cut_left(line, "Exception for "), " -> ")
				DNS_ERR_NO_QUERYNAME.update([domain])
			elif 'The DNS operation timed out after' in line:
				domain = utils.cut_right(utils.cut_left(line, "Exception for "), " -> ")
				DNS_ERR_TIMEOUT.update([domain])
			elif 'A DNS label is > 63 octets long' in line:
				domain = utils.cut_right(utils.cut_left(line, "Exception for "), " -> ")
				DNS_ERR_LABEL.update([domain])
			elif 'Found SSHFP RRs' in line:
				domain = utils.cut_right(utils.cut_left(line, "Found SSHFP RRs: "), " => ")
				FOUND_RRs.update([domain])
			else:
				raise Exception(f"Unknown line: {line}")

	data_out = {
		'counted_dns_err_no_sshfp_len': len(DNS_ERR_NO_SSHFP),
		'counted_dns_err_no_answer_len': len(DNS_ERR_NO_ANSWER),
		'counted_dns_err_no_queryname_len': len(DNS_ERR_NO_QUERYNAME),
		'counted_dns_err_timeout_len': len(DNS_ERR_TIMEOUT),
		'counted_dns_err_label_len': len(DNS_ERR_LABEL),
		'counted_dns_found_sshfp_len': len(FOUND_RRs),

		'counted_dns_err_no_sshfp': DNS_ERR_NO_SSHFP,
		'counted_dns_err_no_answer': DNS_ERR_NO_ANSWER,
		'counted_dns_err_no_queryname': DNS_ERR_NO_QUERYNAME,
		'counted_dns_err_timeout': DNS_ERR_TIMEOUT,
		'counted_dns_err_label': DNS_ERR_LABEL,
		'counted_dns_found_sshfp': FOUND_RRs,
	}

	with open(config.QUERY_LOG_COUNTED_MESSAGES + ".json", "w") as f:
		f.write(json.dumps(data_out))

	with open(config.QUERY_LOG_COUNTED_MESSAGES + "_err_no_sshfp.csv", "w") as f:
		f.write("Count,DomainWithErrNoSSHFP\n")
		for l in DNS_ERR_NO_SSHFP:
			f.write(f"{DNS_ERR_NO_SSHFP[l]},\"{l}\"\n")

	with open(config.QUERY_LOG_COUNTED_MESSAGES + "_err_no_answer.csv", "w") as f:
		f.write("Count,DomainWithErrNoAnswer\n")
		for l in DNS_ERR_NO_ANSWER:
			f.write(f"{DNS_ERR_NO_ANSWER[l]},\"{l}\"\n")

	with open(config.QUERY_LOG_COUNTED_MESSAGES + "_err_no_queryname.csv", "w") as f:
		f.write("Count,DomainWithErrNoQueryname\n")
		for l in DNS_ERR_NO_QUERYNAME:
			f.write(f"{DNS_ERR_NO_QUERYNAME[l]},\"{l}\"\n")

	with open(config.QUERY_LOG_COUNTED_MESSAGES + "_err_timeout.csv", "w") as f:
		f.write("Count,DomainWithErrNoTimeout\n")
		for l in DNS_ERR_TIMEOUT:
			f.write(f"{DNS_ERR_TIMEOUT[l]},\"{l}\"\n")

	with open(config.QUERY_LOG_COUNTED_MESSAGES + "_err_label.csv", "w") as f:
		f.write("Count,DomainWithErrNoLabel\n")
		for l in DNS_ERR_LABEL:
			f.write(f"{DNS_ERR_LABEL[l]},\"{l}\"\n")

	with open(config.QUERY_LOG_COUNTED_MESSAGES + "_found_sshfp.csv", "w") as f:
		f.write("Count,DomainWithSSHFP\n")
		for l in FOUND_RRs:
			f.write(f"{FOUND_RRs[l]},\"{l}\"\n")

def parserlog_to_structured_data():
	STRUCTURED_DOMAINS = dict()
	TIMESORTED_LIST = dict()

	PARSER_ERR_NO_MATCH = list()
	PARSER_ERR_WRONG_FP = list()

	with gzip.open(config.PARSER_LOG_GZ) as f:
		for line in f:
			line = line.decode().strip()

			if 'An error' in line:
				msg = utils.cut_left(line, "An error occured: ")
				json_data = json.loads(utils.cut_right(msg, " -> ").replace("'", '"'))
				error = utils.cut_left(msg, " -> ")
				domain = json_data['domain']
				tstmp = json_data['timestamp']

				if 'No match found' in line:
					error = error.replace("No match found in ", "")
					error_line = f"{tstmp},{domain},No match found,\"{error}\""
					PARSER_ERR_NO_MATCH.append(error_line)
				elif 'Wrong fingerprint' in line:
					error = error.replace("Wrong fingerprint ", "")
					error_line = f"{tstmp},{domain},Wrong fingerprint,\"{error}\""	
					PARSER_ERR_WRONG_FP.append(error_line)
				else:
					raise Exception(f"Error found in line: {line}")
				continue

			# tstmp, domain, type, algo, hash
			lsplit = line.split(",")
			tstmp = lsplit[0]
			domain = lsplit[1]

			tsorted_key = f"{tstmp},{domain}"
			if not tsorted_key in TIMESORTED_LIST:
				TIMESORTED_LIST[tsorted_key] = []
			TIMESORTED_LIST[tsorted_key].append(','.join(lsplit[2:]))

			if not domain in STRUCTURED_DOMAINS:
				STRUCTURED_DOMAINS[domain] = {}
			if not tstmp in STRUCTURED_DOMAINS[domain]:
				STRUCTURED_DOMAINS[domain][tstmp] = []
			STRUCTURED_DOMAINS[domain][tstmp].append(','.join(lsplit[2:]))

	data_output = {
		'STRUCTURED_DOMAINS_len': len(STRUCTURED_DOMAINS),
		'TIMESORTED_LIST_len': len(TIMESORTED_LIST),
		'PARSER_ERR_NO_MATCH_len': len(PARSER_ERR_NO_MATCH),
		'PARSER_ERR_WRONG_FP_len': len(PARSER_ERR_WRONG_FP),

		'STRUCTURED_DOMAINS': STRUCTURED_DOMAINS,
		'TIMESORTED_LIST': TIMESORTED_LIST,
		'PARSER_ERR_NO_MATCH': PARSER_ERR_NO_MATCH,
		'PARSER_ERR_WRONG_FP': PARSER_ERR_WRONG_FP,
	}

	with open(config.PARSER_LOG_STRUCTED_DATA + "_structued_data.json", "w") as f:
		f.write(json.dumps(data_output))

	with open(config.PARSER_LOG_STRUCTED_DATA + "_timesorted_sshpfs.csv", "w") as f:
		f.write("Timestamp,Domain,SSHFPs\n")
		for k in TIMESORTED_LIST.keys():
			sshpfs = "|".join(TIMESORTED_LIST[k])
			f.write(f"{k},\"{sshpfs}\"\n")

	with open(config.PARSER_LOG_STRUCTED_DATA + "_errors.csv", "w") as f:
		f.write("Timestamp,Domain,ErrorType,ErrorMessage\n")
		for k in PARSER_ERR_NO_MATCH:
			f.write(f"{k}\n")
		for k in PARSER_ERR_WRONG_FP:
			f.write(f"{k}\n")


def server_to_structured_data():
	ERROR_DNS_NO_A_RECORD = list()
	ERROR_DNS_SERVFAIL = list()
	ERROR_DNS_TIMEOUT = list()
	ERROR_DNS_NOT_EXIST = list()
	ERROR_SERVER_NO_FP = list()
	ERROR_SERVER_SERVFAIL = list()
	ERROR_SERVER_NXDOMAIN = list()
	ERROR_SERVER_WRONGRESPONSE = list()

	DNSSEC_YES = list()
	DNSSEC_NO = list()
	BOTH_SSHFP_DATA = list()

	with gzip.open(config.SERVER_LOG_GZ) as f:
		for line in f:
			line = line.decode().strip()
			jsond = json.loads(line)

			domain = jsond['domain']
			tstmp = jsond["dns"]['timestamp']

			key = f"{tstmp},{domain}"
			if not jsond['server']:
				for e in jsond['errors']:
					if 'The DNS response does not contain an answer to' in e and 'IN A' in e:
						ERROR_DNS_NO_A_RECORD.append(key)
					elif 'All nameservers failed to answer the query' in e and 'SERVFAIL' in e:
						ERROR_DNS_SERVFAIL.append(key)
					elif 'The DNS operation timed out after' in e:
						ERROR_DNS_TIMEOUT.append(key)
					elif 'The DNS query name does not exist' in e:
						ERROR_DNS_NOT_EXIST.append(key)
					else:
						raise Exception(f"Unknown error: {e}")
				continue

			if not jsond['server']['records']:
				for e in jsond['errors']:
					if 'SSH-Keyscan returned no fingerprints' in e:
						ERROR_SERVER_NO_FP.append(key)
					elif 'SERVFAIL' in e:
						ERROR_SERVER_SERVFAIL.append(key)
					elif 'NXDOMAIN' in e:
						ERROR_SERVER_NXDOMAIN.append(key)
					elif 'got a response from' in e:
						ERROR_SERVER_WRONGRESPONSE.append(key)
					else:
						raise Exception(f"Unknown error: {e}")
				continue

			if jsond['is_authentic']:
				DNSSEC_YES.append(key)
			else:
				DNSSEC_NO.append(key)

			BOTH_SSHFP_DATA.append(jsond)

	data_output = {
		'ERROR_DNS_NO_A_RECORD_len': len(ERROR_DNS_NO_A_RECORD),
		'ERROR_DNS_SERVFAIL_len': len(ERROR_DNS_SERVFAIL),
		'ERROR_DNS_TIMEOUT_len': len(ERROR_DNS_TIMEOUT),
		'ERROR_DNS_NOT_EXIST_len': len(ERROR_DNS_NOT_EXIST),
		'ERROR_SERVER_NO_FP_len': len(ERROR_SERVER_NO_FP),
		'ERROR_SERVER_SERVFAIL_len': len(ERROR_SERVER_SERVFAIL),
		'ERROR_SERVER_NXDOMAIN_len': len(ERROR_SERVER_NXDOMAIN),
		'ERROR_SERVER_WRONGRESPONSE_len': len(ERROR_SERVER_WRONGRESPONSE),
		'DNSSEC_YES_len': len(DNSSEC_YES),
		'DNSSEC_NO_len': len(DNSSEC_NO),

		'ERROR_DNS_NO_A_RECORD': ERROR_DNS_NO_A_RECORD,
		'ERROR_DNS_SERVFAIL': ERROR_DNS_SERVFAIL,
		'ERROR_DNS_TIMEOUT': ERROR_DNS_TIMEOUT,
		'ERROR_DNS_NOT_EXIST': ERROR_DNS_NOT_EXIST,
		'ERROR_SERVER_NO_FP': ERROR_SERVER_NO_FP,
		'ERROR_SERVER_SERVFAIL': ERROR_SERVER_SERVFAIL,
		'ERROR_SERVER_NXDOMAIN': ERROR_SERVER_NXDOMAIN,
		'ERROR_SERVER_WRONGRESPONSE': ERROR_SERVER_WRONGRESPONSE,
		'DNSSEC_YES': DNSSEC_YES,
		'DNSSEC_NO': DNSSEC_NO,

		'BOTH_SSHFP_DATA': BOTH_SSHFP_DATA
	}

	with open(config.SERVER_LOG_STRUCTURED_DATA + "_structued_data.json", "w") as f:
		f.write(json.dumps(data_output))

	with open(config.SERVER_LOG_STRUCTURED_DATA + "_error_dns_no_a_record.csv", "w") as f:
		f.write("Type,Timestamp,Domain\n")
		for l in ERROR_DNS_NO_A_RECORD:
			f.write(f"ERROR_DNS_NO_A_RECORD,{l}\n")

	with open(config.SERVER_LOG_STRUCTURED_DATA + "_error_dns_servfail.csv", "w") as f:
		f.write("Type,Timestamp,Domain\n")
		for l in ERROR_DNS_SERVFAIL:
			f.write(f"ERROR_DNS_SERVFAIL,{l}\n")

	with open(config.SERVER_LOG_STRUCTURED_DATA + "_error_dns_timeout.csv", "w") as f:
		f.write("Type,Timestamp,Domain\n")
		for l in ERROR_DNS_TIMEOUT:
			f.write(f"ERROR_DNS_TIMEOUT,{l}\n")

	with open(config.SERVER_LOG_STRUCTURED_DATA + "_error_dns_not_exist.csv", "w") as f:
		f.write("Type,Timestamp,Domain\n")
		for l in ERROR_DNS_NOT_EXIST:
			f.write(f"ERROR_DNS_NOT_EXIST,{l}\n")

	with open(config.SERVER_LOG_STRUCTURED_DATA + "_error_server_no_fp.csv", "w") as f:
		f.write("Type,Timestamp,Domain\n")
		for l in ERROR_SERVER_NO_FP:
			f.write(f"ERROR_SERVER_NO_FP,{l}\n")

	with open(config.SERVER_LOG_STRUCTURED_DATA + "_error_server_servfail.csv", "w") as f:
		f.write("Type,Timestamp,Domain\n")
		for l in ERROR_SERVER_SERVFAIL:
			f.write(f"ERROR_SERVER_SERVFAIL,{l}\n")

	with open(config.SERVER_LOG_STRUCTURED_DATA + "_error_server_nxdomain.csv", "w") as f:
		f.write("Type,Timestamp,Domain\n")
		for l in ERROR_SERVER_NXDOMAIN:
			f.write(f"ERROR_SERVER_NXDOMAIN,{l}\n")

	with open(config.SERVER_LOG_STRUCTURED_DATA + "_error_server_wrongresponse.csv", "w") as f:
		f.write("Type,Timestamp,Domain\n")
		for l in ERROR_SERVER_WRONGRESPONSE:
			f.write(f"ERROR_SERVER_WRONGRESPONSE,{l}\n")

	with open(config.SERVER_LOG_STRUCTURED_DATA + "_dnssec.csv", "w") as f:
		f.write("DNSSEC,Timestamp,Domain\n")
		for l in DNSSEC_NO:
			f.write(f"No,{l}\n")
		for l in DNSSEC_YES:
			f.write(f"Yes,{l}\n")

