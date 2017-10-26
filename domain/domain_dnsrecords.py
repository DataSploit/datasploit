#!/usr/bin/env python

import json
import base
import sys
import dns.resolver
from termcolor import colored

ENABLED = True
OUTPUT_TYPE = "console"


class style:
    BOLD = '\033[1m'
    END = '\033[0m'


def fetch_dns_records(domain, rec_type):
    try:
        answers = dns.resolver.query(domain, rec_type)
        rec_list = []
        for rdata in answers:
            rec_list.append(rdata.to_text())
        return rec_list
    except:
        if(OUTPUT_TYPE == "console"):
            return colored("No Records Found", 'red')
        if(OUTPUT_TYPE == "json"):
            return list()

def parse_dns_records(domain):
    dict_dns_record = {}
    dict_dns_record['SOA Records'] = fetch_dns_records(domain, "SOA")
    dict_dns_record['MX Records'] = fetch_dns_records(domain, "MX")
    dict_dns_record['TXT Records'] = fetch_dns_records(domain, "TXT")
    dict_dns_record['A Records'] = fetch_dns_records(domain, "A")
    dict_dns_record['Name Server Records'] = fetch_dns_records(domain, "NS")
    dict_dns_record['CNAME Records'] = fetch_dns_records(domain, "CNAME")
    dict_dns_record['AAAA Records'] = fetch_dns_records(domain, "AAAA")
    return dict_dns_record


def banner():
    if(OUTPUT_TYPE == "console"):
        print colored(style.BOLD + '---> Finding DNS Records.\n' + style.END, 'blue')


def main(domain):
    return parse_dns_records(domain)


def output(data, domain=""):
    if(OUTPUT_TYPE == "console"):
        for x in data.keys():
            print x
            if "No" in data[x] and "Found" in data[x]:
                print "\t%s" % data[x]
            else:
                for y in data[x]:
                    print "\t%s" % y
        print "\n-----------------------------\n"

    if(OUTPUT_TYPE == "json"):
        print(json.dumps(data))


if __name__ == "__main__":
    try:
        domain = sys.argv[1]
        if(len(sys.argv) > 2):
            OUTPUT_TYPE = sys.argv[2]

        banner()
        result = main(domain)
        output(result, domain)
    except Exception as e:
        print e
        print "Please provide a domain name as argument"
