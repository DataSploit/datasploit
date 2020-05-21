import sys
import pip_api

def check_dependency():
    list_deps = []
    missing_deps = []

    with open('requirements.txt') as f:
        list_deps = f.read().splitlines()


    pip_list = sorted([i.lower() for i in pip_api.installed_distributions()])

    for req_dep in list_deps:
        if req_dep not in pip_list:
            missing_deps.append(req_dep)

    if missing_deps:
        print("You are missing {0} packages for Datasploit. Please install them using: ".format(missing_deps))
        print("pip install -r requirements.txt")
        sys.exit()
