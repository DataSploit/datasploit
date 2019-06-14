# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='',
    version=__import__("").__version__,
    packages=find_packages(),
    include_package_data=False,
    install_requires=["importlib","sys","pip","requests"],
    install_reqs = parse_requirements('requirements.txt', session='hack')
)
