#!/usr/bin/env python

import re
import sys
import shutil
import os
import textwrap
import argparse
import emailOsint
import domainOsint
import ipOsint
import bitcoinOsint
import usernameOsint
from tld import get_tld
from netaddr import IPAddress,AddrFormatError

def main(argv):
    output=None
    desc="""                                                           
   ____/ /____ _ / /_ ____ _ _____ ____   / /____   (_)/ /_
  / __  // __ `// __// __ `// ___// __ \ / // __ \ / // __/
 / /_/ // /_/ // /_ / /_/ /(__  )/ /_/ // // /_/ // // /_  
 \__,_/ \__,_/ \__/ \__,_//____// .___//_/ \____//_/ \__/  
                               /_/                         
                                                           
            Open Source Assistant for #OSINT               
                www.datasploit.info                                                           

    """
    epilog="""              Connect at Social Media: @datasploit                  
                """
    # Set all parser arguments here.
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,description=textwrap.dedent(desc),epilog=epilog)
    parser.add_argument("-i","--input",help="Provide Input",dest='target',required=True)
    parser.add_argument("-a","--active",help="Run Active Scan attacks",dest='active',action="store_false")
    parser.add_argument("-q","--quiet",help="Run scans in automated manner accepting default answers",dest='quiet',action="store_false")
    parser.add_argument("-o","--output",help="Provide Destination Directory",dest='output')
    # check and ensure the config file is present otherwise create one. required for all further operations
    ds_dir=os.path.dirname(os.path.realpath(__file__))
    config_file_path = os.path.join(ds_dir,"config.py")
    config_sample_path= os.path.join(ds_dir,"config_sample.py")
    print os.path.exists(config_file_path)
    if not os.path.exists(config_file_path):
        print "[+] Looks like a new setup, setting up the config file."
        shutil.copyfile(config_sample_path,config_file_path)
        print "[+] A config file is added please follow guide at https://datasploit.github.io/datasploit/apiGeneration/ to fill API Keys for better results"
        # We can think about quiting at this point.
    # if no argument is provided print help and quit
    if len(argv) == 0:
        parser.print_help()
        sys.exit()
    # parse arguments in case they are provided.
    x=parser.parse_args()
    active=x.active
    quiet=x.quiet
    user_input=x.target
    output=x.output
    # Banner print
    print textwrap.dedent(desc)
    # Auto selection logic
    try:    
        print "User Input: %s" % user_input
        try:
            inp=IPAddress(user_input);
            if inp.is_private() or inp.is_loopback():
                print "Internal IP Detected : Skipping"
                sys.exit()
            else:
                print "Looks like an IP, running ipOsint...\n"
                ipOsint.run(user_input, output)
        except SystemExit:
            print "exiting"
        except AddrFormatError:
            if re.match('[^@]+@[^@]+\.[^@]+', user_input):
                print "Looks like an EMAIL, running emailOsint...\n"
                emailOsint.run(user_input, output)
            elif get_tld(user_input, fix_protocol=True,fail_silently=True) is not None:
                print "Looks like a DOMAIN, running domainOsint...\n"
                domainOsint.run(user_input, output)
            elif re.match('^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$', user_input):
                print "Looks like a Bitcoin address...\n"
                bitcoinOsint.run(user_input, output)
            else:
                print "Nothing Matched assuming username, running usernameOsint...\n"
                usernameOsint.run(user_input, output)
        except:
            print "Unknown Error Occured"
    except KeyboardInterrupt:
        print "Ctrl+C called Quiting"

if __name__ == "__main__":
   main(sys.argv[1:])