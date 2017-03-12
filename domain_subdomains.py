#!/usr/bin/env python

import sys
import json
import requests
from bs4 import BeautifulSoup
import re
from domain_pagelinks import pagelinks
import config as cfg
import hashlib
from urlparse import urlparse
import urllib
from termcolor import colored
import time


class style:
   BOLD = '\033[1m'
   END = '\033[0m'

subdomain_list = []


def check_and_append_subdomains(subdomain):
	if subdomain not in subdomain_list:
		subdomain_list.append(subdomain)


def subdomains(domain):
	r = requests.get("https://dnsdumpster.com/")
	cookies = {}
	if 'csrftoken' in r.cookies.keys():
		cookies['csrftoken'] = r.cookies['csrftoken']
		data = {}
		data['csrfmiddlewaretoken'] = cookies['csrftoken']
		data['targetip'] = domain
		headers = {}
		headers['Referer'] = "https://dnsdumpster.com/"
		req = requests.post("https://dnsdumpster.com/", data = data, cookies = cookies, headers = headers)
		#print req.content
		soup =  BeautifulSoup(req.content.encode('utf-8'), 'lxml')

		subdomains=soup.findAll('td',{"class":"col-md-4"})
		for subd in subdomains:
			if domain in subd.text:
				#print subd.text.split()[0]
				check_and_append_subdomains(subd.text.split()[0])
			else:
				pass


def find_subdomains_from_wolfram(domain):

	'''
	Code is not working as of now, need some modifications.

	'''
	req = requests.get("http://www.wolframalpha.com/input/api/v1/code?ts=%s" % (str(time.time()).split(".")[0]))
	code = json.loads(req.content)['code']


	proxies = {
	  'http': 'http://127.0.0.1:8080',
	  'https': 'http://127.0.0.1:8080'
	}

	headers = {}
	headers['User-Agent'] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:45.0) Gecko/20100101 Firefox/45.0"
	headers['Accept'] = "application/json, text/plain, */*"
	headers['Referer'] = "http://www.wolframalpha.com/input/?i=%s" % (domain)

	#second request to get recalculate_code
	req1 = requests.get("http://www.wolframalpha.com/input/json.jsp?async=true&banners=raw&debuggingdata=false&fbtoken=&format=image,plaintext,imagemap,sound,minput,moutput&formattimeout=8&input=%s&output=JSON&parsetimeout=5&proxycode=%s&scantimeout=0.5&sponsorcategories=true&statemethod=deploybutton&storesubpodexprs=true" % (domain, code), headers=headers, proxies=proxies)
	recalculate = json.loads(req1.content)['queryresult']['recalculate']

	if recalculate != "":
		recalc_code = json.loads(req1.content)['queryresult']['recalculate'].split("=")[1].split("&")[0]

		#third request to get calc_id
		#print "http://www.wolframalpha.com/input/json.jsp?action=recalc&format=image,plaintext,imagemap,minput,moutput&id=%s&output=JSON&output=JSON&scantimeout=10&statemethod=deploybutton&storesubpodexprs=true" % (recalc_code)
		req2 = requests.get("http://www.wolframalpha.com/input/json.jsp?action=recalc&format=image,plaintext,imagemap,minput,moutput&id=%s&output=JSON&output=JSON&scantimeout=10&statemethod=deploybutton&storesubpodexprs=true" % (recalc_code), headers=headers, proxies=proxies)
		pods = json.loads(req2.content)['queryresult']['pods']
		for x in pods:
			if "Web statistics for" in x['title']:
				async_code =  x['async'].split('=')[1]

		#fourth request to get id for subdomains.
		req3 = requests.get("http://www.wolframalpha.com/input/json.jsp?action=asyncPod&format=image,plaintext,imagemap,minput,moutput&formattimeout=20&id=%s&output=JSON&podtimeout=20&statemethod=deploybutton&storesubpodexprs=true" % (async_code), headers=headers, proxies=proxies)
		for x in json.loads(req3.content)['pods'][0]['deploybuttonstates']:
			if x['name'] == "Subdomains":
				server_value = json.loads(req3.content)['pods'][0]['server']
				sub_code = x['input']
			else:
				pass

		#fifth request to find few subdomains
		url = "http://www.wolframalpha.com/input/json.jsp?async=false&dbid=%s&format=image,plaintext,imagemap,sound,minput,moutput&includepodid=WebSiteStatisticsPod:InternetData&input=%s&output=JSON&podTitle=Web+statistics+for+all+of+%s&podstate=%s&s=%s&statemethod=deploybutton&storesubpodexprs=true&text=Subdomains" % (sub_code, domain, domain, sub_code, server_value)
		req4 = requests.get(url, headers = headers, proxies = proxies)
		servervalue_for_more = json.loads(req4.content)['queryresult']['server']
		print servervalue_for_more
		for x in json.loads(req4.content)['queryresult']['pods']:
			for y in x['subpods']:
				if y['title'] == "Subdomains":
					temp_subdomain_list = y['plaintext'].split("\n")
					del temp_subdomain_list[0]
					for x in temp_subdomain_list:
						check_and_append_subdomains(x.split('|')[0].strip(" "))
					more_code = y['deploybuttonstates'][0]['input']
				else:
					more_code = "blank_bro"

		#wooh, final request bitch.
		url = "http://www.wolframalpha.com/input/json.jsp?async=false&dbid=%s&format=image,plaintext,imagemap,sound,minput,moutput&includepodid=WebSiteStatisticsPod:InternetData&input=%s&output=JSON&podTitile=Subdomains&podstate=%s&s=%s&statemethod=deploybutton&storesubpodexprs=true&text=More" % (more_code, domain, more_code, servervalue_for_more)
		req5 = requests.get(url, headers = headers, proxies = proxies)
		for x in json.loads(req5.content)['queryresult']['subpods']:
			if x['title'] == "Subdomains":
				temp_subdomain_list = x['plaintext'].split("\n")
				del temp_subdomain_list[0]
				for y in temp_subdomain_list:
					check_and_append_subdomains(y.split('|')[0].strip(" "))

	else:
		print "Empty Recalculate, Cannot Proceed sire."



