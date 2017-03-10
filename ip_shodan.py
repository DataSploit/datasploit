#!/usr/bin/env python

import config as cfg
import requests
import json
import sys
import socket
from termcolor import colored
class style:
   BOLD = '\033[1m'
   END = '\033[0m'




def shodansearch(ip):
	print colored(style.BOLD + '[+] Searching in Shodan' + style.END)
	endpoint =  "https://api.shodan.io/shodan/host/" + str(ip) + "?key=" + cfg.shodan_api
	req = requests.get(endpoint)
	parsed_res = json.loads(req.content)
	if 'error' in parsed_res.keys():
		print 'No information available for that IP.'
	else:
		asn = ''
		print colored(style.BOLD + 'Report for IP: %s' + style.END, 'blue') % str(ip)
		print colored(style.BOLD + '\n----------- Per Port Results -----------' + style.END)
		if 'data' in parsed_res.keys():
			for x in parsed_res['data']:
				print colored(style.BOLD + '\nResponse from Open Port: %s'  + style.END, 'green') % (x['port'])
				'''if 'title' in x.keys():
					print colored(style.BOLD + '[+] Title:\t\t'  + style.END, 'green') + str(x['title'])'''
				if 'title' in x.keys():	
					print colored(style.BOLD + '[+] HTML Content:\t' + style.END, 'green') + str('Yes (Please inspect Manually on this port)')
				if 'http' in x.keys():	
					print colored(style.BOLD + '[+] HTTP port present:\t'  + style.END, 'green')
					print '\tTitle: %s' % x['http']['title']
					print '\tRobots: %s' % x['http']['robots']
					print '\tServer: %s' % x['http']['server']
					print '\tComponents: %s' % x['http']['components']
					print '\tSitemap: %s' % x['http']['sitemap']
				if 'ssh' in x.keys():	
					print colored(style.BOLD + '[+] HTTP port present:\t'  + style.END, 'green')
					print '\tType: %s' % x['ssh']['type']
					print '\tCipher: %s' % x['ssh']['cipher']
					print '\tFingerprint: %s' % x['ssh']['fingerprint']
					print '\tMac: %s' % x['ssh']['mac']
					print '\tKey: %s' % x['ssh']['key']
				if 'ssl' in x.keys():
					print '\tSSL Versions: %s' % x['ssl']['versions'] 	
				if 'asn' in x.keys():
					asn = parsed_res['asn']
				if 'vulns' in x['opts']:
					for y in x['opts'].keys():
						print x['opts'][y]
				if 'product' in x.keys():
					print 'Product: %s' % x['product']
				if 'version' in x.keys():
					print 'Version: %s' % x['version']
		print colored(style.BOLD + '\n----------- Basic Info -----------' + style.END, 'blue')
		print 'Open Ports: %s' % parsed_res['ports'] 
		print 'Latitude: %s' % parsed_res['latitude']
		print 'Hostnames: %s' % parsed_res['hostnames']
		print 'Postal Code: %s' % parsed_res['postal_code']
		print 'Country Code: %s' % parsed_res['country_code']
		print 'Organization: %s' % parsed_res['org']
		if asn != '':
			print 'ASN: %s' % asn
		if 'vulns' in parsed_res.keys():
			print colored(style.BOLD + 'Vulnerabilties: %s'  + style.END, 'red') % parsed_res['vulns']
	

def domaintoip(domain):
	return socket.gethostbyname(domain)

def main():
	ip_addr = sys.argv[1]
	shodansearch(ip_addr)
	#print res_from_shodan
	print colored(style.BOLD + '-----------------------------------------' + style.END, 'blue')

if __name__ == "__main__":
	main()
