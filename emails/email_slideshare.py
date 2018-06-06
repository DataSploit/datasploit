#!/usr/bin/env python

import base
import sys
import requests
from bs4 import BeautifulSoup
from termcolor import colored

# Control whether the module is enabled or not
ENABLED = True


class style:
    BOLD = '\033[1m'
    END = '\033[0m'


def banner():
    print colored(style.BOLD + '\n---> Searching Slideshare\n' + style.END, 'blue')


def main(email):
    slides = {}
    try:
        req = requests.get('http://www.slideshare.net/search/slideshow?q=%s' % (email))
        soup = BeautifulSoup(req.content, "lxml")
        atag = soup.findAll('a', {'class': 'title title-link antialiased j-slideshow-title'})
        for at in atag:
            slides[at.text] = at['href']
    except Exception as ex:
        print ex
    return slides


def output(data, email=""):
    if data:
        print "Found %s published slides\n" % len(data)
        for tl, lnk in data.items():
            print str(tl).strip() + " : http://www.slideshare.net" + str(lnk).strip()
    else:
        print colored('[-] No Associated Slides found.', 'red')


if __name__ == "__main__":
    try:
        email = sys.argv[1]
        banner()
        result = main(email)
        output(result, email)
    except Exception as e:
        print e
        print "Please provide an email as argument"
