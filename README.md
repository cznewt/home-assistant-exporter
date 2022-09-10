# Home Assistant Exporter for Prometheus

Metrics exporter providing [Home Assistant](https://www.home-assistant.io/) diagnostic metrics.

## Motivation

* Home Assistant [Prometheus intergation](https://www.home-assistant.io/integrations/prometheus/) exposes only entity metrics with no correlation to the devices
* Home Assistant metrics endpoint requires API token which makes it impossible to use with automated Service Discovery
* Home Assistant does no provide low-level details for devices

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

### Linking Battery Entities

## Provided Metrics

### Generic Device Metrics

| Metric name| Metric type | Description | Unit | Labels/tags |
| ---------- | ----------- | ----------- | ---- | ----------- |
| hass_device_info | Gauge | General information about the device | | `device_id` <br> `device_name` <br> `manufacturer` <br> `model` <br> `sw_version` <br> `hw_version` |
| hass_device_last_activity | Counter | Last update time of entities connected to the device | s | `device_id` |
| hass_device_battery_remaining | Gauge | The remaining percentage of device battery | % | `device_id` |

### ESPHome Device Metrics

| Metric name| Metric type | Description | Unit | Labels/tags |
| ---------- | ----------- | ----------- | ---- | ----------- |
| hass_esphome_device_uptime | Counter | Number of seconds the device is running | s | `device_id` |
| hass_esphome_device_signal_strength | Gauge | ESPHome device signal strength with information about connected Access Point | dBm | `device_id` <br> `bssid` <br> `essid` |

### ZHA Device Metrics

| Metric name| Metric type | Description | Unit | Labels/tags |
| ---------- | ----------- | ----------- | ---- | ----------- |
| hass_zha_device_info | Gauge | Specific information about the Zigbee device | | `device_id` <br> `device_type` <br> `power_source` |
| hass_zha_device_lqi | Gauge | The link quality indicator (LQI) of the Zigbee device is an indication of the quality of the data packets received by the receiver. | | `device_id` |
| hass_zha_device_rssi | Gauge | Received signal strength indicator (RSSI) of the Zigbee device is a measurement of the power present in a received radio signal. | dBm | `device_id` |
| hass_zha_mesh_lqi | Gauge | LQI info of neighbouring devices connected to the Zigbee device | | `source_iee`=&lt;ieee&gt; <br> `target_ieee`=&lt;ieee&gt; |

### Generic Entity Metrics

| Metric name| Metric type | Description | Unit | Labels/tags |
| ---------- | ----------- | ----------- | ---- | ----------- |
| hass_entity_info | Gauge | General information about the entity | | `entity_id` <br> `entity_name` <br> `area_id`=&lt;area-id&gt; <br> `device_id` |
| hass_entity_info | Gauge | General information about the entity | | `entity_id` <br> `entity_name` <br> `area_id`=&lt;area-id&gt; <br> `device_id` |
