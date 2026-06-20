// Zigbee (ZHA) device signals.
function(cfg, sig) {
  zhaRssi: sig('Zigbee RSSI', 'hass_zha_device_rssi{%(queriesSelector)s}', 'dBm', 'Received signal strength of Zigbee devices.'),
  zhaLqi: sig('Zigbee LQI', 'hass_zha_device_lqi{%(queriesSelector)s}', 'short', 'Link quality of Zigbee devices.'),
  zhaMeshLqi: sig('Zigbee mesh LQI', 'hass_zha_mesh_lqi{%(queriesSelector)s}', 'short', 'Link quality between neighbouring Zigbee nodes.'),
  zhaAvailable: sig('ZHA availability', 'avg(hass_device_available{%(queriesSelector)s})', 'percentunit', 'Fraction of ZHA devices available.'),
}
