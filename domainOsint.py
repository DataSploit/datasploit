import optparse
import signal
import time
import traceback

import config as cfg
from json2html import *
from termcolor import colored

from domain_censys import censys_search, censys_list
from domain_checkpunkspider import checkpunkspider
from domain_dnsrecords import DNS
from domain_emailhunter import emailhunter, collected_emails
from domain_forumsearch import boardsearch_forumsearch
from domain_github import github_search
from domain_history import netcraft_domain_history
from domain_pagelinks import pagelinks
from domain_pastes import google_search
from domain_shodan import shodandomainsearch
from domain_subdomains import subdomains, subdomains_from_netcraft, subdomain_list
from domain_wappalyzer import Wappalyzer
from domain_whois import Whois
from domain_wikileaks import wikileaks
from domain_zoomeye import search_zoomeye

parser = optparse.OptionParser()
parser.add_option('-d', '--domain', action="store", dest="domain",
                  help="Domain name against which automated Osint is to be performed.", default="spam")

raw_data = {}
csv_dict = {}

allusernames_list = []


def signal_handler(signal, frame):
    print colored(Style.BOLD + '\n [-] Brrrr...You pressed Ctrl+c and this is sad. Trying to exit..\n' + Style.END,
                  'red')
    sys.exit(0)
    quit()


def printart():
    print "\n\t  ____/ /____ _ / /_ ____ _ _____ ____   / /____  (_)/ /_"
    print "\t  / __  // __ `// __// __ `// ___// __ \ / // __ \ / // __/"
    print "\t / /_/ // /_/ // /_ / /_/ /(__  )/ /_/ // // /_/ // // /_  "
    print "\t \__,_/ \__,_/ \__/ \__,_//____// .___//_/ \____//_/ \__/  "
    print "\t                               /_/                        "
    print "\t\t\t\t\t\t"
    print "         	   Open Source Assistant for #OSINT            "
    print "                     website: www.datasploit.info               "
    print "\t"


def display_query_results(os_int_service):
    try:
        return os_int_service.retrieve()
    except Exception as e:
        traceback.print_exc(e)
        time.sleep(.3)

    return ""


