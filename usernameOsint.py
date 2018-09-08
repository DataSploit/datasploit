#!/usr/bin/env python2

import sys
import osint_runner
import optparse


def run(username, output = None):
    osint_runner.run("username", "username", username, output)


if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option('-o', '--output', action="store", dest="output", help="Save output in either JSON or HTML")
    options, args = parser.parse_args()
    username = args[0]
    run(username, options.output)
