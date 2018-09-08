#!/usr/bin/env python2

import base
import vault
import sys
import requests
import cfscrape
from termcolor import colored
import json

class style:
    BOLD = '\033[1m'
    END = '\033[0m'

# Control whether the module is enabled or not
ENABLED = False


def banner():
     print colored(style.BOLD + '\n---> Searching Email in DarkNet\n' + style.END, 'blue')


def main(email):
    req = requests.get("https://hacked-emails.com/api?q=%s" % email)
    if "jschl-answer" in req.text:
	print "Cloudflare detected... Solving challenge."
	scraper = cfscrape.create_scraper()
	req = scraper.get("https://hacked-emails.com/api?q=%s" % email)
	print req.text
	if "jschl-answer" in req.text:
		return {}
    data = json.loads(req.text.encode('UTF-8'))
    return data



def output(data, email=""):
    # Use the data variable to print out to console as you like
    if data.get('status') == 'found':
        print "%s Results found" % data.get('results')
        for rec in data.get('data'):
            print "------"
            print colored(style.BOLD + 'Leak Title: ' + style.END) + str(rec.get('title'))
            print colored(style.BOLD + 'Details: ' + style.END) + str(rec.get('details'))
            if rec.get('source_url') == "#":
                rec['source_url'] = "N/A"
            print colored(style.BOLD + 'Leak URL: ' + style.END) + str(rec.get('source_url'))
            print colored(style.BOLD + 'Leaked on: ' + style.END) + str(rec.get('date_created'))
            if rec.get('source_provider') == 'anon':
                rec['source_provider'] = "Anonymous"
            print colored(style.BOLD + 'Source: ' + style.END) + str(rec.get('source_provider'))
    else:
        print "[-] No Data Found"




if __name__ == "__main__":
    try:
        email = sys.argv[1]
        banner()
        result = main(email)
        output(result, email)
    except Exception as e:
        print e
        print "Please provide an email as argument"
