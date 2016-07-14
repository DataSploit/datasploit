import config as cfg
import requests
import json
import sys
import socket

def shodandomainsearch(domain):
	print "\t\t\t[+] Searching in Shodan" 
	endpoint =  "https://api.shodan.io/shodan/host/search?key=%s&query=hostname:%s&facets={facets}" % (cfg.shodan_api, domain)
	req = requests.get(endpoint)
	return req.content


def main():
	domain = sys.argv[1]
	res_from_shodan = json.loads(shodandomainsearch(domain))
	if 'matches' in res_from_shodan.keys():
		for x in res_from_shodan['matches']:
			print "IP: %s\nHosts: %s\nDomain: %s\nPort: %s\nData: %s\nLocation: %s\n" % (x['ip_str'], x['hostnames'], x['domains'], x['port'], x['data'].replace("\n",""), x['location'])
	print "-----------------------------\n"

if __name__ == "__main__":
	main()
