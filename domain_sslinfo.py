import sys
import json
import requests
from bs4 import BeautifulSoup
import re
from termcolor import colored
class style:
   BOLD = '\033[1m'
   END = '\033[0m'

def check_ssl_htbsecurity(domain):
	headers = {}
	headers['Content-Type'] = "application/x-www-form-urlencoded"
	data='domain=%s&dnsr=off&recheck=false' % domain
	req = requests.post('https://www.htbridge.com/ssl/chssl/1451425590.html', headers=headers , data=data)
	if req.content:
		results = json.loads(req.content)
		return results
	else:
		return "Empty JSON"

def main():
	domain = sys.argv[1]
	results = check_ssl_htbsecurity(domain)
	if 'ERROR' in results.keys():
		print results['ERROR']
	elif 'TOKEN' in results.keys():
		print colored('Picking up One IP from bunch of IPs returned: %s', 'blue') % results['MULTIPLE_IPS'][0]
		results_new = check_ssl_htbsecurity(results['MULTIPLE_IPS'][0])
		print "OverAll Rating: %s" % results_new['GRADE']
		print 'Check https://www.htbridge.com/ssl/ for more information'
		for x in results_new['VALUE'].keys():
			if str("[5]") in str(results_new['VALUE'][x]) or str("[3]") in str(results_new['VALUE'][x]):
				if x == 'httpHeaders':
					pass
				else:
					print results_new['VALUE'][x]
	else:
		print "OverAll Rating: %s" % results['GRADE']
		for x in results['VALUE'].keys():
			if str("[5]") in str(results['VALUE'][x]) or str("[3]") in str(results['VALUE'][x]):
				if x == 'httpHeaders':
					pass
				else:
					print results['VALUE'][x]

if __name__ == "__main__":
	main()
