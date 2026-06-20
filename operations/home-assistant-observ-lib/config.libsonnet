// home-assistant-observ-lib config. Like the grafana observ-libs, this object
// both holds the inputs and wires the per-group signal files (signals+).
// Override any field via main.new() + withConfigMixin(config) (or the mixin's
// _config::).
{
  local this = self,

  // inputs ------------------------------------------------------------------
  uid: 'home-assistant',  // dashboard uid
  dashboardTitle: 'Home Assistant',
  dashboardTags: ['home-assistant', 'iot', 'esphome', 'zha'],
  datasource: '${datasource}',
  selector: 'job=~"$job"',  // applied to all dashboard queries
  varMetric: 'hass_device_info',  // metric backing the $job variable

  // alerting — rules use a STATIC selector (Prometheus rules can't use the
  // $job dashboard variable). Leave empty to match every instance.
  alertSelector: '',
  lowBatteryThreshold: '20',  // %
  criticalBatteryThreshold: '10',  // %
  staleSeconds: '3600',  // entity last_update age (1h)
  esphomeRssiLow: '-80',  // dBm
  zhaLqiLow: '32',  // LQI (0..255)

  // signals — one file per group, each function(this) -> { name: signal }.
  signals+: {
    overview: (import './signals/overview.libsonnet')(this),
    batteries: (import './signals/batteries.libsonnet')(this),
    esphome: (import './signals/esphome.libsonnet')(this),
    zha: (import './signals/zha.libsonnet')(this),
  },
}
