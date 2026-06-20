#!/usr/bin/env python3

from setuptools import setup, find_packages

VERSION = "0.1.10"

setup(
    name="home-assistant-exporter",
    version=VERSION,
    description="Metrics exporter providing Home Assistant device diagnostic metrics.",
    license="GPLv3",
    packages=find_packages(exclude=["tests", "tests.*"]),
    python_requires=">=3.11",
    install_requires=[
        "aiohttp[speedups]",
        "prometheus-client>=0.21",
        "pyyaml",
        "ujson",
        "hass-client==1.2.3",
    ],
    entry_points={
        "console_scripts": [
            "home-assistant-exporter=home_assistant_exporter.__main__:main",
        ],
    },
)
