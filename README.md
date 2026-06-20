# Home Assistant Exporter for Prometheus

Metrics exporter providing [Home Assistant](https://www.home-assistant.io/) diagnostic metrics.

## Motivation

* Home Assistant [Prometheus integration](https://www.home-assistant.io/integrations/prometheus/) exposes only entity metrics with no correlation to the devices
* Home Assistant metrics endpoint requires API token which makes it impossible to use with automated Service Discovery
* Home Assistant does not provide low-level details for devices
* Uses https://github.com/marcelveldt/python-hass-client library

## Usage

Use docker image to run and provide HASS credentials.

```
Home Assistant Exporter

options:
  -h, --help            show this help message and exit
  --debug               Log with debug level
  --hass.url HASS_URL   The URL address of target Home Assistant service.
  --hass.token HASS_TOKEN
                        The long-lived API token of target Home Assistant service.
  --hass.mapping-config HASS_CONFIG
                        Metric mapping configuration file name.
  --web.listen-port WEB_PORT
                        The port on which to expose the web interface and generated Prometheus metrics.
  --web.telemetry-path WEB_PATH
                        Path under which to expose metrics.
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

The `Info` metric type is a `Gauge` metric type with value of `1` that adds some additional information (labels).

### Generic Device Metrics

| Metric name| Metric type | Description | Unit | Labels/tags |
| ---------- | ----------- | ----------- | ---- | ----------- |
| hass_device_info | Info | General information about the device | | `device_id` <br> `device_name` <br> `manufacturer` <br> `model` <br> `sw_version` <br> `hw_version` |
| hass_device_last_activity | Counter | Last update time of entities connected to the device | s | `device_id` <br> `device_name` |
| hass_device_battery_remaining | Gauge | The remaining percentage of device battery | % | `device_id` <br> `device_name` |
| hass_device_battery_voltage | Gauge | The remaining voltage of device battery | V | `device_id` <br> `device_name` |
| hass_device_ip_address | Info | IP address of the device | | `device_id` <br> `device_name` <br> `ip_address` |

### ESPHome Device Metrics

| Metric name| Metric type | Description | Unit | Labels/tags |
| ---------- | ----------- | ----------- | ---- | ----------- |
| hass_esphome_device_info | Info | ESPHome device info and information about connected WiFi AP | dBm | `device_id` <br> `device_name` <br> `bssid` <br> `essid` |
| hass_esphome_device_uptime | Counter | Number of seconds the device is running | s | `device_id` <br> `device_name` |
| hass_esphome_device_rssi | Gauge | Received signal strength indicator (RSSI) of the ESPHome device | dBm | `device_id` <br> `device_name` |

### ZHA Device Metrics

| Metric name| Metric type | Description | Unit | Labels/tags |
| ---------- | ----------- | ----------- | ---- | ----------- |
| hass_zha_device_info | Info | Specific information about the Zigbee device | | `device_id` <br> `device_name` <br> `device_type` <br> `power_source` |
| hass_zha_device_lqi | Gauge | The link quality indicator (LQI) of the Zigbee device is an indication of the quality of the data packets received by the receiver | | `device_id` <br> `device_name` |
| hass_zha_device_rssi | Gauge | Received signal strength indicator (RSSI) of the Zigbee device is a measurement of the power present in a received radio signal | dBm | `device_id` <br> `device_name` |
| hass_zha_mesh_lqi | Gauge | LQI info of neighbouring devices connected to the Zigbee device | | `source_iee` <br> `target_ieee` |

### Generic Entity Metrics

| Metric name| Metric type | Description | Unit | Labels/tags |
| ---------- | ----------- | ----------- | ---- | ----------- |
| hass_entity_info | Info | General information about the entity | | `entity_id` <br> `entity_name` <br> `area_id` <br> `device_id` <br> `device_name` <br> `unit` |
| hass_entity_last_change | Gauge | Last time the entity value has changed | s | `entity_id` |
| hass_entity_last_update | Gauge | Last time the entity value has been updated | s | `entity_id` |
