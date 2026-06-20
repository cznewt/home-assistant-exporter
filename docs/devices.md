# Devices

Every Home Assistant device is exported as `hass_device_info` (an info-style
gauge) carrying its `manufacturer`, `model`, `sw_version`, `hw_version` and the
`integration` it comes from. On top of that, the exporter adds the diagnostics
each integration exposes — battery, availability, signal quality — and some
integrations get richer, dedicated metrics.

## All devices

Whatever the integration, a device gets:

- `hass_device_info{integration=...}` — identity and the source integration
- `hass_device_last_activity` — last time one of its entities updated
- `hass_device_battery_remaining` / `hass_device_battery_voltage` — when the
  device exposes a battery entity
- `hass_device_ip_address` — when the device exposes an IP-address entity

See [Metrics](metrics.md) for the full label sets.

## ESPHome

[ESPHome](https://esphome.io/) devices get dedicated WiFi and uptime
diagnostics — `hass_esphome_device_info` (BSSID/ESSID), `hass_esphome_device_rssi`
and `hass_esphome_device_uptime` — and their MAC address becomes the stable
`device_id`.

Enable a few sensors in the ESPHome device config so the data is available:

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

## Zigbee (ZHA)

Zigbee devices managed by [ZHA](https://www.home-assistant.io/integrations/zha/)
get mesh diagnostics: `hass_zha_device_info` (device type, power source),
`hass_zha_device_lqi`, `hass_zha_device_rssi`, and `hass_zha_mesh_lqi` for the
link quality between neighbouring nodes. ZHA devices also report
`hass_device_available`.

## Z-Wave, Matter, Bluetooth (BLE) and others

These are exported today as **generic devices** — `hass_device_info` with the
integration label (`zwave_js`, `matter`, `bluetooth`, …) plus battery,
availability and last-activity wherever the integration provides them.

!!! note "Roadmap"
    Dedicated diagnostics for Z-Wave (link quality, routing), Matter and
    Bluetooth/BLE (RSSI) are planned, following the same per-integration pattern
    as ESPHome and ZHA. Until then these devices still appear with the common
    device metrics above.
