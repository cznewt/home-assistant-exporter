// ESPHome (Wi-Fi) panels.
function(signals) {
  esphomeRssi: signals.esphomeRssi.asTimeSeries('Wi-Fi RSSI'),
  esphomeUptime: signals.esphomeUptime.asTimeSeries('Uptime'),
}