#def netcraft_makecookies(cookie):
	cookies = dict()
	cookies_list = cookie[0:cookie.find(';')].split("=")
	cookies[cookies_list[0]] = cookies_list[1]
	cookies['netcraft_js_verification_response'] = hashlib.sha1(urllib.unquote(cookies_list[1])).hexdigest()
	return cookies

def subdomains_from_netcraft(domain):
	target_dom_name = domain.split(".")
	#url = "http://searchdns.netcraft.com/?restriction=site+ends+with&host=%s" % (domain)
	#req = requests.get(url)
	#cookies = netcraft_makecookies(req.headers['set-cookie'])
	#req1 = requests.get("http://searchdns.netcraft.com/?host=%s" % (domain), cookies = cookies)
	req1 = requests.get("http://searchdns.netcraft.com/?host=%s" % (domain))
	link_regx = re.compile('<a href="http://toolbar.netcraft.com/site_report\?url=(.*)">')
	links_list = link_regx.findall(req1.content)
	for x in links_list:
		dom_name = x.split("/")[2].split(".")
		if (dom_name[len(dom_name) - 1] == target_dom_name[1]) and (dom_name[len(dom_name) - 2] == target_dom_name[0]):
			check_and_append_subdomains(x.split("/")[2])
	num_regex = re.compile('Found (.*) site')
	num_subdomains = num_regex.findall(req1.content)
	if num_subdomains :
		num_regex = re.compile('First (.*) sites returned')
		num_subdomains = num_regex.findall(req1.content)
	if num_subdomains and num_subdomains[0] != str(0):
		num_pages = int(num_subdomains[0])/20+1
		if num_pages > 1:
			last_regex = re.compile('<td align="left">%s.</td><td align="left">\n<a href="(.*)" rel="nofollow">' % (20))
			last_item = last_regex.findall(req1.content)[0].split("/")[2]
			next_page = 21

			for x in range(2,num_pages):
				url  = "http://searchdns.netcraft.com/?host=%s&last=%s&from=%s&restriction=site%%20contains" % (domain, last_item, next_page)
				req2 = requests.get(url)
				link_regx = re.compile('<a href="http://toolbar.netcraft.com/site_report\?url=(.*)">')
				links_list = link_regx.findall(req2.content)
				for y in links_list:
					dom_name1 = y.split("/")[2].split(".")
					if (dom_name1[len(dom_name1) - 1] == target_dom_name[1]) and (dom_name1[len(dom_name1) - 2] == target_dom_name[0]):
						check_and_append_subdomains(y.split("/")[2])
				last_item = links_list[len(links_list) - 1].split("/")[2]
				next_page = 20 * x + 1
				#print last_item
				#print next_page
	else:
		print colored('zero subdomains found here', 'red')







def main():
	domain = sys.argv[1]
	#subdomains [to be called before pagelinks so as to avoid repititions.]
	print colored(style.BOLD + '---> Finding subdomains, will be back soon with list. \n' + style.END, 'blue')
	time.sleep(0.3)
	subdomains(domain)
	##print "\t\t\t[+] Check_subdomains from wolframalpha"
	##find_subdomains_from_wolfram(domain)
	#pagelinks_list = pagelinks(domain)

	subdomains_from_netcraft(domain)

	#printing all subdomains
	print colored("List of subdomains found\n", 'green')
	for sub in subdomain_list:
		print sub



if __name__ == "__main__":
	main()









