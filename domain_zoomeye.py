#!/usr/bin/env python

import requests
import json
import sys
import config as cfg
from termcolor import colored
import time

class style:
   BOLD = '\033[1m'
   END = '\033[0m'

def get_accesstoken_zoomeye(domain):
	username = cfg.zoomeyeuser
	password = cfg.zoomeyepass
	datalogin = '{"username": "%s","password": "%s"}' % (username, password)
	s = requests.post("https://api.zoomeye.org/user/login", data=datalogin)
	responsedata = json.loads(s.text)
	access_token1 = responsedata['access_token']
	return access_token1


def search_zoomeye(domain):
	print colored(style.BOLD + '\n---> Finding hosts from ZoomEye\n' + style.END, 'blue')
	time.sleep(0.3)
	zoomeye_token = get_accesstoken_zoomeye(domain)
	authData = {"Authorization": "JWT " + str(zoomeye_token)}
	req = requests.get('http://api.zoomeye.org/web/search/?query=site:%s&page=1' % domain, headers=authData)
	return req.text.encode('utf-8')


def main():
	domain = sys.argv[1]
	#checks results from zoomeye
	#filters need to be applied
	zoomeye_results = search_zoomeye(domain)
	dict_zoomeye_results = json.loads(zoomeye_results)
	if 'matches' in dict_zoomeye_results.keys():
		print len(dict_zoomeye_results['matches'])
		for x in dict_zoomeye_results['matches']:
			if x['site'].split('.')[-2] == domain.split('.')[-2]:
				if 'title' in x.keys():
					print "IP: %s\nSite: %s\nTitle: %s\nHeaders: %s\nLocation: %s\n" % (x['ip'], x['site'], x['title'], x['headers'].replace("\n\n",""), x['geoinfo'])
				else:
					for val in x.keys():
						print "%s: %s" % (val, x[val])
	print "\n-----------------------------\n"

if __name__ == "__main__":
	main()
