# Home Assistant Exporter for Prometheus

Metrics exporter providing diagnostic metrics from Home Assistant.

## Motivation

* Home Assistant Prometheus intergation exposes only entity metrics with no correlation to the devices
* Home Assistant metrics endpoint requires API token which makes it impossible to use with automated Service Discovery
* Home Assistant does no provide low-level details for devices

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

### Linking Battery Entities

## Provided Metrics

### Generic Device Metrics

| Metric name| Metric type | Description | Unit | Labels/tags |
| ---------- | ----------- | ----------- | ---- | ----------- |
| hass_device_info | Gauge | General information about the device | | `manufacturer` = &lt;manufacturer&gt; <br> `model` = &lt;model-version&gt; <br> `sw_version` = &lt;sw-version&gt; <br> `hw_version` = &lt;hw-version&gt; <br> `device_id` = &lt;device-id&gt;  <br> `device_name` = &lt;device-name&gt; |
| hass_device_last_seen | Counter | Last update time of entities connected to the device | s | `device_id` = &lt;device-id&gt; |
| hass_device_battery_remaining | Gauge | The remaining percentage of device battery | % | `device_id` = &lt;device-id&gt; |


### ESPHome Device Metrics

| Metric name| Metric type | Description | Unit | Labels/tags |
| ---------- | ----------- | ----------- | ---- | ----------- |
| hass_esphome_device_uptime | Counter | Number of seconds the device is running | s | `device_id` = &lt;device-id&gt; |
| hass_esphome_device_signal_strength | Gauge | ESPHome device signal strength with information about connected Access Point | dBm | `device_id` = &lt;device-id&gt; <br> `bssid` = &lt;ap-mac&gt; <br> `essid` = &lt;ap-name&gt; |

### ZHA Device Metrics

| Metric name| Metric type | Description | Unit | Labels/tags |
| ---------- | ----------- | ----------- | ---- | ----------- |
| hass_zha_device_info | Gauge | Specific information about the Zigbee device | | `device_id` = &lt;device-id&gt; |
| hass_zha_device_lqi | Gauge | The link quality indicator (LQI) of the Zigbee device is an indication of the quality of the data packets received by the receiver. | | `device_id` = &lt;device-id&gt; |
| hass_zha_device_rssi | Gauge | Received signal strength indicator (RSSI) of the Zigbee device is a measurement of the power present in a received radio signal. | dBm | `device_id` = &lt;device-id&gt; |
| hass_zha_mesh_lqi | Gauge | LQI info of neighbouring devices connected to the Zigbee device | | `source_iee` = &lt;ieee&gt; <br> `target_ieee` = &lt;ieee&gt; |

### Generic Entity Metrics

| Metric name| Metric type | Description | Unit | Labels/tags |
| ---------- | ----------- | ----------- | ---- | ----------- |
| hass_entity_info | Gauge | General information about the entity | | `area_id` = &lt;area-id&gt; <br> `device_id` = &lt;device-id&gt; <br> `entity_id` = &lt;entity-id&gt; <br> `entity_name` = &lt;entity-name&gt; |