#!/usr/bin/env python

import time
import whois
import requests
import socket
import codecs
import sys
import json
from Wappalyzer import Wappalyzer, WebPage
from bs4 import BeautifulSoup
import dns.resolver
import config as cfg
import re
import csv
from urlparse import urlparse
import hashlib
import urllib
from pymongo import MongoClient
import clearbit
import time
import hashlib
from termcolor import colored
import signal
from json2html import *



reload(sys)
sys.setdefaultencoding("utf-8")





from domain_whois import whoisnew
from domain_dnsrecords import fetch_dns_records,parse_dns_records
from ip_shodan import shodansearch
from domain_zoomeye import get_accesstoken_zoomeye,search_zoomeye
from domain_checkpunkspider import checkpunkspider
from domain_wappalyzer import wappalyzeit
from domain_subdomains import check_and_append_subdomains,subdomains,find_subdomains_from_wolfram,subdomains_from_netcraft,subdomain_list
from domain_pagelinks import pagelinks
from domain_history import netcraft_domain_history
from domain_emailhunter import emailhunter,collected_emails
from domain_github import github_search
from domain_forumsearch import boardsearch_forumsearch
from domain_wikileaks import wikileaks
from domain_censys import view,censys_search,censys_list
from domain_shodan import shodandomainsearch
from email_fullcontact import fullcontact
from domain_pastes import google_search,colorize



import optparse
parser = optparse.OptionParser()
parser.add_option('-d', '--domain', action="store", dest="domain", help="Domain name against which automated Osint is to be performed.", default="spam")


'''
collected_emails = []
subdomain_list = []
censys_list = []
'''
######
##   Proram starts here  ##
######

dict_to_apend= {}
csv_dict = {}

'''
# Code for mongoDb
client = MongoClient()
db = client.database1
'''
allusernames_list = []


class style:
   BOLD = '\033[1m'
   END = '\033[0m'


def signal_handler(signal, frame):
	print colored(style.BOLD + '\n [-] Brrrr...You pressed Ctrl+c and this is sad. Trying to exit..\n' + style.END, 'red')
	sys.exit(0)
	quit()


def printart():
	print "\n\t  ____/ /____ _ / /_ ____ _ _____ ____   / /____  (_)/ /_"
	print "\t  / __  // __ `// __// __ `// ___// __ \ / // __ \ / // __/"
	print "\t / /_/ // /_/ // /_ / /_/ /(__  )/ /_/ // // /_/ // // /_  "
	print "\t \__,_/ \__,_/ \__/ \__,_//____// .___//_/ \____//_/ \__/  "
	print "\t                               /_/                        "
	print "\t\t\t\t\t\t"
	print "         	   Open Source Assistant for #OSINT            "
	print "                     website: www.datasploit.info               "
	print "\t"




