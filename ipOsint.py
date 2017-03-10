#!/usr/bin/env python

import requests
import sys
import config as cfg
import clearbit
import json
import time
import hashlib
from bs4 import BeautifulSoup
import re
from termcolor import colored
from ip_whois import ip_whois
from ip_shodan import domaintoip,shodansearch


class style:
   BOLD = '\033[1m'
   END = '\033[0m'


ip_addr = sys.argv[1]

	
def print_iposint(ip_addr):
	ip_whois(ip_addr)
	#print res_from_shodan
	print colored(style.BOLD + '-----------------------------------------' + style.END, 'blue')

	shodansearch(ip_addr)
	#print res_from_shodan
	print colored(style.BOLD + '-----------------------------------' + style.END, 'blue')


def main():
	print_iposint(ip_addr)
	
if __name__ == "__main__":
	main()

