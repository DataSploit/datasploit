import pkg_resources
import sys

def check_dependency():
    missing_deps = []

    with open('requirements.txt', 'r') as reqs_file:
        for req_dep in reqs_file.read().splitlines():
            try:
                pkg_resources.get_distribution(req_dep)
            except pkg_resources.DistributionNotFound:
                missing_deps.append(req_dep)

    if missing_deps:
        print "You are missing the following module(s) needed to run DataSploit:"
        print ", ".join(missing_deps)
        print "Please install them using: `pip install -r requirements.txt`"
        sys.exit()