def do_everything(domain):
    raw_data['targetname'] = domain

    # print WhoIs information
    raw_data['whois'] = display_query_results(Whois(domain))

    # print DNS Information
    raw_data['dns'] = display_query_results(DNS(domain))

    # print colored(Style.BOLD + '\n---> Finding Paste(s)..\n' + Style.END, 'blue')
    # if cfg.google_cse_key and cfg.google_cse_cx:
    #     total_results = google_search(domain, 1)
    #     if total_results > 10:
    #         more_iters = (total_results / 10)
    #         if more_iters >= 10:
    #             print colored(Style.BOLD + '\n---> Too many results, Daily API limit might exceed\n' + Style.END, 'red')
    #         for x in xrange(1, more_iters + 1):
    #             google_search(domain, (x * 10) + 1)
    #     print "\n\n-----------------------------\n"
    # else:
    #     print colored(
    #         Style.BOLD + '\n[-] google_cse_key and google_cse_cx not configured. Skipping paste(s) search.\nPlease refer to http://datasploit.readthedocs.io/en/latest/apiGeneration/.\n' + Style.END,
    #         'red')
    # 
    # # convert domain to reverse_domain for passing to checkpunkspider()
    # reversed_domain = ""
    # for x in reversed(domain.split(".")):
    #     reversed_domain = reversed_domain + "." + x
    # reversed_domain = reversed_domain[1:]
    # res = checkpunkspider(reversed_domain)
    # if 'data' in res.keys() and len(res['data']) >= 1:
    #     raw_data['punkspider'] = res['data']
    #     print colored("[+] Few vulnerabilities found at Punkspider", 'green')
    #     for x in res['data']:
    #         print "==> ", x['bugType']
    #         print "Method:", x['verb'].upper()
    #         print "URL:\n" + x['vulnerabilityUrl']
    #         print "Param:", x['parameter']
    # else:
    #     print colored("[-] No Vulnerabilities found on PunkSpider", 'red')
    # 
    # print colored(Style.BOLD + '\n---> Wapplyzing web page of base domain:\n' + Style.END, 'blue')

    raw_data['wappalyzer'] = display_query_results(Wappalyzer(domain))

    print "All the raw data:"
    for os_data_source in raw_data:
        print os_data_source
        print "\t%s" % raw_data[os_data_source]
        # make Search github code for the given domain.

        # git_results = github_search(domain, 'Code')
        # if git_results is not None:
        #     print git_results
        # else:
        #     print colored("Sad! Nothing found on github", 'red')
        # 
        # # collecting emails for the domain and adding information in master email list. 
        # if cfg.emailhunter != "":
        #     emails = emailhunter(domain)
        #     if len(collected_emails) >= 1:
        #         for x in collected_emails:
        #             print str(x)
        #         raw_data['email_ids'] = collected_emails
        # 
        # dns_ip_history = netcraft_domain_history(domain)
        # if len(dns_ip_history.keys()) >= 1:
        #     for x in dns_ip_history.keys():
        #         print "%s: %s" % (dns_ip_history[x], x)
        #     raw_data['domain_ip_history'] = dns_ip_history
        # 
        # subdomains(domain)
        # 
        # # domain pagelinks
        # links = pagelinks(domain)
        # if len(links) >= 1:
        #     for x in links:
        #         print x
        #     raw_data['pagelinks'] = links
        # 
        # # calling and printing subdomains after pagelinks.
        # 
        # subdomains_from_netcraft(domain)
        # print colored(Style.BOLD + '---> Finding subdomains: \n' + Style.END, 'blue')
        # time.sleep(0.9)
        # if len(subdomain_list) >= 1:
        #     for sub in subdomain_list:
        #         print sub
        #     raw_data['subdomains'] = subdomain_list
        # 
        # # wikileaks
        # leaklinks = wikileaks(domain)
        # for tl, lnk in leaklinks.items():
        #     print "%s (%s)" % (lnk, tl)
        # if len(leaklinks.keys()) >= 1:
        #     raw_data['wikileaks'] = leaklinks
        # print "For all results, visit: " + 'https://search.wikileaks.org/?query=&exact_phrase=%s&include_external_sources=True&order_by=newest_document_date' % (
        #     domain)
        # 
        # links_brd = boardsearch_forumsearch(domain)
        # for tl, lnk in links_brd.items():
        #     print "%s (%s)" % (lnk, tl)
        # if len(links_brd.keys()) >= 1:
        #     raw_data['forum_links'] = links_brd
        # 
        # if cfg.zoomeyeuser != "" and cfg.zoomeyepass != "":
        #     temp_list = []
        #     zoomeye_results = search_zoomeye(domain)
        #     dict_zoomeye_results = json.loads(zoomeye_results)
        #     if 'matches' in dict_zoomeye_results.keys():
        #         print len(dict_zoomeye_results['matches'])
        #         for x in dict_zoomeye_results['matches']:
        #             if x['site'].split('.')[-2] == domain.split('.')[-2]:
        #                 temp_list.append(x)
        #                 if 'title' in x.keys():
        #                     print "IP: %s\nSite: %s\nTitle: %s\nHeaders: %s\nLocation: %s\n" % (
        #                         x['ip'], x['site'], x['title'], x['headers'].replace("\n", ""), x['geoinfo'])
        #                 else:
        #                     for val in x.keys():
        #                         print "%s: %s" % (val, x[val])
        #     if len(temp_list) >= 1:
        #         raw_data['zoomeye'] = temp_list
        # 
        # if cfg.censysio_id and cfg.censysio_secret:
        #     print colored(Style.BOLD + '\n---> Kicking off Censys Search. This may take a while..\n' + Style.END, 'blue')
        #     censys_search(domain)
        #     if len(censys_list) >= 1:
        #         raw_data['censys'] = censys_list
        #         for x in censys_list:
        #             if x is not None and x != 'None':
        #                 print x
        # 
        # if cfg.shodan_api != "":
        #     res_from_shodan = json.loads(shodandomainsearch(domain))
        #     if 'matches' in res_from_shodan.keys():
        #         raw_data['shodan'] = res_from_shodan['matches']
        #         for x in res_from_shodan['matches']:
        #             print "IP: %s\nHosts: %s\nDomain: %s\nPort: %s\nData: %s\nLocation: %s\n" % (
        #                 x['ip_str'], x['hostnames'], x['domains'], x['port'], x['data'].replace("\n", ""), x['location'])


def main():
    signal.signal(signal.SIGINT, signal_handler)
    options, args = parser.parse_args()
    printart()
    domain = options.domain
    if domain == 'spam':
        print "[-] Invalid argument passed. \nUsage: domainOsint.py [options]\n\nOptions:\n  -h,\t\t--help\t\t\tshow " \
              "this help message and exit\n  -d DOMAIN,\t--domain=DOMAIN\t\tDomain name against which automated " \
              "Osint is to be performed. "
    else:
        do_everything(domain)


if __name__ == "__main__":
    main()
