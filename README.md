SSFHP DNS Measurement
====================

This repository contains the code and references to the datasets in the paper:

- `Oh SSH-it, what's my fingerprint? A Large-Scale Analysis of SSH Host Key Fingerprint Verification Records in the DNS`

- Find the paper here [0] and a preprint on ArXiv [1]

- Find the datasets on Zenodo [2]

# Abstract

The SSH protocol is commonly used to access remote systems on the Internet, as it provides an encrypted and authenticated channel for communication.
If upon establishing a new connection, the presented server key is unknown to the client, the user is asked to verify the key fingerprint manually, which is prone to errors and often blindly trusted.
The SSH standard describes an alternative to such manual key verification: using the Domain Name System (DNS) to publish the server key information in SSHFP records.

In this paper, we conduct a large-scale Internet study to measure the prevalence of SSHFP records among DNS domain names. We scan the Tranco 1M list and over 500 million names from the certificate transparency log over the course of 26 days.
The results show that in two studied populations, about 1 in 10,000 domains has SSHFP records,
with more than half of them deployed without using DNSSEC, drastically reducing security benefits.

# Tool usage

- Define the `DOMAINSOURCE` in the `docker-compose.yml`. If `certstream` is chosen, the certificate transparency log stream is used as a continuous source of domains. The other option is `domainfile` and a provided `DOMAINFILE`.

- Customize the number of `*_WORKERS` in `collector/app/config.py` if necessary.

- Run the scan using `sudo docker-compose up --build --force-recreate`.

- To analyze the data, update the two symlinks `logdir_certstream` and `logdir_tranco1m` in `collector/data/` to point to your new scan's log dirs.

- Uncomment the datacleaning and analysis functions in `collector/data/analysis.py` and run `python3 analysis.py`.


# References

[0] https://link.springer.com/chapter/10.1007/978-3-031-20974-1_4
[1] https://arxiv.org/abs/2208.08846
[2] https://zenodo.org/record/6993096