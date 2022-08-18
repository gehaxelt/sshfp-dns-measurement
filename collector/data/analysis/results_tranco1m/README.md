Dataset: results_tranco1m.tar.lrz
====================================

As the dataset is too large for GitHub, it has been uploaded to Zenodo and is available at [0].
Lrzip [1] was used to minimize its size. 

Files in this dataset:

```
ls results_tranco1m
total 79M
drwxr-xr-x  2 sneef sneef 4.0K Jun  8 17:03 .
drwxr-xr-x 11 sneef sneef 4.0K Aug 15 13:24 ..
-rw-r--r--  1 sneef sneef  850 Jun  8 22:38 domainfile_analysis_scanned_domains.txt
-rw-r--r--  1 sneef sneef  21M May 25 12:28 domainfile_counted_unique_domains.json
-rw-r--r--  1 sneef sneef  19M May 25 12:28 domainfile_counted_unique_domains_unique_domains.csv
-rw-r--r--  1 sneef sneef 4.0K May 27 03:03 parserlog_analysis_errors_and_sshfps.txt
-rw-r--r--  1 sneef sneef  16K Jun  8 16:32 parserlog_analysis_v6.json
-rw-r--r--  1 sneef sneef   83 Jun  8 17:04 parserlog_analysis_v6_out.txt
-rw-r--r--  1 sneef sneef  226 May 25 12:28 parserlog_structured_data_errors.csv
-rw-r--r--  1 sneef sneef  66K May 25 12:28 parserlog_structured_data_structued_data.json
-rw-r--r--  1 sneef sneef  31K May 25 12:28 parserlog_structured_data_timesorted_sshpfs.csv
-rw-r--r--  1 sneef sneef    0 Jun  8 22:38 querylog_analysis_err_label.txt
-rw-r--r--  1 sneef sneef  900 Jun  8 22:38 querylog_analysis_err_no_answer.txt
-rw-r--r--  1 sneef sneef  915 Jun  8 22:38 querylog_analysis_err_no_queryname.txt
-rw-r--r--  1 sneef sneef  909 Jun  8 22:38 querylog_analysis_err_no_sshfp.txt
-rw-r--r--  1 sneef sneef  844 Jun  8 22:38 querylog_analysis_err_timeout.txt
-rw-r--r--  1 sneef sneef  829 Jun  8 22:38 querylog_analysis_found_sshfp.txt
-rw-r--r--  1 sneef sneef   27 May 25 12:28 querylog_counted_messages_err_label.csv
-rw-r--r--  1 sneef sneef 589K May 25 12:28 querylog_counted_messages_err_no_answer.csv
-rw-r--r--  1 sneef sneef 269K May 25 12:28 querylog_counted_messages_err_no_queryname.csv
-rw-r--r--  1 sneef sneef  18M May 25 12:28 querylog_counted_messages_err_no_sshfp.csv
-rw-r--r--  1 sneef sneef  58K May 25 12:28 querylog_counted_messages_err_timeout.csv
-rw-r--r--  1 sneef sneef 1.8K May 25 12:28 querylog_counted_messages_found_sshfp.csv
-rw-r--r--  1 sneef sneef  21M May 25 12:28 querylog_counted_messages.json
-rw-r--r--  1 sneef sneef 4.4K Jun  9 15:57 serverlog_analysis_all.txt
-rw-r--r--  1 sneef sneef  241 Jun  8 11:45 serverlog_analysis_ptr.txt
-rw-r--r--  1 sneef sneef 5.4K Jun  7 23:58 serverlog_ptr_mapping.json
-rw-r--r--  1 sneef sneef 2.0K Jun  7 15:57 serverlog_structured_data_dnssec.csv
-rw-r--r--  1 sneef sneef   22 Jun  7 15:57 serverlog_structured_data_error_dns_no_a_record.csv
-rw-r--r--  1 sneef sneef   22 Jun  7 15:57 serverlog_structured_data_error_dns_not_exist.csv
-rw-r--r--  1 sneef sneef   69 Jun  7 15:57 serverlog_structured_data_error_dns_servfail.csv
-rw-r--r--  1 sneef sneef   22 Jun  7 15:57 serverlog_structured_data_error_dns_timeout.csv
-rw-r--r--  1 sneef sneef 1.5K Jun  7 15:57 serverlog_structured_data_error_server_no_fp.csv
-rw-r--r--  1 sneef sneef   22 Jun  7 15:57 serverlog_structured_data_error_server_nxdomain.csv
-rw-r--r--  1 sneef sneef   22 Jun  7 15:57 serverlog_structured_data_error_server_servfail.csv
-rw-r--r--  1 sneef sneef   22 Jun  7 15:57 serverlog_structured_data_error_server_wrongresponse.csv
-rw-r--r--  1 sneef sneef 129K Jun  7 15:57 serverlog_structured_data_structued_data.json
```

[0] https://zenodo.org/record/6993096
[1] https://github.com/ckolivas/lrzip 