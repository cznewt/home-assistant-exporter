// home-assistant-observ-lib defaults. Override any field via new(config).
{
  uid: 'home-assistant',
  dashboardTitle: 'Home Assistant',
  dashboardTags: ['home-assistant', 'iot', 'esphome', 'zha'],
  datasource: '${datasource}',
  selector: 'job=~"$job"',
  varMetric: 'hass_device_info',

  // alerting — rules use a STATIC selector (Prometheus rules can't use the
  // $job dashboard variable). Leave empty to match every instance.
  alertSelector: '',
  lowBatteryThreshold: '20',  // %
  criticalBatteryThreshold: '10',  // %
  staleSeconds: '3600',  // entity last_update age (1h)
  esphomeRssiLow: '-80',  // dBm
  zhaLqiLow: '32',  // LQI (0..255)
}
