Dataset: results_certstream.tar.lrz
====================================

As the dataset is too large for GitHub, it has been uploaded to Zenodo and is available at [0].
Lrzip [1] was used to minimize its size. 

Files in this dataset:

```
ls results_certstream
total 17G
drwxr-xr-x  2 sneef sneef 4.0K Jun  8 19:26 .
drwxr-xr-x 11 sneef sneef 4.0K Aug 15 13:24 ..
-rw-r--r--  1 sneef sneef 1.3K Jun  8 22:54 certstream_analysis_scanned_domains.txt
-rw-r--r--  1 sneef sneef 1.2K Jun  8 22:39 certstream_analysis_skipped_domains.txt
-rw-r--r--  1 sneef sneef 4.5G May 23 13:21 certstream_counted_unique_domains.json
-rw-r--r--  1 sneef sneef  450 May 23 13:22 certstream_counted_unique_domains_otherlines.csv
-rw-r--r--  1 sneef sneef 602M May 23 13:22 certstream_counted_unique_domains_skipped_domains.csv
-rw-r--r--  1 sneef sneef 3.6G May 23 13:22 certstream_counted_unique_domains_unique_domains.csv
-rw-r--r--  1 sneef sneef 6.1K Jun  3 16:48 parserlog_analysis_errors_and_sshfps.txt
-rw-r--r--  1 sneef sneef  39K Jun  3 16:48 parserlog_analysis_errors_and_sshfps.txt_errors.txt
-rw-r--r--  1 sneef sneef 3.1M Jun  8 19:20 parserlog_analysis_v6.json
-rw-r--r--  1 sneef sneef   94 Jun  8 19:26 parserlog_analysis_v6_out.txt
-rw-r--r--  1 sneef sneef  37K May 23 13:41 parserlog_structured_data_errors.csv
-rw-r--r--  1 sneef sneef  45M May 23 13:41 parserlog_structured_data_structued_data.json
-rw-r--r--  1 sneef sneef  22M May 23 13:41 parserlog_structured_data_timesorted_sshpfs.csv
-rw-r--r--  1 sneef sneef 2.1K Jun  8 23:09 querylog_analysis_err_label.txt
-rw-r--r--  1 sneef sneef 1.2K Jun  8 23:09 querylog_analysis_err_no_answer.txt
-rw-r--r--  1 sneef sneef 1.4K Jun  8 23:09 querylog_analysis_err_no_queryname.txt
-rw-r--r--  1 sneef sneef 1.3K Jun  8 23:08 querylog_analysis_err_no_sshfp.txt
-rw-r--r--  1 sneef sneef 1.1K Jun  8 23:09 querylog_analysis_err_timeout.txt
-rw-r--r--  1 sneef sneef 1.1K Jun  8 23:09 querylog_analysis_found_sshfp.txt
-rw-r--r--  1 sneef sneef 2.6K May 23 13:41 querylog_counted_messages_err_label.csv
-rw-r--r--  1 sneef sneef  76M May 23 13:41 querylog_counted_messages_err_no_answer.csv
-rw-r--r--  1 sneef sneef 206M May 23 13:41 querylog_counted_messages_err_no_queryname.csv
-rw-r--r--  1 sneef sneef 3.4G May 23 13:41 querylog_counted_messages_err_no_sshfp.csv
-rw-r--r--  1 sneef sneef 7.0M May 23 13:41 querylog_counted_messages_err_timeout.csv
-rw-r--r--  1 sneef sneef 423K May 23 13:41 querylog_counted_messages_found_sshfp.csv
-rw-r--r--  1 sneef sneef 3.9G May 23 13:40 querylog_counted_messages.json
-rw-r--r--  1 sneef sneef 6.0K Jun  9 15:57 serverlog_analysis_all.txt
-rw-r--r--  1 sneef sneef  259 Jun  8 00:51 serverlog_analysis_ptr.txt
-rw-r--r--  1 sneef sneef 305K Jun  8 00:24 serverlog_ptr_mapping.json
-rw-r--r--  1 sneef sneef 1.4M May 23 22:41 serverlog_structured_data_dnssec.csv
-rw-r--r--  1 sneef sneef  63K May 23 22:41 serverlog_structured_data_error_dns_no_a_record.csv
-rw-r--r--  1 sneef sneef   74 May 23 22:41 serverlog_structured_data_error_dns_not_exist.csv
-rw-r--r--  1 sneef sneef 9.1K May 23 22:41 serverlog_structured_data_error_dns_servfail.csv
-rw-r--r--  1 sneef sneef  239 May 23 22:41 serverlog_structured_data_error_dns_timeout.csv
-rw-r--r--  1 sneef sneef 1.7M May 23 22:41 serverlog_structured_data_error_server_no_fp.csv
-rw-r--r--  1 sneef sneef 1.7K May 23 22:41 serverlog_structured_data_error_server_nxdomain.csv
-rw-r--r--  1 sneef sneef  17K May 23 22:41 serverlog_structured_data_error_server_servfail.csv
-rw-r--r--  1 sneef sneef   79 May 23 22:41 serverlog_structured_data_error_server_wrongresponse.csv
-rw-r--r--  1 sneef sneef  70M May 23 22:41 serverlog_structured_data_structued_data.json
```

[0] 
[1] https://github.com/ckolivas/lrzip 