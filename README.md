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
  name: device_name
sensor:
  - id: device_name_uptime
    name: device_name_uptime
    platform: uptime
    update_interval: 5s
  - id: device_name_wifi_signal
    name: device_name_wifi_signal
    platform: wifi_signal
    update_interval: 5s
text_sensor:
  - bssid:
      id: device_name_bssid
      name: device_name_bssid
    ip_address:
      id: device_name_ip_address
      name: device_name_ip_address
    mac_address:
      id: device_name_mac_address
      name: device_name_mac_address
    ssid:
      id: device_name_ssid
      name: device_name_ssid
    platform: wifi_info
```

Device MAC address gets propagated to `identifier` label in `hass_device_info` metrics.


## Exposed metrics

| Metric name| Metric type | Description | Unit (where applicable) | Labels/tags | Status |
| ---------- | ----------- | ----------- | ----------------------- | ----------- | ------ |
| hass_device_info | Gauge | Information about the device | | `manufacturer`=&lt;manufacturer&gt; <br> `model`=&lt;model-version&gt; <br> `sw_version`=&lt;sw-version&gt; <br> `hw_version`=&lt;hw-version&gt; <br> `id`=&lt;unique-id&gt; | STABLE |
| hass_device_name | Gauge | Human name of the device | | `name`=&lt;human-name&gt; <br> `id`=&lt;unique-id&gt; | STABLE |
| hass_device_esp_signal_strength | Gauge | Signal of the ESP device | | `ap_name`=&lt;ap-name&gt; <br> `ap_essid`=&lt;ap-essid&gt; <br> `id`=&lt;unique-id&gt; | STABLE |