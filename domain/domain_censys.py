#!/usr/bin/env python
import base
import re, sys, json, time, requests
import config as cfg

ENABLED = True


def censys_search(domain):
    censys_list = []

    pages = float('inf')
    page = 1

    while page <= pages:
        print "Parsed and collected results from page %s" % (str(page))
        time.sleep(0.5)
        params = {'query': domain, 'page': page}
        res = requests.post("https://www.censys.io/api/v1/search/ipv4", json=params,
                            auth=(cfg.censysio_id, cfg.censysio_secret))
        payload = res.json()

        if 'error' not in payload.keys():
            if 'results' in payload.keys():
                for r in payload['results']:
                    temp_dict = {}
                    ip = r["ip"]
                    proto = r["protocols"]
                    proto = [p.split("/")[0] for p in proto]
                    proto.sort(key=float)
                    protoList = ','.join(map(str, proto))

                    temp_dict["ip"] = ip
                    temp_dict["protocols"] = protoList
                    print temp_dict

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
    res = requests.get("https://www.censys.io/api/v1/view/ipv4/%s" % (server),
                       auth=(cfg.censysio_id, cfg.censysio_secret))
    payload = res.json()

    try:
        if 'title' in payload['80']['http']['get'].keys():
            # print "[+] Title: %s" % payload['80']['http']['get']['title']
            title = payload['80']['http']['get']['title']
            temp_dict['title'] = title
        if 'server' in payload['80']['http']['get']['headers'].keys():
            header = "[+] Server: %s" % payload['80']['http']['get']['headers']['server']
            temp_dict["server_header"] = payload['80']['http']['get']['headers']['server']
        return temp_dict

    except Exception as error:
        print error


def output(data, domain=""):
    for i in data:
        print i


def main(domain):
    data = censys_search(domain)
    return data


if __name__ == "__main__":
    try:
        domain = sys.argv[1]
        result = main(domain)
        output(result, domain)
    except Exception as e:
        print e
        print "Please provide a domain name as argument"
