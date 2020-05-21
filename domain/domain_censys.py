#!/usr/bin/env python
from . import base
import re, sys, json, time, requests
import vault
from termcolor import colored


ENABLED = True

class style:
    BOLD = '\033[1m'
    END = '\033[0m'

def check_api_keys():
    try:
        if vault.get_key('censysio_id') != None and vault.get_key('censysio_secret') != None:
            return True
        else:
            return False
    except:
        return False

def censys_search(domain):
    censys_list = []

    pages = float('inf')
    page = 1

    censysio_id = vault.get_key('censysio_id')
    censysio_secret = vault.get_key('censysio_secret')

    while page <= pages:
        print("Parsed and collected results from page %s" % (str(page)))
        #time.sleep(0.5)
        params = {'query': domain, 'page': page}
        res = requests.post("https://www.censys.io/api/v1/search/ipv4", json=params,
                            auth=(censysio_id, censysio_secret))
        payload = res.json()

        if 'error' not in list(payload.keys()):
            if 'results' in list(payload.keys()):
                for r in payload['results']:
                    temp_dict = {}
                    ip = r["ip"]
                    proto = r["protocols"]
                    proto = [p.split("/")[0] for p in proto]
                    proto.sort(key=float)
                    protoList = ','.join(map(str, proto))

                    temp_dict["ip"] = ip
                    temp_dict["protocols"] = protoList

                    if '80' in protoList:
                        new_dict = view(ip, temp_dict)
                        censys_list.append(new_dict)
                    else:
                        censys_list.append(temp_dict)

                    pages = payload['metadata']['pages']
                    page += 1
        else:
            censys_list = None
            break
    return censys_list


def view(server, temp_dict):
    censysio_id = vault.get_key('censysio_id')
    censysio_secret = vault.get_key('censysio_secret')
    res = requests.get("https://www.censys.io/api/v1/view/ipv4/%s" % (server),
                       auth=(censysio_id, censysio_secret))
    payload = res.json()

    try:
        if 'title' in list(payload['80']['http']['get'].keys()):
            # print "[+] Title: %s" % payload['80']['http']['get']['title']
            title = payload['80']['http']['get']['title']
            temp_dict['title'] = title
        if 'server' in list(payload['80']['http']['get']['headers'].keys()):
            header = "[+] Server: %s" % payload['80']['http']['get']['headers']['server']
            temp_dict["server_header"] = payload['80']['http']['get']['headers']['server']
        return temp_dict

    except Exception as error:
        print(error)


def output(data, domain=""):
    if data is not None:
        for i in data:
            print(i)


def main(domain):
    if check_api_keys() == True:
        data = censys_search(domain)
        return data
    else:
        print(colored(style.BOLD + '\n[-] Please configure respective API Keys for this module.\n' + style.END, 'red'))
        return None

if __name__ == "__main__":
    try:
        domain = sys.argv[1]
        result = main(domain)
        output(result, domain)
    except Exception as e:
        print(e)
        print(colored(style.BOLD + '\n[-] Please provide a domain name as argument\n' + style.END, 'red'))
