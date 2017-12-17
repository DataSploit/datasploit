import optparse
from domain_dnsrecords import fetch_dns_records,parse_dns_records
import requests
from termcolor import colored




parser = optparse.OptionParser()
parser.add_option('-e', '--email_file', action="store", dest="emailfile", help="File containing list of Email ids", default="spam")
parser.add_option('-s', '--subdomain_file', action="store", dest="subdomain_file", help="File containing list of subdomains.",	 default="spam")



class style:
   BOLD = '\033[1m'
   END = '\033[0m'

def run_active(filename,entity):
	counter = 0
	if entity == "subdomains":
		hosts_with_http_or_https = []
		might_be_vuln = []
		subdomain_list = []
		fh = open(filename, 'r')
		for y in fh.readlines():
			subdomain_list.append(y.strip("\n").strip("\r"))
		print colored(style.BOLD + "\n[+] Running Active Scan on " + str(len(subdomain_list)) + " subdomains" + style.END, 'green')
		print "\n"
		for x in subdomain_list:
			print x + ": ",
			recrd = fetch_dns_records(x,"CNAME") 
			print recrd
			if "No Records Found" not in recrd:
				try:
					req = requests.get("http://" + str(x), timeout=5)
					print colored("[+] HTTP - " + str(x) + ":\t" + str(req.status_code), 'green')
					#If response code is 404, might be a third party app without mapping
					if req.status_code == 404 or req.status_code == 403:
						might_be_vuln.append(["http", x, recrd, req.status_code])
					hosts_with_http_or_https.append("http://%s" % x)
				except:
					pass
				try:
					req = requests.get("https://" + str(x), timeout=5)
					print colored("[+] HTTPS - " + str(x) + ":\t" + str(req.status_code), 'green')
					#If response code is 404, might be a third party app without mapping
					if req.status_code == 404 or req.status_code == 403:
						might_be_vuln.append(["http", x])
					hosts_with_http_or_https.append("https://%s" % x)
				except:
					pass
			else:
				counter = counter + 1
		print colored(style.BOLD + "\n[+] No CNAME record found for " + str(counter) + " subdomains \n" + style.END, 'green')
		if len(might_be_vuln) != 0:
			print "Following subdomains are affected by Subdomain Take Over Vulnerability\n"
			for x in might_be_vuln:
				print x
		else:
			print "No subdomains are affected by Subdomain Take Over Vulnerability\n"

	elif entity == "emails":
		print "Work in Progress"


options, args = parser.parse_args()
emailfile = options.emailfile
subdomain_file = options.subdomain_file
if emailfile != 'spam':
	filename = emailfile
	run_active(filename, "emails")
elif subdomain_file != 'spam':
	filename = subdomain_file
	run_active(filename, "subdomains")
else:
	print 'Please pass filename'
