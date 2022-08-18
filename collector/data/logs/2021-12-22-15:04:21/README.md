Dataset: 2021-12-22-15:04:21.tar.lrz
====================================

As the dataset is too large for GitHub, it has been uploaded to Zenodo and is available at [0].
Lrzip [1] was used to minimize its size. 

Download all the parts `.tar.lrz-00` through `.tar.lrz-10` and concatenate them: `cat ./*.tar.lrz-* > /tmp/2021-12-22-15:04:21.tar.lrz`.

Files in this dataset:

```
ls 2021-12-22-15\:04\:21
total 11G
drwxr-xr-x  2 sneef sneef 4.0K Aug 15 15:43 .
drwxr-xr-x 62 sneef sneef 4.0K Aug 15 15:51 ..
-rw-r--r--  1 sneef sneef 4.2G May 23 12:43 certstream.log.new.gz
-rw-r--r--  1 sneef sneef 3.3M May 23 12:37 parser.log.new.gz
-rw-r--r--  1 sneef sneef 6.0G May 23 12:52 query.log.new.gz
-rw-r--r--  1 sneef sneef  104 Dec 22  2021 README
-rw-r--r--  1 sneef sneef 6.3M May 23 12:37 server.log.new.gz
```

[0] https://zenodo.org/record/6993096
[1] https://github.com/ckolivas/lrzip 
