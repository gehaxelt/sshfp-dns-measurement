
import matplotlib.pyplot as pyplot
from matplotlib import cm
import numpy as np
import os

from collections import Counter
from config import config

def resetPyPlot():
	pyplot.clf()
	pyplot.style.use(['default'])
	pyplot.rcParams['text.usetex'] = True
	pyplot.rcParams['font.size'] = 10
	pyplot.rcParams['legend.fontsize'] = 10
	pyplot.rcParams['xtick.direction'] = 'out'
	pyplot.rcParams['ytick.direction'] = 'out'


def getColor(c, N, idx):
	import matplotlib as mpl
	cmap = mpl.cm.get_cmap(c)
	norm = mpl.colors.Normalize(vmin=0.0, vmax=N - 1)
	return cmap(norm(idx))


def sshfp_match_ratio():
	resetPyPlot()

	SSHFP_MATCH_RATIO = config.getData("sshfp_match_ratio")
	print(SSHFP_MATCH_RATIO)
	n = len(SSHFP_MATCH_RATIO)
	print(np.arange(1,n)/float(n))
	cs=cm.Greys(np.arange(1, n)/float(n*1.5))
	
	pyplot.clf()
	pyplot.axis("equal")

	nsum = sum(SSHFP_MATCH_RATIO.values())
	#pyplot.title("Match ratio of the DNS and server fingerprints")
	pyplot.pie([float(v) for v in SSHFP_MATCH_RATIO.values()], labels=[f"{int(round(k,2) * 100)}\% ({SSHFP_MATCH_RATIO[k]}, {round(SSHFP_MATCH_RATIO[k]/nsum*100,2)}\%)" for k in SSHFP_MATCH_RATIO], autopct=None, colors=cs, labeldistance=1.5)
	
	pyplot.margins(0,0)
	pyplot.gca().xaxis.set_major_locator(pyplot.NullLocator())
	pyplot.gca().yaxis.set_major_locator(pyplot.NullLocator())
	pyplot.savefig(config.FIGURES_DIR + os.path.sep + "_serverlog_match_ratio.pdf", bbox_inches='tight')

