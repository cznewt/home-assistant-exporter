# ESPHome

To get diagnostic information for ESPHome devices, enable a few sensors in the
ESPHome device configuration. The exporter reads them to populate
`hass_esphome_device_*` and the device's IP address.

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

The device MAC address is propagated to the `device_id` label of the ESPHome
device's metrics.
