#!/usr/bin/env python3

from setuptools import setup

VERSION = '0.1.3'

setup(
    name="home-assistant-exporter",
    version=VERSION,
    description="Metrics exporter providing Home Assistant diagnostic metrics.",
    license="GPLv3",
    install_requires=["aiohttp", "prometheus_client", "pyyaml", "ujson"],
)
