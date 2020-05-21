import os
from termcolor import colored
from configobj import ConfigObj

def get_key(a):
    config_path = os.path.dirname(__file__)
    config_file = "%s/config.py" % config_path
    if os.path.exists(config_file):
      config = ConfigObj(config_file)
      try:
          if config[a] != '':
              return config[a]
          else:
              msg = "[-] " + a + " not configured"
              print(colored(msg, 'yellow'))
              return None
      except:
          msg = "[!] " + a + " not present"
          print(colored(msg, 'yellow'))
          return None
    else:
      print(colored("[-] Error opening config file", 'yellow'))
