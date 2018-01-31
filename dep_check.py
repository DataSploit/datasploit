import pip
import sys

def check_dependency():
    list_deps = []
    missing_deps = []

    with open('requirements.txt') as f:
        list_deps = f.read().splitlines()

    pip_list = sorted([(i.key) for i in pip.get_installed_distributions()])

    for req_dep in list_deps:
        compare_char = ["==", ">=", "<=", ">", "<", "!="]
        for c in compare_char:
            if c in req_dep:
                pkg = req_dep.split(c)
                if pkg[0] not in pip_list:
                    missing_deps.append(req_dep)
                    break
                else:
                    installed_ver = pkg_resources.get_distribution(pkg[0]).version
                    if self.get_truth(installed_ver, c, pkg[1]):
                        break
                    else:
                        missing_deps.append(req_dep)                            
            else:
                if req_dep not in pip_list:
                    # Why this package is not in get_installed_distributions ?
                    if str(req_dep) == "argparse":
                        pass
                    else:
                        missing_deps.append(req_dep)

    if missing_deps:
        print "You are missing a module for Datasploit. Please install them using: "
        print "pip install -r requirements.txt"
        sys.exit()
