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

def get_account_properties(bitcoin_address):
    block_explorer_url_addr = "https://blockexplorer.com/api/addr/"
    try:
        print "[!] Details in Satoshis"
        block_explorer_url_full = block_explorer_url_addr + bitcoin_address + "/balance"
        balance = requests.get(block_explorer_url_full)
        print "[+] Balance             : %s" % balance.content

        block_explorer_url_full = block_explorer_url_addr + bitcoin_address + "/totalReceived"
        total_received = requests.get(block_explorer_url_full)
        print "[+] Total Received      : %s" % total_received.content

        block_explorer_url_full = block_explorer_url_addr + bitcoin_address + "/totalSent"
        total_sent = requests.get(block_explorer_url_full)
        print "[+] Total Sent          : %s" % total_sent.content

        block_explorer_url_full = block_explorer_url_addr + bitcoin_address + "/unconfirmedBalance"
        unconfirmed_balance = requests.get(block_explorer_url_full)
        print "[+] Unconfirmed Balance : %s" % unconfirmed_balance.content

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
