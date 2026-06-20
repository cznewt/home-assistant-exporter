# Home Assistant Exporter for Prometheus

Metrics exporter providing [Home Assistant](https://www.home-assistant.io/) diagnostic metrics.

## Motivation

* Home Assistant [Prometheus integration](https://www.home-assistant.io/integrations/prometheus/) exposes only entity metrics with no correlation to the devices
* Home Assistant metrics endpoint requires API token which makes it impossible to use with automated Service Discovery
* Home Assistant does not provide low-level details for devices
* Uses https://github.com/marcelveldt/python-hass-client library

## Usage

The exporter connects to Home Assistant over the **websocket API** and serves
Prometheus metrics on `:9878/metrics`. Provide the target through the `HASS_URL`
and `HASS_TOKEN` environment variables (or the matching CLI flags):

```
docker run --rm -p 9878:9878 \
  -e HASS_URL=ws://homeassistant.local:8123/api/websocket \
  -e HASS_TOKEN=<long-lived-access-token> \
  cznewt/home-assistant-exporter
```

All options:

```
Home Assistant Exporter

options:
  -h, --help            show this help message and exit
  --debug               Log with debug level
  --hass.url HASS_URL   Websocket URL of the target Home Assistant
                        (e.g. ws://homeassistant.local:8123/api/websocket).
  --hass.token HASS_TOKEN
                        The long-lived API token of target Home Assistant service.
  --web.listen-port WEB_PORT
                        The port on which to expose the web interface and
                        generated Prometheus metrics. (default: 9878)
  --web.telemetry-path WEB_PATH
                        Path under which to expose metrics. (default: /metrics)
```

### ESPHome device config

To get diagnostic information for ESPHome devices you need to enable some sensors in ESPhome device configuration.

```yaml
esphome:
  name: <device_name>
sensor:
  - id: <device_name>_uptime
    name: <device_name>_uptime
    platform: uptime
    update_interval: 5s
  - id: <device_name>_wifi_signal
    name: <device_name>_wifi_signal
    platform: wifi_signal
    update_interval: 5s
text_sensor:
  - bssid:
      id: <device_name>_bssid
      name: <device_name>_bssid
    ip_address:
      id: <device_name>_ip_address
      name: <device_name>_ip_address
    mac_address:
      id: <device_name>_mac_address
      name: <device_name>_mac_address
    ssid:
      id: <device_name>_ssid
      name: <device_name>_ssid
    platform: wifi_info
```

Device MAC address gets propagated to `identifier` label in `hass_device_info` metrics.

## Provided Metrics

Every metric is a Prometheus **gauge**. Some are *info-style* gauges (type
"Gauge (info)" below): their value is always `1` and the useful data is carried
in the labels.

### Area & Device Metrics

| Metric name | Type | Description | Unit | Labels/tags |
| ----------- | ---- | ----------- | ---- | ----------- |
| hass_area_info | Gauge (info) | Information about the area | | `area_id` <br> `area_name` |
| hass_device_info | Gauge (info) | Information about the device | | `device_id` <br> `device_name` <br> `hass_id` <br> `manufacturer` <br> `model` <br> `sw_version` <br> `hw_version` <br> `integration` |
| hass_device_available | Gauge | Device availability (`1`/`0`); reported for ZHA devices | | `device_id` <br> `device_name` |
| hass_device_last_activity | Gauge | Last update time of the device's entities (unix timestamp) | s | `device_id` <br> `device_name` |
| hass_device_battery_remaining | Gauge | Remaining device battery charge | % | `device_id` <br> `device_name` |
| hass_device_battery_voltage | Gauge | Device battery voltage | V | `device_id` <br> `device_name` |
| hass_device_ip_address | Gauge (info) | IP address of the device | | `device_id` <br> `device_name` <br> `ip_address` |

### ESPHome Device Metrics

| Metric name | Type | Description | Unit | Labels/tags |
| ----------- | ---- | ----------- | ---- | ----------- |
| hass_esphome_device_info | Gauge (info) | ESPHome device and connected WiFi AP info | | `device_id` <br> `device_name` <br> `bssid` <br> `essid` |
| hass_esphome_device_rssi | Gauge | WiFi signal strength (RSSI) of the ESPHome device | dBm | `device_id` <br> `device_name` |
| hass_esphome_device_uptime | Gauge | Seconds the device has been running | s | `device_id` <br> `device_name` |

### ZHA (Zigbee) Device Metrics

| Metric name | Type | Description | Unit | Labels/tags |
| ----------- | ---- | ----------- | ---- | ----------- |
| hass_zha_device_info | Gauge (info) | Information about the Zigbee device | | `device_id` <br> `device_name` <br> `device_type` <br> `power_source` |
| hass_zha_device_lqi | Gauge | Link quality indicator (LQI) of the Zigbee device | | `device_id` <br> `device_name` |
| hass_zha_device_rssi | Gauge | Received signal strength indicator (RSSI) of the Zigbee device | dBm | `device_id` <br> `device_name` |
| hass_zha_mesh_lqi | Gauge | LQI between neighbouring devices in the Zigbee mesh | | `source_id` <br> `target_id` |

### Entity Metrics

| Metric name | Type | Description | Unit | Labels/tags |
| ----------- | ---- | ----------- | ---- | ----------- |
| hass_entity_info | Gauge (info) | Entity information; `1` when available, `0` otherwise | | `entity_id` <br> `entity_name` <br> `area_id` <br> `device_id` <br> `device_name` <br> `class` <br> `unit` |
| hass_entity_value | Gauge | Numeric entity state (only when the entity has a unit) | | `entity_id` |
| hass_entity_available | Gauge | Entity availability (`1`/`0`) | | `entity_id` |
| hass_entity_last_change | Gauge | Last time the entity value changed (unix timestamp) | s | `entity_id` |
| hass_entity_last_update | Gauge | Last time the entity value was updated (unix timestamp) | s | `entity_id` |
