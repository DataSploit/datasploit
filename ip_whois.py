#!/usr/bin/env python
from ipwhois import IPWhois
import config as cfg
import requests
import json
import sys
import socket
from termcolor import colored
class style:
   BOLD = '\033[1m'
   END = '\033[0m'




def ip_whois(ip):
	obj = IPWhois(ip)
	try:
		results = obj.lookup_rdap(depth=1)
	except:
		results = 'notfound'
		print 'ASN Registry Lookup Failed'
	if results != 'notfound':
		print colored(style.BOLD + '\nWhoIS Report for IP: %s\n' + style.END, 'green') % str(ip)
		print colored(style.BOLD + '--------------- Basic Info ---------------' + style.END, 'blue')
		print 'ASN ID: %s' % results['asn']
		if 'network' in results.keys():
			print 'Org. Name: %s' % results['network']['name']
			print 'CIDR Range: %s' % results['network']['cidr']
			print 'Start Address: %s' % results['network']['start_address']
			print 'Parent Handle: %s' % results['network']['parent_handle']
			print 'Country: %s' % results['network']['country']
		if 'objects' and 'entities' in results.keys():
			print colored(style.BOLD + '\n----------- Per Handle Results -----------' + style.END, 'blue')
			for x in results['entities']:
				print 'Handle: %s' % x
				if 'contact' in results['objects'][x].keys():
					print '\tKind: %s' % results['objects'][x]['contact']['kind']
					if results['objects'][x]['contact']['phone'] is not None:
						for y in results['objects'][x]['contact']['phone']:
							print '\tPhone: %s' % y['value']
					if results['objects'][x]['contact']['title'] is not None:
						print results['objects'][x]['contact']['title']
					if results['objects'][x]['contact']['role'] is not None:
						print results['objects'][x]['contact']['role']
					if results['objects'][x]['contact']['address'] is not None:
						for y in results['objects'][x]['contact']['address']:
							print '\tAddress: %s' % y['value'].replace('\n',',')
					if results['objects'][x]['contact']['email'] is not None:
						for y in results['objects'][x]['contact']['email']:
							print '\tEmail: %s' % y['value']


def main():
	ip_addr = sys.argv[1]
	ip_whois(ip_addr)
	#print res_from_shodan
	print colored(style.BOLD + '-----------------------------------------' + style.END, 'blue')

if __name__ == "__main__":
	main()