def sshfp_dnssec_barplot():
	resetPyPlot()

	### SSHFP records
	tranco_auth = Counter({'OK': 124, 'NOT OK': 42})
	tranco_unauth = Counter({'OK': 132, 'NOT OK': 82})
	ctlogs_auth = Counter({'OK': 18282, 'NOT OK': 8668})
	ctlogs_unauth = Counter({'NOT OK': 22943, 'OK': 22619})

	ntranco_matching = tranco_auth["OK"] + tranco_unauth["OK"]
	ntranco_mismatching = tranco_auth["NOT OK"] + tranco_unauth["NOT OK"]
	nctlogs_matching = ctlogs_auth["OK"] + ctlogs_unauth["OK"]
	nctlogs_mismatching = ctlogs_auth["NOT OK"] + ctlogs_unauth["NOT OK"]

	labels = ['Tranco 1M\nMatching', 'Tranco 1M\nMismatching', 'CT Log\nMatching', 'CT Log\nMismatching']
	secure = [tranco_auth["OK"]/ntranco_matching, tranco_auth["NOT OK"]/ntranco_mismatching, ctlogs_auth["OK"]/nctlogs_matching, ctlogs_auth["NOT OK"]/nctlogs_mismatching]
	insecure = [tranco_unauth["OK"]/ntranco_matching, tranco_unauth["NOT OK"]/ntranco_mismatching, ctlogs_unauth["OK"]/nctlogs_matching, ctlogs_unauth["NOT OK"]/nctlogs_mismatching]
	width = 0.35       # the width of the bars: can also be len(x) sequence

	secure = list(map(lambda x: x*100, secure))
	insecure = list(map(lambda x: x*100, insecure))


	pyplot.rcParams['text.usetex'] = False
	pyplot.clf()
	fig, (ax1, ax2) = pyplot.subplots(1,2, constrained_layout=True)

	fig.set_size_inches(8, 5.5)


	cs=cm.Greys([0.55,0.55, 0.55, 0.55])
	ax1.bar(labels, secure, width, label='Secure', color=cs)
	
	cs=cm.Greys([0.35,0.35, 0.35, 0.35])
	ax1.bar(labels, insecure, width,bottom=secure, label='Insecure',color=cs)

	ax1.set_ylabel('%')
	ax1.set_title('a) DNSSEC authenticity of \n(mis-)matching SSHFP records.')
	ax1.legend()

	
	for bar in ax1.patches:
		height = bar.get_height()
		width = bar.get_width()
		x = bar.get_x()
		y = bar.get_y()
		label_text = f"{format(round(height,2),'.2f')}%"
		label_x = x + width / 2
		label_y = y + height / 2
		ax1.text(label_x, label_y, label_text, ha='center',    
				va='center',rotation='vertical')


	### SSHFP domains and hosts
	tranco_1m_hosts = Counter({'secure': 27, 'insecure': 32, 'nomatch': 9})
	tranco_1m_domains = Counter({'secure': 28, 'insecure': 35, 'nomatch': 9})

	# only_first_domain_measurement = False
	ctlogs_hosts = Counter({'secure': 1953, 'insecure': 1698, 'nomatch': 313})
	ctlogs_domains = Counter({'secure': 3910, 'insecure': 6635, 'nomatch': 1438})
	
	# only_first_domain_measurement = True
	ctlogs_hosts = Counter({'secure': 1937, 'insecure': 1677, 'nomatch': 284})
	ctlogs_domains = Counter({'secure': 3896, 'insecure': 6482, 'nomatch': 1146})

	ntranco_1m_hosts = sum(tranco_1m_hosts.values())
	ntranco_1m_domains = sum(tranco_1m_domains.values())

	nctlogs_hosts = sum(ctlogs_hosts.values())
	nctlogs_domains = sum(ctlogs_domains.values())

	print(tranco_1m_hosts['secure']/ntranco_1m_hosts + tranco_1m_hosts['insecure']/ntranco_1m_hosts + tranco_1m_hosts['nomatch']/ntranco_1m_hosts)

	labels = ['Tranco 1M\n(hosts)', 'Tranco 1M\n(domains)', 'CT Log\n(hosts)', 'CT Log\n(domains)']
	secure = [tranco_1m_hosts['secure']/ntranco_1m_hosts, tranco_1m_domains['secure']/ntranco_1m_domains, ctlogs_hosts['secure']/nctlogs_hosts, ctlogs_domains['secure']/nctlogs_domains]
	insecure = [tranco_1m_hosts['insecure']/ntranco_1m_hosts, tranco_1m_domains['insecure']/ntranco_1m_domains, ctlogs_hosts['insecure']/nctlogs_hosts, ctlogs_domains['insecure']/nctlogs_domains]
	nomatch = [tranco_1m_hosts['nomatch']/ntranco_1m_hosts, tranco_1m_domains['nomatch']/ntranco_1m_domains, ctlogs_hosts['nomatch']/nctlogs_hosts, ctlogs_domains['nomatch']/nctlogs_domains]
	width = 0.35       # the width of the bars: can also be len(x) sequence

	secure = list(map(lambda x: x*100, secure))
	insecure = list(map(lambda x: x*100, insecure))
	nomatch = list(map(lambda x: x*100, nomatch))

	print(secure[0] + insecure[0] + nomatch[0])
	print(secure[1] + insecure[1] + nomatch[1])
	print(secure[2] + insecure[2] + nomatch[2])

	cs=cm.Greys([0.15,0.15, 0.15, 0.15])
	ax2.bar(labels, nomatch, width, label='No match',color=cs)
	
	cs=cm.Greys([0.55,0.55, 0.55, 0.55])
	ax2.bar(labels, secure, width, bottom=nomatch, label='Match (secure)', color=cs)
	
	cs=cm.Greys([0.35,0.35, 0.35, 0.35])
	ax2.bar(labels, insecure, width,bottom=[x+y for x,y in zip(nomatch,secure)], label='Match (insecure)',color=cs)


	#ax2.set_ylabel('% of domains or hosts')
	ax2.set_title('b) DNSSEC authenticity of \nunique hosts and domains.*')
	#pyplot.figtext(0.99, 0.01, 'footnote text', horizontalalignment='right') 
	pyplot.annotate('* Limited to the first measurement per domain.', (0,0), (0, -35), xycoords='axes fraction', textcoords='offset points', va='top')
	ax2.legend()

	
	for bar in ax2.patches:
		height = bar.get_height()
		width = bar.get_width()
		x = bar.get_x()
		y = bar.get_y()
		label_text = f"{format(round(height,2),'.2f')}%"
		label_x = x + width / 1.8
		label_y = y + height / 1.8
		ax2.text(label_x, label_y, label_text, ha='center',    
				va='center',rotation='vertical')

	#ax.set_xticklabels(labels,rotation='horizontal')

	pyplot.savefig(config.FIGURES_DIR + os.path.sep + "dnssec_barplot.pdf") # bbox_inches='tight'

	# tranco_auth = Counter({'OK': 124, 'NOT OK': 42})
	# tranco_unauth = Counter({'OK': 132, 'NOT OK': 82})
	# ctlogs_auth = Counter({'OK': 18282, 'NOT OK': 8668})
	# ctlogs_unauth = Counter({'NOT OK': 22943, 'OK': 22619})

	# ntranco_auth = sum(tranco_auth.values())
	# ntranco_unauth = sum(tranco_unauth.values())
	# nctlogs_auth = sum(ctlogs_auth.values())
	# nctlogs_unauth = sum(ctlogs_unauth.values())

	# labels = ['Tranco 1M: Secure', 'Tranco 1M: Insecure', 'CT Logs: Secure', 'CT Logs: Insecure']
	# matching = [tranco_auth["OK"]/ntranco_auth, tranco_unauth["OK"]/ntranco_unauth, ctlogs_auth["OK"]/nctlogs_auth, ctlogs_unauth["OK"]/nctlogs_unauth]
	# mismatching = [tranco_auth["NOT OK"]/ntranco_auth, tranco_unauth["NOT OK"]/ntranco_unauth, ctlogs_auth["NOT OK"]/nctlogs_auth, ctlogs_unauth["NOT OK"]/nctlogs_unauth]
	# width = 0.35       # the width of the bars: can also be len(x) sequence

	# pyplot.clf()
	# fig, ax = pyplot.subplots()


	# cs=cm.Greys([0.55,0.55, 0.55, 0.55])
	# ax.bar(labels, matching, width, label='Matching', color=cs)
	
	# cs=cm.Greys([0.35,0.35, 0.35, 0.35])
	# ax.bar(labels, mismatching, width,bottom=matching, label='Mismatching',color=cs)

	# ax.set_ylabel('\% of SSHFPs')
	# ax.set_title('DNSSEC authenticity of (mis-)matching SSHFP records.')
	# ax.legend()

	
	# for bar in ax.patches:
	# 	height = bar.get_height()
	# 	width = bar.get_width()
	# 	x = bar.get_x()
	# 	y = bar.get_y()
	# 	label_text = round(height,3)
	# 	label_x = x + width / 2
	# 	label_y = y + height / 2
	# 	ax.text(label_x, label_y, label_text, ha='center',    
	# 			va='center',rotation='vertical')

	# #ax.set_xticklabels(labels,rotation='horizontal')

	# pyplot.savefig(config.FIGURES_DIR + os.path.sep + "dnssec_barplot.pdf", bbox_inches='tight')