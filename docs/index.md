# Home Assistant Exporter

A Prometheus exporter that provides **device / entity / area / ZHA / ESPHome
diagnostic metrics** from [Home Assistant](https://www.home-assistant.io/),
correlating entities with the devices that own them.

Unlike the built-in
[Prometheus integration](https://www.home-assistant.io/integrations/prometheus/)
(entity metrics only, behind an API token), this exporter talks to Home Assistant
over the **websocket API** and exposes device-level diagnostics that work with
automated service discovery.

- **[Configuration](configuration.md)** — point it at Home Assistant.
- **[Devices](devices.md)** — per-integration device diagnostics (ESPHome, Zigbee, …).
- **[Integrations](integrations.md)** — scrape with Prometheus or Grafana Alloy.
- **[Metrics](metrics.md)** — every metric and its labels.

## Run

```
docker run --rm -p 9878:9878 \
  -e HASS_URL=ws://homeassistant.local:8123/api/websocket \
  -e HASS_TOKEN=<long-lived-access-token> \
  ghcr.io/cznewt/home-assistant-exporter
```

On **Home Assistant OS**, install it from the
[haos-apps](https://github.com/Craftama/haos-apps) add-on repository — the add-on
is a thin wrapper around this same image.
