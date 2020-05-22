import sys
import os

class style:
    BOLD = '\033[1m'
    END = '\033[0m'

dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, dir_path)
