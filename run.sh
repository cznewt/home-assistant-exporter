#!/usr/bin/with-contenv bashio

set -xe

export PYTHONPATH=/app

python /app/home_assistant_exporter/__main__.py