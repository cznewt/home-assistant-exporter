#!/usr/bin/env python3

from setuptools import setup

VERSION = '0.1.8'

setup(
    name="home-assistant-exporter",
    version=VERSION,
    description="Metrics exporter providing Home Assistant device diagnostic metrics.",
    license="GPLv3",
    install_requires=["aiohttp", "prometheus_client", "pyyaml", "ujson"],
)
