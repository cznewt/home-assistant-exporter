// ESPHome (Wi-Fi) device signals.
function(cfg, sig) {
  esphomeRssi: sig('ESPHome Wi-Fi RSSI', 'hass_esphome_device_rssi{%(queriesSelector)s}', 'dBm', 'Wi-Fi signal strength of ESPHome devices.'),
  esphomeUptime: sig('ESPHome uptime', 'hass_esphome_device_uptime{%(queriesSelector)s}', 's', 'ESPHome device uptime.'),
}