def do_everything(domain):
	dict_to_apend['targetname'] = domain

	API_URL = "https://www.censys.io/api/v1"
	#print cfg.zoomeyeuser


	#print WhoIs information
	whoisdata = whoisnew(domain)
	print whoisdata
	dict_to_apend['whois'] = whoisdata



	#print DNS Information
	dns_records = parse_dns_records(domain)
	#dict_to_apend['dns_records'] = dns_records > not working
	#bson.errors.InvalidDocument: Cannot encode object: <DNS IN A rdata: 54.208.84.166>

	for x in dns_records.keys():
		print x
		if "No" in dns_records[x] and "Found" in dns_records[x]:
			print "\t%s" % (dns_records[x])
		else:
			for y in dns_records[x]:
				print "\t%s" % (y)
			#print type(dns_records[x])

	print colored(style.BOLD + '\n---> Finding Paste(s)..\n' + style.END, 'blue')
	if cfg.google_cse_key != "" and cfg.google_cse_key != "XYZ" and cfg.google_cse_cx != "" and cfg.google_cse_cx != "XYZ":
		total_results = google_search(domain, 1)
		if (total_results != 0 and total_results > 10):
			more_iters = (total_results / 10)
			if more_iters >= 10:
					print colored(style.BOLD + '\n---> Too many results, Daily API limit might exceed\n' + style.END, 'red')
			for x in xrange(1,more_iters + 1):
				google_search(domain, (x*10)+1)
		print "\n\n-----------------------------\n"
	else:
		print colored(style.BOLD + '\n[-] google_cse_key and google_cse_cx not configured. Skipping paste(s) search.\nPlease refer to http://datasploit.readthedocs.io/en/latest/apiGeneration/.\n' + style.END, 'red')


	#convert domain to reverse_domain for passing to checkpunkspider()
	reversed_domain = ""
	for x in reversed(domain.split(".")):
		reversed_domain = reversed_domain + "." + x
	reversed_domain = reversed_domain[1:]
	res = checkpunkspider(reversed_domain)
	if 'data' in res.keys() and len(res['data']) >= 1:
		dict_to_apend['punkspider'] = res['data']
		print colored("[+] Few vulnerabilities found at Punkspider", 'green'	)
		for x in res['data']:
			print "==> ", x['bugType']
			print "Method:", x['verb'].upper()
			print "URL:\n" + x['vulnerabilityUrl']
			print "Param:", x['parameter']
	else:
		print colored("[-] No Vulnerabilities found on PunkSpider", 'red')



	print colored(style.BOLD + '\n---> Wapplyzing web page of base domain:\n' + style.END, 'blue')


	wappalyze_results = {}
	#make proper URL with domain. Check on ssl as well as 80.
	print "Hitting HTTP:\n",
	try:
		targeturl = "http://" + domain
		list_of_techs = wappalyzeit(targeturl)
		wappalyze_results['http'] = list_of_techs
	except:
		print "[-] HTTP connection was unavailable"
		wappalyze_results['http'] = []
	print "\nHitting HTTPS:\n",
	try:
		targeturl = "https://" + domain
		list_of_techs = wappalyzeit(targeturl)
		wappalyze_results['https'] = list_of_techs
	except:
		print "[-] HTTPS connection was unavailable"
		wappalyze_results['https'] = []


	if len(wappalyze_results.keys()) >= 1:
		dict_to_apend['wappalyzer'] = wappalyze_results


	#make Search github code for the given domain.

	git_results = github_search(domain, 'Code')
	if git_results is not None:
		print git_results
	else:
		print colored("Sad! Nothing found on github", 'red')

	#collecting emails for the domain and adding information in master email list.
	if cfg.emailhunter != "":
		emails = emailhunter(domain)
		if len(collected_emails) >= 1:
			for x in collected_emails:
				print str(x)
			dict_to_apend['email_ids'] = collected_emails


	'''
	##### code for automated osint on enumerated email email_ids

	while True:
		a = raw_input(colored("\n\nDo you want to launch osint check for these emails? [(Y)es/(N)o/(S)pecificEmail]: ", 'red'))
		if a.lower() =="yes" or a.lower() == "y":
			for x in collected_emails:
				print "Checking for %s" % x
				print_emailosint(x)
			break
		elif a.lower() =="no" or a.lower() == "n":
			break
		elif a.lower() =="s":
			while True:
				b = raw_input("Please Enter the EmailId you want to tun OSINT.) [(C)ancel?]: ")
				if b.lower() =="c":
					break
				else:
					print_emailosint(b)
					break
			break

		else:
			print("[-] Wrong choice. Please enter Yes or No  [Y/N]: \n")
		#print emailOsint.username_list
	'''



	dns_ip_history = netcraft_domain_history(domain)
	if len(dns_ip_history.keys()) >= 1:
		for x in dns_ip_history.keys():
			print "%s: %s" % (dns_ip_history[x], x)
		dict_to_apend['domain_ip_history'] = dns_ip_history


	#subdomains [to be called before pagelinks so as to avoid repititions.]
	subdomains(domain)
	##print "---> Check_subdomains from wolframalpha"
	##find_subdomains_from_wolfram(domain)



	#domain pagelinks
	links=pagelinks(domain)
	if len(links) >= 1:
		for x in links:
			print x
		dict_to_apend['pagelinks'] = links


	#calling and printing subdomains after pagelinks.

	subdomains_from_netcraft(domain)
	print colored(style.BOLD + '---> Finding subdomains: \n' + style.END, 'blue')
	time.sleep(0.9)
	if len(subdomain_list) >= 1:
		for sub in subdomain_list:
			print sub
		dict_to_apend['subdomains'] = subdomain_list

	#wikileaks
	leaklinks=wikileaks(domain)
	for tl,lnk in leaklinks.items():
		print "%s (%s)" % (lnk, tl)
	if len(leaklinks.keys()) >= 1:
		dict_to_apend['wikileaks'] = leaklinks
	print "For all results, visit: "+ 'https://search.wikileaks.org/?query=&exact_phrase=%s&include_external_sources=True&order_by=newest_document_date'%(domain)



	links_brd =boardsearch_forumsearch(domain)
	for tl,lnk in links_brd.items():
		print "%s (%s)" % (lnk, tl)
	if len(links_brd.keys()) >= 1:
		dict_to_apend['forum_links'] = links_brd


	if cfg.zoomeyeuser != "" and cfg.zoomeyepass != "":
		temp_list =[]
		zoomeye_results = search_zoomeye(domain)
		dict_zoomeye_results = json.loads(zoomeye_results)
		if 'matches' in dict_zoomeye_results.keys():
			print len(dict_zoomeye_results['matches'])
			for x in dict_zoomeye_results['matches']:
				if x['site'].split('.')[-2] == domain.split('.')[-2]:
					temp_list.append(x)
					if 'title' in x.keys() :
						print "IP: %s\nSite: %s\nTitle: %s\nHeaders: %s\nLocation: %s\n" % (x['ip'], x['site'], x['title'], x['headers'].replace("\n",""), x['geoinfo'])
					else:
						for val in x.keys():
							print "%s: %s" % (val, x[val])
		if len(temp_list) >= 1:
			dict_to_apend['zoomeye'] = temp_list


	if cfg.censysio_id != "" and cfg.censysio_secret != "":
		print colored(style.BOLD + '\n---> Kicking off Censys Search. This may take a while..\n' + style.END, 'blue')
		censys_search(domain)
		if len(censys_list) >= 1:
			dict_to_apend['censys'] = censys_list
			for x in censys_list:
				if x is not None and x != 'None':
					print x


	if cfg.shodan_api != "":
		res_from_shodan = json.loads(shodandomainsearch(domain))
		if 'matches' in res_from_shodan.keys():
			dict_to_apend['shodan'] = res_from_shodan['matches']
			for x in res_from_shodan['matches']:
				print "IP: %s\nHosts: %s\nDomain: %s\nPort: %s\nData: %s\nLocation: %s\n" % (x['ip_str'], x['hostnames'], x['domains'], x['port'], x['data'].replace("\n",""), x['location'])


	'''
	#insert data into mongodb instance
	try:
		result = db.domaindata.insert(dict_to_apend, check_keys=False)
		print 'output saved to MongoDb'
	except:
		print "More data than I can handle, hence not saved in MongoDb. Apologies."
	'''





