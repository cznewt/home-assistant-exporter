#!/usr/bin/env python3

from setuptools import setup

VERSION = '0.1'

setup(
    name='home-assistant-exporter',
    version=VERSION,
    description='',
    license="GPLv3",
    install_requires=["flask", "prometheus_client", "pyyaml"],
)
