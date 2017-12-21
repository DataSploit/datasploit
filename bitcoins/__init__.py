
from os.path import dirname, basename, isfile, abspath
import glob, importlib, sys

modules = glob.glob(dirname(__file__) + "/bitcoin_*.py")
__all__ = [basename(f)[:-3] for f in modules if isfile(f)]
sys.path.append(dirname(abspath(__file__)))

for m in __all__:
        __import__(m, locals(), globals())
del m, f, dirname, basename, isfile, abspath, glob, importlib, sys, modules