def main():
	signal.signal(signal.SIGINT, signal_handler)
        sys.stdout = codecs.getwriter('utf8')(sys.stdout)
        sys.stderr = codecs.getwriter('utf8')(sys.stderr)
	options, args = parser.parse_args()
	printart()
	domain = options.domain
	if domain == 'spam':
		print "[-] Invalid argument passed. \nUsage: domainOsint.py [options]\n\nOptions:\n  -h,\t\t--help\t\t\tshow this help message and exit\n  -d DOMAIN,\t--domain=DOMAIN\t\tDomain name against which automated Osint is to be performed."
	else:
		do_everything(domain)
		'''
		Since mongodb support is gone, dont need this snippet
		cursor = db.domaindata.find({"targetname": domain})
		if cursor.count() > 0:
			while True:
				a = raw_input(colored("Would you like to delete all the data for %s and launch a new scan? (Note: Deleting all data will disable alerting options.) [(Y)es/(N)o/(C)ancel]: ",'red') % domain,)
				if a.lower() =="yes" or a.lower() == "y":
					print colored("Deleting all data for %s...", 'blue') % domain
					result = db.domaindata.delete_many({"targetname": domain})
					print colored("Deleted %s document(s)", 'green') % result.deleted_count
					print colored("Launching new scan....\n",'blue')
					do_everything(domain)
					break
				elif a.lower() =="no" or a.lower() == "n":
					print colored("Note: This will create another entry for %s\n", 'red') % domain
					do_everything(domain)
					break
				elif a.lower() =="cancel" or a.lower() == "c":
					print colored("I lost the battle against your will. Quitting...", 'red')
					break
				else:
					print("[-] Wrong choice. Please enter Yes or No  [Y/N]: \n")
		else:
			print colored("No earlier scans found for %s, Launching fresh scan in 3, 2, 1..\n", 'blue') % domain
			do_everything(domain)
		'''

if __name__ == "__main__":
	main()


