#!/usr/bin/env python3
import json
import re
import io
import time

class SSHFP:
    ALGO_RESERVED = 0 # RFC 4255
    ALGO_RSA = 1 # RFC 4255
    ALGO_DSA = 2 # RFC 4255
    ALGO_ECDSA = 3 # RFC 6594
    ALGO_ED25519 = 4 # RFC 7479
    ALGO_ED448 = 6 # RFC 8709

    TYPE_RESERVED = 0 # RFC 4255
    TYPE_SHA1 = 1  # RFC 4255
    TYPE_SHA256 = 2 # RFC 6594

    REGEX_SHA1 = re.compile(r'^[a-f0-9]{40}$')
    REGEX_SHA256 = re.compile(r'^[a-f0-9]{64}$')
    REGEX_SSHFP = re.compile(r'^(0|1|2|3|4|6) (0|1|2) ([a-f0-9]{40}|[a-f0-9]{64})$')

    def __init__(self, *args, algo=None, ftype=None, fingerprint=None, domain=None, timestamp=None, **kwargs):
        if type(algo) == str:
            algo = SSHFP.algo_to_id(algo)

        if not algo in [SSHFP.ALGO_RESERVED, SSHFP.ALGO_RSA, SSHFP.ALGO_DSA, SSHFP.ALGO_ECDSA, SSHFP.ALGO_ED25519, SSHFP.ALGO_ED448]:
            raise Exception(f"Wrong algorithm {algo}")
        else:
            self.algo = algo

        if type(ftype) == str:
            ftype = SSHFP.type_to_id(ftype)

        if not ftype in [SSHFP.TYPE_RESERVED, SSHFP.TYPE_SHA1, SSHFP.TYPE_SHA256]:
            raise Exception(f"Wrong type {ftype}")
        else:
            self.type = ftype

        fingerprint = fingerprint.lower()
        if not (SSHFP.REGEX_SHA1.fullmatch(fingerprint) and self.type == SSHFP.TYPE_SHA1) and not ( SSHFP.REGEX_SHA256.fullmatch(fingerprint) and self.type == SSHFP.TYPE_SHA256):
            raise Exception(f"Wrong fingerprint {fingerprint}")
        else:
            self.fingerprint = fingerprint

        self.domain = domain
        self.timestamp = timestamp

    def algo_stringified(self):
        return SSHFP.algo_to_str(self.algo)

    def type_stringified(self):
        return SSHFP.type_to_str(self.type)

    def to_dns(self):
        return f"{self.domain} IN SSHFP {self.algo} {self.type} {self.fingerprint}"

    def to_dict(self):
        return {
            'algo': SSHFP.algo_to_str(self.algo),
            'type': SSHFP.type_to_str(self.type),
            'fingerprint': self.fingerprint,
            'domain': self.domain,
            'timestamp': self.timestamp
            }

    def to_json(self):
        return json.dumps(self.to_dict(), default=lambda o: o.__dict__)

    @classmethod
    def from_json(cls, j):
        data = json.loads(j)
        return SSHFP.from_dict(data)

    @classmethod
    def from_dict(cls, d):
        # required args
        for k in ['algo', 'type', 'fingerprint']:
            if not k in d:
                raise Exception(f"SSHFP key {k} was not found")
        default = {
            'domain': None,
            'timestamp': 0,
        }
        # optional args
        for k in ['domain', 'timestamp']:
            if k in d:
                default[k] = d[k]

        return SSHFP(algo=d['algo'], ftype=d['type'], fingerprint=d['fingerprint'], domain=default['domain'], timestamp=default['timestamp'])

    @classmethod
    def from_string(cls, s):
        match = SSHFP.REGEX_SSHFP.match(s)
        if not match:
            raise Exception(f"No match found in {s}")
        match = match.groups(0)
        algo = int(match[0])
        t = int(match[1])
        fp = match[2]
        return SSHFP(algo=algo, ftype=t, fingerprint=fp)

    @classmethod
    def algo_to_id(cls, s):
        if s == "RESERVED":
            return SSHFP.ALGO_RESERVED
        elif s == "RSA":
            return SSHFP.ALGO_RSA
        elif s == "DSA":
            return SSHFP.ALGO_DSA
        elif s == "ECDSA":
            return SSHFP.ALGO_ECDSA
        elif s == "ED25519":
            return SSHFP.ALGO_ED25519
        elif s == "ED448":
            return SSHFP.ALGO_ED448
        else:
            raise Exception(f"Wrong Algorithm {s}")

    @classmethod
    def algo_to_str(cls, algo):
        if algo == SSHFP.ALGO_RESERVED:
            return "RESERVED"
        elif algo == SSHFP.ALGO_RSA:
            return "RSA"
        elif algo == SSHFP.ALGO_DSA:
            return "DSA"
        elif algo == SSHFP.ALGO_ECDSA:
            return "ECDSA"
        elif algo == SSHFP.ALGO_ED25519:
            return "ED25519"
        elif algo == SSHFP.ALGO_ED448:
            return "ED448"
        else:
            raise Exception(f"Wrong algorith {algo}")

    @classmethod
    def type_to_str(cls, t):
        if t == SSHFP.TYPE_RESERVED:
            return "RESERVED"
        elif t == SSHFP.TYPE_SHA1:
            return "SHA1"
        elif t == SSHFP.TYPE_SHA256:
            return "SHA256"

    @classmethod
    def type_to_id(cls, s):
        if s == "RESERVED":
            return SSHFP.TYPE_RESERVED
        elif s == "SHA1":
            return SSHFP.TYPE_SHA1
        elif s == "SHA256":
            return SSHFP.TYPE_SHA256
        else:
            raise Exception(f"Wrong Type {s}")

