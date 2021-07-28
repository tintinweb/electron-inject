#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import setup

def read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except Exception:
        return "Not available"
setup(
    name="electron-inject",
    version="0.6",
    packages=["electron_inject"],
    author="tintinweb",
    author_email="tintinweb@oststrom.com",
    description=(
        "An electron application wrapper that utilizes the remote debug console to inject code into electron applications to enable developer tools"),
    license="GPLv3",
    keywords=["electron", "inject", "devtools", "developer tools"],
    url="https://github.com/tintinweb/electron-inject/",
    download_url="https://github.com/tintinweb/electron-inject/tarball/v0.5",
    #python setup.py register -r https://testpypi.python.org/pypi
    long_description=read("README.md"),
    long_description_content_type='text/markdown',
    install_requires=['websocket','requests'],
    package_data = {
                    'electron_inject': ['electron_inject'],
                    },
)
