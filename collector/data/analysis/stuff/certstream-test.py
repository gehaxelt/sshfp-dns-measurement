
import certstream
import time
from collections import Counter

DOMAIN_COUNTER = Counter()
CERT_CNT = 0

start = time.time()

def certstream_callback(message, context):
    global CERT_CNT
    global DOMAIN_COUNTER
    global start

    if not message['message_type'] == "certificate_update":
        return

    all_domains = message['data']['leaf_cert']['all_domains']

    if len(all_domains) == 0:
        return

    for domain in all_domains:
        if domain[0] == '*':
            continue

        DOMAIN_COUNTER.update([domain])

    CERT_CNT += 1
    if CERT_CNT % 1000 == 0:
        stop = time.time()
        print(CERT_CNT, stop-start, len(DOMAIN_COUNTER), DOMAIN_COUNTER.most_common(10))
        start = stop

certstream.listen_for_events(certstream_callback, url='wss://certstream.calidog.io/')

"""
[sneef@WorkTop analysis]$ python3 /tmp/ct-test.py 
1000 9.354507207870483 1451 [('sni.cloudflaressl.com', 15), ('z3napitest-e86360af6178db197d830f12c5c37ef9.zendesk.com', 3), ('www.aotusa1.com', 3), ('tls.automattic.com', 3), ('azure-device-registration.i-d-dvce.iekube.datto.net', 3), ('register.ids.nl.erwinbon.com', 2), ('aida.production.wmse.basecom.de', 2), ('at.production.wmse.basecom.de', 2), ('cz.production.wmse.basecom.de', 2), ('de.production.wmse.basecom.de', 2)]
2000 7.66203761100769 2558 [('sni.cloudflaressl.com', 37), ('z3napitest-e86360af6178db197d830f12c5c37ef9.zendesk.com', 6), ('tls.automattic.com', 4), ('visolit.nu', 4), ('cpanel.sgreservatorios.com.br', 3), ('cpcalendars.sgreservatorios.com.br', 3), ('cpcontacts.sgreservatorios.com.br', 3), ('mail.sgreservatorios.com.br', 3), ('scholarshipbrasil.com.br', 3), ('sgreservatorios.com.br', 3)]
3000 7.890012741088867 3322 [('sni.cloudflaressl.com', 45), ('tls.automattic.com', 7), ('kc.vedge-dev.axon-networks.com', 7), ('z3napitest-e86360af6178db197d830f12c5c37ef9.zendesk.com', 6), ('visolit.nu', 6), ('telco.direct.quickconnect.to', 5), ('minakata.direct.quickconnect.to', 4), ('autodiscover.candlejoy.com', 4), ('candlejoy.com', 4), ('cpanel.candlejoy.com', 4)]
4000 6.6348021030426025 3982 [('sni.cloudflaressl.com', 57), ('tls.automattic.com', 9), ('z3napitest-e86360af6178db197d830f12c5c37ef9.zendesk.com', 7), ('telco.direct.quickconnect.to', 7), ('kc.vedge-dev.axon-networks.com', 7), ('visolit.nu', 6), ('minakata.direct.quickconnect.to', 5), ('52flq.com', 5), ('kuniovn.myds.me', 5), ('markitsmart.kringle.ai', 5)]
5000 6.856921911239624 4908 [('sni.cloudflaressl.com', 78), ('tls.automattic.com', 9), ('kc.vedge-dev.axon-networks.com', 9), ('z3napitest-e86360af6178db197d830f12c5c37ef9.zendesk.com', 7), ('telco.direct.quickconnect.to', 7), ('www.linkwide.in', 6), ('visolit.nu', 6), ('kuniovn.myds.me', 6), ('markitsmart.kringle.ai', 6), ('location4event.com', 6)]
6000 7.201345205307007 5449 [('sni.cloudflaressl.com', 92), ('tls.automattic.com', 10), ('kc.vedge-dev.axon-networks.com', 9), ('www.linkwide.in', 7), ('z3napitest-e86360af6178db197d830f12c5c37ef9.zendesk.com', 7), ('telco.direct.quickconnect.to', 7), ('location4event.com', 7), ('52flq.com', 6), ('visolit.nu', 6), ('kuniovn.myds.me', 6)]
7000 8.51852536201477 6274 [('sni.cloudflaressl.com', 233), ('tls.automattic.com', 12), ('location4event.com', 11), ('hanacloud.ondemand.com', 9), ('kc.vedge-dev.axon-networks.com', 9), ('www.linkwide.in', 8), ('z3napitest-e86360af6178db197d830f12c5c37ef9.zendesk.com', 8), ('telco.direct.quickconnect.to', 7), ('ds216elars.synology.me', 7), ('lathrop-cam.direct.quickconnect.to', 7)]
8000 8.193208456039429 6824 [('sni.cloudflaressl.com', 392), ('hanacloud.ondemand.com', 17), ('tls.automattic.com', 13), ('location4event.com', 11), ('kc.vedge-dev.axon-networks.com', 9), ('www.linkwide.in', 8), ('z3napitest-e86360af6178db197d830f12c5c37ef9.zendesk.com', 8), ('telco.direct.quickconnect.to', 7), ('lepri.direct.quickconnect.to', 7), ('ds216elars.synology.me', 7)]
9000 8.673211574554443 7782 [('sni.cloudflaressl.com', 566), ('hanacloud.ondemand.com', 39), ('tls.automattic.com', 15), ('location4event.com', 11), ('trakal.ltz.life', 9), ('kc.vedge-dev.axon-networks.com', 9), ('www.linkwide.in', 8), ('z3napitest-e86360af6178db197d830f12c5c37ef9.zendesk.com', 8), ('telco.direct.quickconnect.to', 7), ('lepri.direct.quickconnect.to', 7)]
10000 9.131265878677368 8412 [('sni.cloudflaressl.com', 656), ('hanacloud.ondemand.com', 47), ('tls.automattic.com', 16), ('location4event.com', 12), ('trakal.ltz.life', 11), ('kc.vedge-dev.axon-networks.com', 9), ('www.linkwide.in', 8), ('z3napitest-e86360af6178db197d830f12c5c37ef9.zendesk.com', 8), ('ftp.ingeper.cl', 7), ('ingeper.cl', 7)]
[...]
"""