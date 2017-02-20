from bs4 import BeautifulSoup
import sys
import urllib2
import re
import string
from celery import shared_task

from osint.utils import *

'''
This code is a bit messed up. Lists files from first page only. Needs a lot of modification.

'''

def googlesearch(query, ext):
	print query
	try:
		google="https://www.google.co.in/search?filter=0&q=site:"
		getrequrl="https://www.google.co.in/search?filter=0&num=100&q=%s&start=" % (query)
		hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
	       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
	       'Accept-Encoding': 'none',
	       'Accept-Language': 'en-US,en;q=0.8',
	       'Connection': 'keep-alive'}
		req=urllib2.Request(getrequrl, headers=hdr)
		response=urllib2.urlopen(req)
                encoding = response.headers.getparam('charset')
		data = response.read().encode(encoding)
		data=re.sub('<b>','',data)
		for e in ('>','=','<','\\','(',')','"','http',':','//'):
			data = string.replace(data,e,' ')

		r1 = re.compile('[-_.a-zA-Z0-9.-_]*'+'\.'+ ext)
		res = r1.findall(data)
		if not res:
			print "No results were found"
			return []
		else:
			return res
	except:
		return []

@shared_task
def run(domain, taskId):
	list_ext = ["pdf", "xls", "docx"]
	data = {}
        for x in list_ext:
                query  = "site:%s+filetype:%s" % (domain, x)
                results = googlesearch(query, x)
		data[x] = list(set(results))
	save_record(domain, taskId, "Google Search", data)
	return data

if __name__ == "__main__":
	domain=sys.argv[1]
	print "\t\t\t[+] PDF Files\n"

	result = run(domain)
	print result
	for i, x in result.iteritems():
		x= re.sub('<li class="first">','',x)
		x= re.sub('</li>','',x)
		print x
		print "\n"
		print "====================\n"
