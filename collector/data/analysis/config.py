import os

class Config:
	DATA_BASEDIR = "./logdir/"
	RESULTS_DIR = "./results/"
	FIGURES_DIR = "./figures/"
	KEY = "default"
	STORE = {}

	def storeData(self, k, d):
		self.STORE[f"{self.KEY}_{k}"] = d

	def getData(self, k):
		return self.STORE[f"{self.KEY}_{k}"]

	####
	#
	# Datacleaning
	#
	####

	@property
	def DOMAINFILE_LOG_GZ(self):
		return self.DATA_BASEDIR + os.path.sep + "domainfile.log.new.gz" 

	@property
	def DOMAINFILE_COUNTED_UNIQUE_DOMAINS(self):
		return self.RESULTS_DIR + os.path.sep + "domainfile_counted_unique_domains"
	

	@property
	def CERTSTREAM_LOG_GZ(self):
		return self.DATA_BASEDIR + os.path.sep + "certstream.log.new.gz" 
	
	@property
	def CERTSTREAM_COUNTED_UNIQUE_DOMAINS(self):
		return self.RESULTS_DIR + os.path.sep + "certstream_counted_unique_domains"

	@property
	def QUERY_LOG_GZ(self):
		return self.DATA_BASEDIR + os.path.sep + "query.log.new.gz"
	
	@property
	def QUERY_LOG_COUNTED_MESSAGES(self):
		return self.RESULTS_DIR + os.path.sep + "querylog_counted_messages"

	@property
	def PARSER_LOG_GZ(self):
		return self.DATA_BASEDIR + os.path.sep + "parser.log.new.gz"
	
	@property
	def PARSER_LOG_STRUCTED_DATA(self):
		return self.RESULTS_DIR + os.path.sep + "parserlog_structured_data"

	@property
	def SERVER_LOG_GZ(self):
		return self.DATA_BASEDIR + os.path.sep + "server.log.new.gz"

	@property
	def SERVER_LOG_STRUCTURED_DATA(self):
		return self.RESULTS_DIR + os.path.sep + "serverlog_structured_data"
	

	######
	#
	# Analysis
	#
	######

	@property
	def DOMAINFILE_ANALYSIS_SCANNED_OUTFILE(self):
		return self.RESULTS_DIR + os.path.sep + "domainfile_analysis_scanned_domains.txt"
	

	@property
	def CERTSTREAM_ANALYSIS_SKIPPED_OUTFILE(self):
		return self.RESULTS_DIR + os.path.sep + "certstream_analysis_skipped_domains.txt"
	
	@property
	def CERTSTREAM_ANALYSIS_SCANNED_OUTFILE(self):
		return self.RESULTS_DIR + os.path.sep + "certstream_analysis_scanned_domains.txt"

	@property
	def QUERYLOG_ANALYSIS_OUTFILE_NO_SSHFP(self):
		return self.RESULTS_DIR + os.path.sep + "querylog_analysis_err_no_sshfp.txt"

	@property
	def QUERYLOG_ANALYSIS_OUTFILE_NO_ANSWER(self):
		return self.RESULTS_DIR + os.path.sep + "querylog_analysis_err_no_answer.txt"

	@property
	def QUERYLOG_ANALYSIS_OUTFILE_NO_QUERYNAME(self):
		return self.RESULTS_DIR + os.path.sep + "querylog_analysis_err_no_queryname.txt"

	@property
	def QUERYLOG_ANALYSIS_OUTFILE_TIMEOUT(self):
		return self.RESULTS_DIR + os.path.sep + "querylog_analysis_err_timeout.txt"

	@property
	def QUERYLOG_ANALYSIS_OUTFILE_LABEL(self):
		return self.RESULTS_DIR + os.path.sep + "querylog_analysis_err_label.txt"

	@property
	def QUERYLOG_ANALYSIS_OUTFILE_FOUND_SSHFP(self):
		return self.RESULTS_DIR + os.path.sep + "querylog_analysis_found_sshfp.txt"

	@property
	def PARSERLOG_ANALYSIS_OUTFILE(self):
		return self.RESULTS_DIR + os.path.sep + "parserlog_analysis_errors_and_sshfps.txt"

	@property
	def SERVERLOG_ANALYSIS_OUTFILE(self):
		return self.RESULTS_DIR + os.path.sep + "serverlog_analysis_all.txt"

	@property
	def SERVERLOG_ANALYSIS_PTR_MAPPING(self):
		return self.RESULTS_DIR + os.path.sep + "serverlog_ptr_mapping.json"

	@property
	def SERVERLOG_ANALYSIS_PTR_OUT(self):
		return self.RESULTS_DIR + os.path.sep + "serverlog_analysis_ptr.txt"

	@property
	def PARSERLOG_ANALYSIS_V6(self):
		return self.RESULTS_DIR + os.path.sep + "parserlog_analysis_v6.json"
	@property
	def PARSERLOG_ANALYSIS_V6_OUT(self):
		return self.RESULTS_DIR + os.path.sep + "parserlog_analysis_v6_out.txt"
	
	
	
config = Config()