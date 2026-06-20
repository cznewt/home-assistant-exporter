// Zigbee (ZHA) panels.
function(signals) {
  zhaRssi: signals.zhaRssi.asTimeSeries('Zigbee RSSI'),
  zhaLqi: signals.zhaLqi.asTimeSeries('Zigbee LQI'),
  zhaMeshLqi: signals.zhaMeshLqi.asTimeSeries('Mesh LQI'),
  zhaAvailable: signals.zhaAvailable.asStat('ZHA available'),
}
