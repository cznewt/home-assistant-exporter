#!/usr/bin/with-contenv bashio

set -xe

export PYTHONPATH=/exporter

python /exporter/home_assistant_exporter/__main__.py