#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    install_requires=[
        "pyserial>=3.5",
        "flask_restful>=0.3.9",
        "docopt>=0.6.2",
        "waitress>=2.0.0"
    ]
)
