#!/usr/bin/env python

import sys
import osint_runner
import optparse


def run(bitcoin, output = None):
    osint_runner.run("bitcoin", "bitcoins", bitcoin, output)


if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option('-o', '--output', action="store", dest="output", help="Save output in either JSON or HTML")
    options, args = parser.parse_args()
    bitcoin = args[0]
    run(bitcoin, options.output)
