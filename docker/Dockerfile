# Prometheus exporter for Home Assistant device / entity / ZHA / ESPHome
# diagnostics. It connects to Home Assistant over the websocket API and exposes
# the metrics on :9878/metrics. Configure with the HASS_URL / HASS_TOKEN
# environment variables (or the matching --hass.* flags); see README.md.
#
# This is the plain Docker / Kubernetes image. The Home Assistant OS add-on in
# the haos-apps repository is a thin `FROM ghcr.io/cznewt/home-assistant-exporter`
# wrapper around it.
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY files/requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

COPY files/home_assistant_exporter /app/home_assistant_exporter

EXPOSE 9878

RUN useradd --create-home --uid 10001 exporter
USER exporter

ENTRYPOINT ["python", "-m", "home_assistant_exporter"]