class SSHFPDomain:
    def __init__(self, *args, domain=None, timestamp=None, sshfp_records=None, **kwargs):
        self.domain = domain
        self.timestamp = timestamp

        if not sshfp_records:
            self.records = []
        else:
            self.records = sshfp_records

    def to_dns(self):
        out = io.StringIO()
        for record in self.records:
            out.write(record.to_dns())
            out.write("\n")
        return out.getvalue()

    def to_dict(self):
        return {
            'domain': self.domain,
            'timestamp': self.timestamp,
            'records': self.records,
            }

    def to_json(self):
        return json.dumps(self.to_dict(), default=lambda o: o.to_dict())

    @classmethod
    def from_json(cls, j):
        data = json.loads(j)
        return SSHFPDomain.from_dict(data)

    @classmethod
    def from_dict(cls, d):
        for k in ['domain', 'timestamp', 'records']:
            if not k in d:
                raise Exception(f"SSHFP key {k} was not found")
        sshfpd = SSHFPDomain(domain=d['domain'], timestamp=d['timestamp'])
        for record in d['records']:
            sshfp = SSHFP.from_dict(record)
            sshfpd.records.append(sshfp)
        return sshfpd

class SSHFPComparison:
    def __init__(self,*args, domain=None, dns_sshfp=None, server_sshfp=None, errors=None, is_authentic=None, **kwargs):
        self.domain = domain
        self.dns_sshfp = dns_sshfp
        self.server_sshfp = server_sshfp
        self.errors = errors
        self.is_authentic = is_authentic

    def to_json(self):
        return json.dumps({
            'domain': self.domain,
            'dns': self.dns_sshfp,
            'server': self.server_sshfp,
            'errors': self.errors,
            'is_authentic': self.is_authentic
            }, default=lambda o: o.to_dict())

if __name__ == "__main__":
    sshfp = SSHFP(algo=SSHFP.ALGO_RSA, ftype=SSHFP.TYPE_SHA1, fingerprint="66b4b3d36098ec5231fcce828a8bf6ad3252fd71", domain="test.org", timestamp=int(time.time()))
    sshfpd = SSHFPDomain(domain="test.org", timestamp=int(time.time()), sshfp_records=[sshfp])