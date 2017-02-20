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


def colorize(string):
	colourFormat = '\033[{0}m'
	colourStr = colourFormat.format(32)
	resetStr = colourFormat.format(0)
	lastMatch = 0
	formattedText = ''
	for match in re.finditer(r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+(\.[a-zA-Z]{2,4})|/(?:http:\/\/)?(?:([^.]+)\.)?datasploit\.info/|/(?:http:\/\/)?(?:([^.]+)\.)?(?:([^.]+)\.)?datasploit\.info/)', string):
	    start, end = match.span()
	    formattedText += string[lastMatch: start]
	    formattedText += colourStr
	    formattedText += string[start: end]
	    formattedText += resetStr
	    lastMatch = end
	formattedText += string[lastMatch:]
	return formattedText

def google_search(domain,start_index):
	time.sleep(0.3)
	url="https://www.googleapis.com/customsearch/v1?key=%s&cx=%s&q=\"%s\"&start=%s" % (cfg.google_cse_key, cfg.google_cse_cx, domain, start_index)
	res=requests.get(url)
	results = json.loads(res.text)
	if 'items' in results.keys():
		if start_index == 1:
			print "[+] %s results found\n" % int(results['searchInformation']['totalResults'])
		for x in results['items']:
			print "Title: %s\nURL: %s\nSnippet: %s\n" % (x['title'], colorize(x['link']), colorize(x['snippet']))
			start_index = +1
		return int(results['searchInformation']['totalResults'])
        #searchInformation isn't guaranteed to be in results
	elif 'searchInformation' in results and results['searchInformation']['totalResults'] == "0":
			print '0 Results found'
			return 0
	elif results['error']['code'] == 403:
		print 'Rate limit Exceeded'
		return 0
	else:
		return 0
	#return json.loads(res.text)


def main():
	domain = sys.argv[1]
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

if __name__ == "__main__":
	main()

