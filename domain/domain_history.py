#!/usr/bin/env python

import base
import sys
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from termcolor import colored
import time

ENABLED = True


class style:
    BOLD = '\033[1m'
    END = '\033[0m'


def netcraft_domain_history(domain):
    ip_history_dict = {}
    time.sleep(0.3)
    endpoint = "http://toolbar.netcraft.com/site_report?url=%s" % (domain)
    # These try's could be in a for loop, but I wanted manual control
    # over the order in which the webdrivers were chosen.
    driver = None
    try:
        webdriver.PhantomJS()
        driver = webdriver.PhantomJS()
    except WebDriverException:
        try:
            webdriver.Firefox().quit()
            driver = webdriver.Firefox()
        except WebDriverException:
            try:
                webdriver.Chrome().quit()
                driver = webdriver.Chrome()
            except WebDriverException:
                ip_history_dict = { 'Error': 'No WebDriver Found!\nTry installing PhantomJS or adding the Chrome or Firefox binaries to your $PATH.'}
    if driver:
        driver.get(endpoint)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        urls_parsed = soup.findAll('a', href=re.compile(r'.*netblock\?q.*'))
        for url in urls_parsed:
            if urls_parsed.index(url) != 0:
                ip_history_dict[url['href'].split('=')[1]] = url.get_text()
        driver.quit()
    return ip_history_dict


def banner():
    print colored(style.BOLD + '\n---> Searching Domain history in Netcraft\n' + style.END, 'blue')


def main(domain):
    return netcraft_domain_history(domain)


def output(data, domain=""):
    if len(data.keys()) > 0:
        for x in data.keys():
            if 'Error' in x:
                print data[x]
                data[x] = ''
            else:
                print "%s: %s" % (data[x], x)
    else:
        print colored(style.BOLD + '\n[!] No previous domain owners found!\n' +
                      style.END, 'red')
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
