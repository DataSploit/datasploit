import pip
import sys

def check_dependency():
    list_deps = []
    missing_deps = []

    with open('requirements.txt') as f:
        list_deps = f.read().splitlines()

    pip_list = sorted([(i.key) for i in pip.get_installed_distributions()])

    for req_dep in list_deps:
        if req_dep not in pip_list:
            missing_deps.append(req_dep)

    if missing_deps:
        import os
        dependecy = 'pip install '
        for dep in missing_deps:
            dependecy += dep + ' '
        os.system(dependecy)
        sys.exit()
