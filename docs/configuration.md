# Configuration

The exporter connects to Home Assistant over the websocket API and serves
Prometheus metrics on `:9878/metrics`.

## Environment variables

| Variable | Description |
| --- | --- |
| `HASS_URL` | Websocket URL of the target Home Assistant, e.g. `ws://homeassistant.local:8123/api/websocket`. |
| `HASS_TOKEN` | A Home Assistant [long-lived access token](https://www.home-assistant.io/docs/authentication/#your-account-profile). |

## Command-line flags

Flags take precedence over the environment variables.

```
--debug                   Log with debug level
--hass.url HASS_URL       Websocket URL of the target Home Assistant
--hass.token HASS_TOKEN   Long-lived API token
--web.listen-port PORT    Port to expose metrics on (default: 9878)
--web.telemetry-path P    Path to expose metrics under (default: /metrics)
```

## Running

### Docker

```
docker run --rm -p 9878:9878 \
  -e HASS_URL=ws://homeassistant.local:8123/api/websocket \
  -e HASS_TOKEN=<token> \
  ghcr.io/cznewt/home-assistant-exporter
```

### Compose

```
HASS_URL=ws://homeassistant.local:8123/api/websocket HASS_TOKEN=<token> \
  docker compose up --build
```

### Home Assistant OS

Install from the [haos-apps](https://github.com/Craftama/haos-apps) add-on
repository. The add-on wraps this image and, by default, talks to the local
instance through the Supervisor websocket proxy — no URL or token to configure.
