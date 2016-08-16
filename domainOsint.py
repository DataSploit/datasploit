#input domain name

#domain_osint

#pip lxml json 

#http://searchdns.netcraft.com/?restriction=site+contains&host=olacabs.com&lookup=wait..&position=limited

#completed

#punkspider, shodan, whois,

#show whois , dns, buildwith, wappalyzer, punkspider info
	#	subdomain find. knocy.py / google 
	#	server profiling of subdomains
	#	check for .git/htaccess/web.config/extractc.

#https://github.com/ivanlei/threatbutt
#	harvest emails
#	find files
#	extract info from files 
#	find information, harvest email. 
#	check on fb, relate to username. 
#	show possible graph search links
#	twiter graph on the username
#	namecheck with usernamejjjj
#	hibp

import time
import whois
import requests
import socket
import sys	
import json
from Wappalyzer import Wappalyzer, WebPage
from bs4 import BeautifulSoup
import dns.resolver
import config as cfg
import re
from urlparse import urlparse
import hashlib
import urllib
from pymongo import MongoClient
import clearbit
import time
import hashlib
import config
from termcolor import colored

reload(sys)
sys.setdefaultencoding("utf-8")




from domain_whois import whoisnew
from domain_dnsrecords import fetch_dns_records,parse_dns_records
from ip_shodan import shodansearch
from domain_zoomeye import get_accesstoken_zoomeye,search_zoomeye
from domain_checkpunkspider import checkpunkspider
from domain_wappalyzer import wappalyzeit
from domain_subdomains import check_and_append_subdomains,subdomains,find_subdomains_from_wolfram,subdomains_from_netcraft,subdomain_list
from domain_sslinfo import check_ssl_htbsecurity
from domain_pagelinks import pagelinks
from domain_history import netcraft_domain_history
from domain_emailhunter import emailhunter,collected_emails
from domain_github import github_search
from domain_forumsearch import boardsearch_forumsearch
from domain_wikileaks import wikileaks
from domain_censys import view,censys_search,censys_list
from domain_shodan import shodandomainsearch
from email_fullcontact import fullcontact
from emailOsint import print_emailosint



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
client = MongoClient(config.mongo_uri)
db = client.database1

allusernames_list = []


class style:
   BOLD = '\033[1m'
   END = '\033[0m'

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



	#make proper URL with domain. Check on ssl as well as 80.
	#print "---> Wapplyzing " + domain 
	print colored(style.BOLD + '\n---> Wappalyzing web pages\n' + style.END, 'blue')
	time.sleep(0.3)
	print colored("->Trying Wapalyzer on HTTP: ", 'blue')
	wappalyze_results = {}
	try:
		targeturl = "http://" + domain
		list_of_techs = wappalyzeit(targeturl)
		if len(list_of_techs) >= 1:
			wappalyze_results['http'] = list_of_techs
			for abc in list_of_techs:
				print abc,
		else:
			pass
		print "\n"
	except:	
		print colored("[-] HTTP connection was unavailable", 'red')
	
	print colored("->Trying Wapalyzer on HTTPS: ", 'blue')
	try:
		targeturl = "https://" + domain
		list_of_techs = wappalyzeit(targeturl)
		if len(list_of_techs) >= 1:
			wappalyze_results['https'] = list_of_techs
			for abc in list_of_techs:
				print abc,
		else:
			pass
		print "\n"
	except:
		print colored("[-] HTTP connection was unavailable", 'red')
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
				print str(x) + ", ",
			dict_to_apend['email_ids'] = collected_emails

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

	
	print colored(style.BOLD + '\n---> Performing passive SSL Scan\n' + style.END, 'blue')
	results = check_ssl_htbsecurity(domain)
	htb_res_dict = {}
	htb_res_lists = []
	if 'ERROR' in results.keys():
		print results['ERROR']
	elif 'TOKEN' in results.keys():
		if 'MULTIPLE_IPS' in results.keys():
			print colored('Picking up One IP from bunch of IPs returned: %s', 'green') % results['MULTIPLE_IPS'][0]
			results_new = check_ssl_htbsecurity(results['MULTIPLE_IPS'][0])
			print "OverAll Rating: %s" % results_new['GRADE']
			htb_res_dict['rating'] = results_new['GRADE']
			print 'Check https://www.htbridge.com/ssl/ for more information'
			for x in results_new['VALUE'].keys():
				if str("[5]") in str(results_new['VALUE'][x]) or str("[3]") in str(results_new['VALUE'][x]):
					if x == 'httpHeaders':
						pass
					else:
						print results_new['VALUE'][x]
						htb_res_lists.append(results_new['VALUE'][x])
	else:
		print "OverAll Rating: %s" % results['GRADE']
		htb_res_dict['rating'] = results['GRADE']
		for x in results['VALUE'].keys():
			if str("[5]") in str(results['VALUE'][x]) or str("[3]") in str(results['VALUE'][x]):
				if x == 'httpHeaders':
					pass
				else:
					print results['VALUE'][x]
					htb_res_lists.append(results['VALUE'][x])
	htb_res_dict['issues'] = htb_res_lists
	dict_to_apend['ssl_scan'] = htb_res_dict

	
	
	#checks results from zoomeye
	#filters need to be applied
	#zoomeye_results = search_zoomeye(domain)
	#dict_zoomeye_results = json.loads(zoomeye_results)
	#if 'matches' in dict_zoomeye_results.keys():
	#	for x in dict_zoomeye_results['matches']:
	#		if x['site'].split('.')[-2] == domain.split('.')[-2]:
	#			print "IP: %s\nSite: %s\nTitle: %s\nHeaders: %s\nLocation: %s\n" % (x['ip'], x['site'], x['title'], x['headers'].replace("\n",""), x['geoinfo'])
	#print "\n-----------------------------\n"

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


	
	#Code for shodan Ip search. now we are doing Hostname search.
		
		#converts domain to IP. Prints a statement for the same.
		#ip_addr = socket.gethostbyname(domain)

		#checks for information at shodan, and comes back with whatever available.
		## need to apply filter here (lot of noise coming in)
		#res_from_shodan = json.loads(shodansearch(ip_addr))
		#print res_from_shodan
		#for iterate_shodan_list in res_from_shodan['data']:
		#	print "ISP: %s \n Hosts: %s \n IP: %s \n Data: %s\n" % (iterate_shodan_list['isp'], iterate_shodan_list['hostnames'], iterate_shodan_list['ip_str'], iterate_shodan_list['data'].strip("\n"))
		#print "\n-----------------------------\n"
	

	
	if cfg.shodan_api != "":
		res_from_shodan = json.loads(shodandomainsearch(domain))
		if 'matches' in res_from_shodan.keys():
			dict_to_apend['shodan'] = res_from_shodan['matches']
			for x in res_from_shodan['matches']:
				print "IP: %s\nHosts: %s\nDomain: %s\nPort: %s\nData: %s\nLocation: %s\n" % (x['ip_str'], x['hostnames'], x['domains'], x['port'], x['data'].replace("\n",""), x['location'])


	#insert data into mongodb instance

	result = db.domaindata.insert(dict_to_apend, check_keys=False)
	print 'done'





def main(): 
	options, args = parser.parse_args()
	printart()
	domain = options.domain
	if domain == 'spam':
		print "[-] Invalid argument passed. \nUsage: domainOsint.py [options]\n\nOptions:\n  -h,\t\t--help\t\t\tshow this help message and exit\n  -d DOMAIN,\t--domain=DOMAIN\t\tDomain name against which automated Osint is to be performed."
	else:
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
			

if __name__ == "__main__":
	main()


