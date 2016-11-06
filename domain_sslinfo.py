import sys
import json
import requests 
from bs4 import BeautifulSoup
import re
from termcolor import colored
import time

class style:
   BOLD = '\033[1m'
   END = '\033[0m'

def check_ssl_htbsecurity(domain, token='', ip=''):
	global timestamp
	headers = {}
	headers['Content-Type'] = "application/x-www-form-urlencoded"
	if token == '':
		data='domain=%s&show_test_results=true&recheck=false&verbosity=1' % domain
		url = 'https://www.htbridge.com/ssl/api/v1/check/' + str(timestamp) + '.html'
		req = requests.post(url, headers=headers , data=data, verify=False)
		results = json.loads(req.content)
		return results
	else:
		data='domain=' + str(domain) + '&show_test_results=true&recheck=false&choosen_ip=' + str(ip) + '&verbosity=1&token=' + str(token)
		url = 'https://www.htbridge.com/ssl/api/v1/check/' + str(timestamp) + '.html'
		req = requests.post(url, headers=headers , data=data, verify=False)
		results = json.loads(req.content)
		return results

def main():
	domain = sys.argv[1]
	results = check_ssl_htbsecurity(domain)
	if 'error' in results.keys():
		print results['error']
	elif 'token' in results.keys():
		print colored('Picking up One IP from bunch of IPs returned: %s', 'blue') % results['MULTIPLE_IPS'][0]
		token = results['token']
		results_new = check_ssl_htbsecurity(domain, token, results['multiple_ips'][0])
		print "OverAll Rating: %s" % results_new['results']['grade']
		print 'Check https://www.htbridge.com/ssl/ for more information'

#Added unix timestamp instead of using the same time stamp given in the example. This is done to prevent caching on client side. For more details refer: https://www.htbridge.com/ssl/#api

if __name__ == "__main__":
	global timestamp;
	timestamp = int(time.time())
	main()

