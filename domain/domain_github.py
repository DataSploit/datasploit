#!/usr/bin/env python

import base
import config as cfg
import sys
import json
import requests
from termcolor import colored

ENABLED = True

class style:
    BOLD = '\033[1m'
    END = '\033[0m'

def github_search(query):
    endpoint_git = "https://api.github.com/search/code?q=%s&access_token=%s" % (query, cfg.github_access_token)
    req = requests.get(endpoint_git)
    data = json.loads(req.content)
    print data
    if data['message'] == 'Bad credentials':
        return None, 'Error'
    else:
        return data['total_count'], data['items']

def banner():
    print colored(style.BOLD + '\n---> Searching Github for domain results\n' + style.END, 'blue')

def output(data, domain=""):
    if data[1] == 'Error':
        print colored('Authentication failed. Check Github API key in config.py.\n', 'red')
    elif not data[0]:
        print colored("Sad! Nothing found on github", 'red')
    else:
        print colored("[+] Found %s results on github." % data[0], 'green')
        if data[0] >= 30:
            print "Top 30 results shown below"
        else:
            print "Top %s results shown below" % data[0]
        count = 1
        for snip in data[1]:
            print "%s. File: %s" % (str(count).zfill(2), snip['html_url'])
            print "    Owner: %s" % snip['repository']['full_name']
            print "    Repository: %s" % snip['repository']['html_url']
            count += 1
    print "\nCheck results here: https://github.com/search?q=%s&type=Code&utf8=%%E2%%9C%%93" % domain
    print "-----------------------------\n"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        domain = sys.argv[1]
    else:
        print "Please provide a domain name as argument"
        sys.exit(0)
    try:
        banner()
        count, result = github_search(domain)
        output([count, result], domain)
    except Exception as e:
        print e
