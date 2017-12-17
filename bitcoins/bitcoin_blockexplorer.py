#!/usr/bin/env python

import base
import config as cfg
import sys
from termcolor import colored
import requests

# Control whether the module is enabled or not
ENABLED = True

class style:
    BOLD = '\033[1m'
    END = '\033[0m'

def validate(bitcoin_address):
    r = requests.get("https://blockexplorer.com/api/addr-validate/" + bitcoin_address)
    return r.content

def get_data(bitcoin_address, url):
    block_explorer_url_full = "https://blockexplorer.com/api/addr/" + bitcoin_address + url
    res = requests.get(block_explorer_url_full)
    # Status 400 - Some internal error "Bitcoin JSON-RPC: Work queue depth exceeded. Code:429"
    # Status 502 - Internal server error. Cloudflare error page breaks the code.
    while res.status_code == 400 or res.status_code == 502: 
      res = requests.get(block_explorer_url_full)
    return res.content

def get_account_properties(bitcoin_address):
    try:
        print "[!] Details in Satoshis (1 BTC = 100,000,000 Satoshis)"

        balance = get_data(bitcoin_address, "/balance")
        print "[+] Balance             : %s" % balance

        total_received = get_data(bitcoin_address, "/totalReceived")
        print "[+] Total Received      : %s" % total_received

        total_sent = get_data(bitcoin_address, "/totalSent")
        print "[+] Total Sent          : %s" % total_sent

        unconfirmed_balance = get_data(bitcoin_address, "/unconfirmedBalance")
        print "[+] Unconfirmed Balance : %s" % unconfirmed_balance

        print ""
    except Exception as e:
        print e
        print "[-] Error retrieving bitcoin wallet balance\n"

def banner():
    print colored(style.BOLD + '---> Finding details of this Bitcoin wallet\n' + style.END, 'blue')


def main(bitcoin):
    if validate(bitcoin) == 'true':
        print "[+] Bitcoin address exists\n"
        get_account_properties(bitcoin)
    else:
        print "[-] Invalid Bitcoin address"

# def output(data, bitcoin=""):
#    for i in data:
#        print i


if __name__ == "__main__":
    try:
        bitcoin = sys.argv[1]
        banner()
        #result = main(bitcoin)
        #output(result, bitcoin)
        main(bitcoin)
    except Exception as e:
        print e
        print "Please provide an valid Bitcoin address as argument"
