#!/usr/bin/env python

import base
import sys
import dns.resolver
from termcolor import colored

ENABLED = True


class style:
    BOLD = '\033[1m'
    END = '\033[0m'


def fetch_dns_records(domain, rec_type):
    try:
        answers = dns.resolver.query(domain, rec_type)
        rec_list = []
        for rdata in answers:
            rec_list.append(str(rdata))
        return rec_list
    except:
        return colored("No Records Found", 'red')


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
    print colored(style.BOLD + '---> Finding DNS Records.\n' + style.END, 'blue')


def main(domain):
    return parse_dns_records(domain)


def output(data, domain=""):
    for x in data.keys():
        print x
        if "No" in data[x] and "Found" in data[x]:
            print "\t%s" % data[x]
            data[x] = ''
        else:
            for y in data[x]:
                try:
                    print "\t%s" % y
                except:
                    pass
    print "\n-----------------------------\n"


if __name__ == "__main__":
    try:
        domain = sys.argv[1]
        banner()
        result = main(domain)
        output(result, domain)
    except Exception as e:
        print e
        print "Please provide a domain name as argument"
