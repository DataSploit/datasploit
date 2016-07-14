import requests
import sys
import json
import warnings

warnings.filterwarnings("ignore")

def checkpunkspider(reversed_domain):
	print "\t\t\t[+] Checking PunkSpider" 
	req= requests.post("http://www.punkspider.org/service/search/detail/" + reversed_domain, verify=False)
	return json.loads(req.content)



def main():
	domain = sys.argv[1]
	#convert domain to reverse_domain for passing to checkpunkspider()
	reversed_domain = ""
	for x in reversed(domain.split(".")):
		reversed_domain = reversed_domain + "." + x
	reversed_domain = reversed_domain[1:]
	res = checkpunkspider(reversed_domain)
	if res is not None:
		if 'data' in res.keys() and len(res['data']) >= 1:
			print "[+] Few vulnerabilities found at Punkspider"
			for x in res['data']:
				print "==> ", x['bugType']
				print "Method:", x['verb'].upper()
				print "URL:\n" + x['vulnerabilityUrl']
				print "Param:", x['parameter']
		else:
			print "[-] No Vulnerabilities found on PunkSpider"
		print "\n-----------------------------\n"

if __name__ == "__main__":
	main()
