#!/usr/bin/env python

import config as cfg
import requests
import json
import sys
import time
import re
from termcolor import colored
class style:
   BOLD = '\033[1m'
   END = '\033[0m'



def basic_checks(email):
	if re.match('[^@]+@[^@]+\.[^@]+', email):
		print colored(style.BOLD + '\n---> Basic Email Check(s)..\n' + style.END, 'blue')
		if cfg.mailboxlayer_api != "" and cfg.mailboxlayer_api != "XYZ" and cfg.mailboxlayer_api != "" and cfg.mailboxlayer_api != "XYZ":
			url = "http://apilayer.net/api/check?access_key=%s&email=%s&smtp=1&format=1" % (cfg.mailboxlayer_api, email)
			req = requests.get(url)
			resp = json.loads(req.text)
			print "Is it a free Email Address?:", 
			if resp['free'] == False:
				print "No"
			else:
				print "Yes"
			print "Email ID Exist?: ",
			if resp['smtp_check'] == True:
				print "Yes"
			else:
				print "No"
			print "Can this domain recieve emails?: ",
			if resp['mx_found'] == True:
				print "Yes"
			else:
				print "No"
			print "Is it a Disposable email?: ",
			if resp['disposable'] == True:
				print "Yes"
			else:
				print "No"
			print "\n"
	else:
		print colored(style.BOLD + '\n[-] Please pass a valid email ID.\n' + style.END, 'red')

def main():
	email = sys.argv[1]
	basic_checks(email)
	







	'''
	print colored(style.BOLD + '\n---> Basic Email Check(s)..\n' + style.END, 'blue')
	if cfg.mailboxlayer_api != "" and cfg.mailboxlayer_api != "XYZ" and cfg.mailboxlayer_api != "" and cfg.mailboxlayer_api != "XYZ":
		total_results = google_search(email, 1)
		if (total_results != 0 and total_results > 10):
			more_iters = (total_results / 10)
			if more_iters >= 10:
					print colored(style.BOLD + '\n---> Too many results, Daily API limit might exceed\n' + style.END, 'red')
			for x in xrange(1,more_iters + 1):	
				google_search(email, (x*10)+1)
		print "\n\n-----------------------------\n"
	else:
		print colored(style.BOLD + '\n[-] google_cse_key and google_cse_cx not configured. Skipping paste(s) search.\nPlease refer to http://datasploit.readthedocs.io/en/latest/apiGeneration/.\n' + style.END, 'red')
	'''


if __name__ == "__main__":
	main()

