from collections import Counter

def main():
	from config import config
	import scripts.datacleaning
	import scripts.analysis
	import scripts.figures

	####
	#
	# General figures
	#
	####
	
	# scripts.figures.sshfp_dnssec_barplot()
	

	## Tranco-1M-Scan
	config.DATA_BASEDIR = "./logdir_tranco1m/"
	config.RESULTS_DIR = "./results_tranco1m/"
	config.FIGURES_DIR = "./figures_tranco1m/"
	config.KEY = "tranco1m"

	####
	#
	# Datacleaning
	#
	####
	# Read the domainfile log and create a list of unique domains and skipped wirldcards
	# scripts.datacleaning.domainfile_log_to_unique_domainlist_with_count()

	# Read the query log and analyze its (error) messages
	# scripts.datacleaning.querylog_to_counted_messages()

	# Read the parser log and structure its data
	# scripts.datacleaning.parserlog_to_structured_data()

	# Read the server log and structure its data
	# scripts.datacleaning.server_to_structured_data()

	####
	#
	# Analysis
	#
	####
	# Count the number of scanned domains
	# scripts.analysis.domainfile_general_numbers_scanned_domains()
	# Count the errors and successful SSHFP queries:
	# scripts.analysis.query_log_analysis()
	# Analyze the parser errors and successfully parsed SSHFP entries
	# scripts.analysis.parserlog_analysis()
	# 
	scripts.analysis.serverlog_analysis()

	#scripts.analysis.serverlog_ptr_analysis(mode=1)
	#scripts.analysis.serverlog_ptr_analysis(mode=2)

	#scripts.analysis.parserlog_domain_v6_analysis(mode=1)
	#scripts.analysis.parserlog_domain_v6_analysis(mode=2)

	######
	#
	# Figures
	#
	######
	# config.storeData("sshfp_match_ratio", Counter({1.0: 36, 0.5: 26, 0.0: 9, 0.3333333333333333: 1, 0.25: 1, 0.16666666666666666: 1, 0.6666666666666666: 1}))
	# scripts.figures.sshfp_match_ratio()

	## Certstream-Scan
	config.DATA_BASEDIR = "./logdir_certstream/"
	config.RESULTS_DIR = "./results_certstream/"
	config.FIGURES_DIR = "./figures_certstream/"
	config.KEY = "certstream"


	####
	#
	# Datacleaning
	#
	####
	# Read certstream.log.gz and create a list of unique domains and skipped wildcards.
	#scripts.datacleaning.cerstream_log_to_unique_domainlist_with_count()
	
	# Read the query log and analyze its (error) messages
	#scripts.datacleaning.querylog_to_counted_messages()

	# Read the parser log and structure its data
	#scripts.datacleaning.parserlog_to_structured_data()

	# Read the server log and structure its data
	# scripts.datacleaning.server_to_structured_data()

	####
	#
	# Analysis
	#
	####
	# Count the number of wildcards in the certstream log
	# scripts.analysis.cerstream_general_numbers_skipped()
	# Count the number of scanned domains
	# scripts.analysis.cerstream_general_numbers_scanned_domains()
	# Count the errors and successful SSHFP queries:
	# scripts.analysis.query_log_analysis()
	# Analyze the parser errors and successfully parsed SSHFP entries
	# scripts.analysis.parserlog_analysis()
	# 
	scripts.analysis.serverlog_analysis()

	#scripts.analysis.serverlog_ptr_analysis(mode=1)
	#scripts.analysis.serverlog_ptr_analysis(mode=2)

	#scripts.analysis.parserlog_domain_v6_analysis(mode=1)
	# scripts.analysis.parserlog_domain_v6_analysis(mode=2)


	######
	#
	# Figures
	#
	######
	# config.storeData("sshfp_match_ratio", Counter({0.5: 8980, 1.0: 3857, 0.0: 1816, 0.25: 942, 0.6666666666666666: 227, 0.3333333333333333: 184, 0.16666666666666666: 142, 0.75: 115, 0.8333333333333334: 68}))
	# scripts.figures.sshfp_match_ratio()



if __name__ == "__main__":
	main()
