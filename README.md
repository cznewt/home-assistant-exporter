# home-assistant-exporter

Metric exporter exposing diagnostic metrics for devices connected to Home Assistant.

## Motivation

* Home Assistant Prometheus intergation exposes only entity metrics with no correlation to actual devices
* Home Assistant metrics endpoint requires API token which makes it impossible to use with automated Service Discovery
* Home Assistant does no provide low-level details for devices at all

## Usage

Use docker image to run and provide HASS credentials.

### ESPHome device config

To get diagnostic information for ESPHome devices we need to have some sensors defined in their configuration.

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

## Exposed metrics

| Metric name| Metric type | Description | Unit | Labels/tags |
| ---------- | ----------- | ----------- | ---- | ----------- |
| hass_device_info | Gauge | General information about the device | | `manufacturer` =&lt; manufacturer&gt; <br> `model` =&lt; model-version&gt; <br> `sw_version` =&lt; sw-version&gt; <br> `hw_version` =&lt; hw-version&gt; <br> `id` =&lt; unique-id&gt; |
| hass_device_last_seen | Counter | Last update time of entities connected to the device | | `device` =&lt; device-id&gt; |
| hass_device_battery_remaining | Gauge | The remaining percentage of device battery | % | `device` =&lt; device-id&gt; |
| hass_device_esphome_uptime | Counter | Number of seconds the device is running | s | `device` =&lt; device-id&gt; |
| hass_device_esphome_wifi_signal_strength | Gauge | ESPHome device signal strength with information about connected Access Point | dBm | `device` =&lt; device-id&gt; <br> `bssid` =&lt; ap-name&gt; <br> `essid` =&lt; ap-essid&gt; |
| hass_device_zha_mesh_lqi | Gauge | LQI info of neighbouring devices connected to the Zigbee device | | `device` =&lt; device-id&gt; <br> `neighbour` =&lt; device-id&gt; |
