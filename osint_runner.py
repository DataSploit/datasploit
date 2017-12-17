import importlib
import os
import sys
import json
from glob import glob
from collections import OrderedDict
from datetime import datetime


def run(component, module_dir, m_input, output = None):
    dir_path = "%s/%s" % (os.path.dirname(os.path.abspath(__file__)), module_dir)
    sys.path.insert(0, dir_path)
    domain_files = glob("%s/%s_*.py" % (dir_path, component))
    active_modules = OrderedDict()
    for index, i in enumerate(domain_files):
        module_name = os.path.basename(os.path.splitext(i)[0])
        x = importlib.import_module(module_name)
        if not x.ENABLED:
            print "[-] Skipping %s because it is marked as disabled." % module_name.split("_")[1].title()
        else:
            active_modules[os.path.basename(os.path.splitext(i)[0])] = x

    json_output = {}

    for name, x in active_modules.iteritems():
        if "banner" in dir(x):
            x.banner()
        data = x.main(m_input)
        if data:
            x.output(data, m_input)
        if output and str(output).upper() == "JSON":
            json_output[name] = data

    if output and str(output).upper() == "JSON":
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = "datasploit_%s_%s_%s.json" % (module_dir, m_input, timestamp)
        filepath = "reports/json"
        if not os.path.exists(filepath):
            os.makedirs(filepath)
        file = "%s/%s" % (filepath, filename)
        with open(file, "w") as fh:
            json.dump(json_output, fh, indent=4, sort_keys=True)
        print "JSON report saved to %s/%s" % (filepath, filename)
