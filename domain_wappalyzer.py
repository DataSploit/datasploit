#!/usr/bin/env python

import Wappalyzer.Wappalyzer as wapplyzer_module
import sys
from Wappalyzer import WebPage
from os_int_service import OsIntService


class Wappalyzer(OsIntService):
    def _perform_query(self):
        def wappalyze_results_for_url(url):
            web_page = WebPage.new_from_url(url)
            return wapplyzer_module.latest().analyze(web_page) or []

        http_and_https = ["http://www.%s" % self.domain, "https://www.%s" % self.domain]
        return {url: wappalyze_results_for_url(url) for url in http_and_https}

    def _formatted_data(self):
        formatted_data = ""
        for url in sorted(self.raw_data):
            if self.raw_data[url]:
                formatted_data += "[+] Third party libraries in Use for %s:\n" % url
                formatted_data += "".join("\t%s\n" % s for s in self.raw_data[url])
            else:
                formatted_data = "\t\t\t[-] Nothing found. Make sure domain name is passed properly"
        return formatted_data


def main():
    domain = sys.argv[1]
    w = Wappalyzer(domain)
    w.retrieve()


if __name__ == "__main__":
    main()
