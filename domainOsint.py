#!/usr/bin/env python2

import sys
import osint_runner
import optparse


def run(domain, output = None):
    osint_runner.run("domain", "domain", domain, output)


if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option('-o', '--output', action="store", dest="output", help="Save output in either JSON or HTML")
    options, args = parser.parse_args()
    domain = args[0]
    run(domain, options.output)
