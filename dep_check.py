import pkg_resources
import sys

def check_dependency():
    list_deps = []
    missing_deps = []

    with open('requirements.txt') as f:
        list_deps = f.read().splitlines()

    # get list of installed python packages
    pip_list = []
    for item in pkg_resources.working_set.entry_keys:
        pip_list += pkg_resources.working_set.entry_keys[item]

    for req_dep in list_deps:
        if req_dep not in pip_list:
            missing_deps.append(req_dep)

    if missing_deps:
        print "You are missing a module for Datasploit:"
        for module in missing_deps:
            print module
        print "Please install them using: pip install -r requirements.txt"
        sys.exit()
