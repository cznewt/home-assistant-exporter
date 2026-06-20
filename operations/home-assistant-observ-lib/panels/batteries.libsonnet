// Device battery panels.
function(signals) {
  battery: signals.battery.asTable('Battery remaining'),
  batteryVoltage: signals.batteryVoltage.asTimeSeries('Battery voltage'),
  lowBattery: signals.lowBattery.asStat('Low batteries'),
}
