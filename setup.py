# -*- coding: utf-8 -*-
# https://gist.github.com/philippeowagner/6826498 autogen
#https://stackoverflow.com/questions/14399534/reference-requirements-txt-for-the-install-requires-kwarg-in-setuptools-setup-py 
# https://wiki.gentoo.org/wiki/Project:Python/distutils-r1 makes ebuilds for Gentoo or Pentoo and or Arch etc too easy. 
## proffer the template for author and improvemnts. 

from setuptools import setup, find_packages

setup(
    name='',
    version=__import__("").__version__,
    packages=find_packages(),
    include_package_data=False,
    install_requires=["importlib","sys","pip","requests"],
    install_reqs = parse_requirements('requirements.txt', session='hack')
)
