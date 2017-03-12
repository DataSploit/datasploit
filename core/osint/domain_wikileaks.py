import requests
from bs4 import BeautifulSoup
import sys
import json
from celery import shared_task
from osint.utils import *

@shared_task
def wikileaks(domain, taskId):
	req = requests.get('https://search.wikileaks.org/?query=&exact_phrase=%s&include_external_sources=True&order_by=newest_document_date'%(domain))
	soup=BeautifulSoup(req.content, "lxml")
	count=soup.findAll('div',{"class":"total-count"})
	print "Total "+count[0].text.encode('utf-8')
	divtag=soup.findAll('div',{'class':'result'})
	links={}
	for a in divtag:
		links[a.a.text.encode('utf-8')]=a.a['href']
	save_record(domain, taskId, "WikiLeaks", links)
	return links


def main():
	domain = sys.argv[1]
	#wikileaks
	print "\t\t\t[+] Associated WikiLeaks\n"
	leaklinks=wikileaks(domain)
	for tl,lnk in leaklinks.items():
		print "%s (%s)" % (lnk, tl)
	print "For all results, visit: "+ 'https://search.wikileaks.org/?query=&exact_phrase=%s&include_external_sources=True&order_by=newest_document_date'%(domain)
	print "\n-----------------------------\n"



#if __name__ == "__main__":
	#main()
