#!/usr/bin/env python2

import base
import re
import sys
import requests
from termcolor import colored

# Control whether the module is enabled or not
ENABLED = True


class style:
    BOLD = '\033[1m'
    END = '\033[0m'


def banner():
    print colored(style.BOLD + '\n---> Searching Scribd Docs\n' + style.END, 'blue')


def main(email):
    req = requests.get('https://www.scribd.com/search?page=1&content_type=documents&query=%s' % (email))
    m = re.findall('(?<=https://www.scribd.com/doc/)\w+', req.text.encode('UTF-8'))
    m = set(m)
    m = list(m)
    links = []
    length = len(m)
    for lt in range(0, length - 1):
        links.append("https://www.scribd.com/doc/" + m[lt])
    return links


def output(data, email=""):
    if data:
        print "Found %s associated SCRIBD documents:\n" % len(data)
        for link in data:
            print link
        print ""
        print colored(style.BOLD + 'More results might be available, please follow this link:' + style.END)
        print "https://www.scribd.com/search?page=1&content_type=documents&query=" + email
    else:
        print colored('[-] No Associated Scribd Documents found.', 'red')


if __name__ == "__main__":
    try:
        email = sys.argv[1]
        banner()
        result = main(email)
        output(result, email)
    except Exception as e:
        print e
        print "Please provide an email as argument"

