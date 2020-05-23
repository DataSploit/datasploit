#!/usr/bin/env python

import base
import vault
import requests
import json
import sys
from termcolor import colored

# set to false until I find time to debug. API may have been updated
ENABLED = False


def banner():
    print(colored(base.style.BOLD + '[+] Searching in Shodan' + base.style.END))


def main(ip):
    shodan_api = vault.get_key('shodan_api')
    if shodan_api != None:
        endpoint = "https://api.shodan.io/shodan/host/" + str(ip) + "?key=" + shodan_api
        req = requests.get(endpoint)
        return json.loads(req.content)
    else:
        return [False, "INVALID_API"]


def output(data, ip=""):
    if type(data) == list and data[1] == "INVALID_API":
        print(colored(
                base.style.BOLD + '\n[-] Shodan API Key not configured. Skipping Shodan search.\nPlease refer to http://datasploit.readthedocs.io/en/latest/apiGeneration/.\n' + base.style.END, 'red'))
    else:
        if 'error' in list(data.keys()):
            print('No information available for that IP.')
        else:
            asn = ''
            print(colored(base.style.BOLD + '\n----------- Per Port Results -----------' + base.style.END))
            if 'data' in list(data.keys()):
                for x in data['data']:
                    print(colored(base.style.BOLD + '\nResponse from Open Port: %s' + base.style.END, 'green') % (x['port']))
                    '''if 'title' in x.keys():
                        print colored(base.style.BOLD + '[+] Title:\t\t'  + base.style.END, 'green') + str(x['title'])'''
                    if 'title' in list(x.keys()):
                        print(colored(base.style.BOLD + '[+] HTML Content:\t' + base.style.END, 'green') + str(
                            'Yes (Please inspect Manually on this port)'))
                    if 'http' in list(x.keys()):
                        print(colored(base.style.BOLD + '[+] HTTP port present:\t' + base.style.END, 'green'))
                        print('\tTitle: %s' % x['http']['title'])
                        print('\tRobots: %s' % x['http']['robots'])
                        print('\tServer: %s' % x['http']['server'])
                        print('\tComponents: %s' % x['http']['components'])
                        print('\tSitemap: %s' % x['http']['sitemap'])
                    if 'ssh' in list(x.keys()):
                        print(colored(base.style.BOLD + '[+] HTTP port present:\t' + base.style.END, 'green'))
                        print('\tType: %s' % x['ssh']['type'])
                        print('\tCipher: %s' % x['ssh']['cipher'])
                        print('\tFingerprint: %s' % x['ssh']['fingerprint'])
                        print('\tMac: %s' % x['ssh']['mac'])
                        print('\tKey: %s' % x['ssh']['key'])
                    if 'ssl' in list(x.keys()):
                        print('\tSSL Versions: %s' % x['ssl']['versions'])
                    if 'asn' in list(x.keys()):
                        asn = data['asn']
                    if 'vulns' in x['opts']:
                        for y in list(x['opts'].keys()):
                            print(x['opts'][y])
                    if 'product' in list(x.keys()):
                        print('Product: %s' % x['product'])
                    if 'version' in list(x.keys()):
                        print('Version: %s' % x['version'])
            print(colored(base.style.BOLD + '\n----------- Basic Info -----------' + base.style.END, 'blue'))
            print('Open Ports: %s' % data['ports'])
            print('Latitude: %s' % data['latitude'])
            print('Hostnames: %s' % data['hostnames'])
            print('Postal Code: %s' % data['postal_code'])
            print('Country Code: %s' % data['country_code'])
            print('Organization: %s' % data['org'])
            if asn != '':
                print('ASN: %s' % asn)
            if 'vulns' in list(data.keys()):
                print(colored(base.style.BOLD + 'Vulnerabilties: %s' + base.style.END, 'red') % data['vulns'])
        print("")

if __name__ == "__main__":
    try:
        ip = sys.argv[1]
        banner()
        result = main(ip)
        if result:
            output(result, ip)
    except Exception as e:
        print(e)
        print("Please provide an IP Address as argument")
