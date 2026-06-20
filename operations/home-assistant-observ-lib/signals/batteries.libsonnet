// Device battery signals.
function(cfg, sig) {
  battery: sig('Battery remaining', 'hass_device_battery_remaining{%(queriesSelector)s}', 'percent', 'Remaining battery charge per device.'),
  batteryVoltage: sig('Battery voltage', 'hass_device_battery_voltage{%(queriesSelector)s}', 'volt', 'Battery voltage per device.'),
  lowBattery: sig('Low batteries', 'count(hass_device_battery_remaining{%(queriesSelector)s} < ' + cfg.lowBatteryThreshold + ')', 'short', 'Devices below the low-battery threshold.'),
}
