# Metrics

Every metric is a Prometheus **gauge**. Some are *info-style* gauges (type
"Gauge (info)" below): their value is always `1` and the useful data is carried
in the labels.

## Area & Device Metrics

| Metric name | Type | Description | Unit | Labels/tags |
| ----------- | ---- | ----------- | ---- | ----------- |
| hass_area_info | Gauge (info) | Information about the area | | `area_id` <br> `area_name` |
| hass_device_info | Gauge (info) | Information about the device | | `device_id` <br> `device_name` <br> `hass_id` <br> `manufacturer` <br> `model` <br> `sw_version` <br> `hw_version` <br> `integration` |
| hass_device_available | Gauge | Device availability (`1`/`0`); reported for ZHA devices | | `device_id` <br> `device_name` |
| hass_device_last_activity | Gauge | Last update time of the device's entities (unix timestamp) | s | `device_id` <br> `device_name` |
| hass_device_battery_remaining | Gauge | Remaining device battery charge | % | `device_id` <br> `device_name` |
| hass_device_battery_voltage | Gauge | Device battery voltage | V | `device_id` <br> `device_name` |
| hass_device_ip_address | Gauge (info) | IP address of the device | | `device_id` <br> `device_name` <br> `ip_address` |

## ESPHome Device Metrics

| Metric name | Type | Description | Unit | Labels/tags |
| ----------- | ---- | ----------- | ---- | ----------- |
| hass_esphome_device_info | Gauge (info) | ESPHome device and connected WiFi AP info | | `device_id` <br> `device_name` <br> `bssid` <br> `essid` |
| hass_esphome_device_rssi | Gauge | WiFi signal strength (RSSI) of the ESPHome device | dBm | `device_id` <br> `device_name` |
| hass_esphome_device_uptime | Gauge | Seconds the device has been running | s | `device_id` <br> `device_name` |

## ZHA (Zigbee) Device Metrics

| Metric name | Type | Description | Unit | Labels/tags |
| ----------- | ---- | ----------- | ---- | ----------- |
| hass_zha_device_info | Gauge (info) | Information about the Zigbee device | | `device_id` <br> `device_name` <br> `device_type` <br> `power_source` |
| hass_zha_device_lqi | Gauge | Link quality indicator (LQI) of the Zigbee device | | `device_id` <br> `device_name` |
| hass_zha_device_rssi | Gauge | Received signal strength indicator (RSSI) of the Zigbee device | dBm | `device_id` <br> `device_name` |
| hass_zha_mesh_lqi | Gauge | LQI between neighbouring devices in the Zigbee mesh | | `source_id` <br> `target_id` |

## Entity Metrics

| Metric name | Type | Description | Unit | Labels/tags |
| ----------- | ---- | ----------- | ---- | ----------- |
| hass_entity_info | Gauge (info) | Entity information; `1` when available, `0` otherwise | | `entity_id` <br> `entity_name` <br> `area_id` <br> `device_id` <br> `device_name` <br> `class` <br> `unit` |
| hass_entity_value | Gauge | Numeric entity state (only when the entity has a unit) | | `entity_id` |
| hass_entity_available | Gauge | Entity availability (`1`/`0`) | | `entity_id` |
| hass_entity_last_change | Gauge | Last time the entity value changed (unix timestamp) | s | `entity_id` |
| hass_entity_last_update | Gauge | Last time the entity value was updated (unix timestamp) | s | `entity_id` |
