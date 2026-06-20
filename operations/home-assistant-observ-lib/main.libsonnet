// home-assistant-observ-lib — an observ-viz observ-lib for the
// home-assistant-exporter (hass_* metrics). The interesting bits are wireless
// device properties (ESPHome Wi-Fi RSSI, ZHA Zigbee LQI/RSSI), device batteries
// and entity availability. observ-viz renders the Grafana v2 dashboard — there
// is no grafonnet here.
//
//   local ha = import 'home-assistant-observ-lib/main.libsonnet';
//   ha.new({ selector: 'job="home-assistant-exporter"' }).grafana.dashboard
//   ha.new({ alertSelector: 'job="home-assistant-exporter"' }).prometheus.alerts
//
// Structure:
//   config.libsonnet      defaults (override via new(config))
//   signals/              hass_* signal definitions, one file per group
//   panels/               panel elements built from signals, one file per group
//   dashboards.libsonnet  board layout (rows of panels)
//   alerts.libsonnet      Prometheus alert rules from the same signals
local pack = import 'libs/common-lib/pack.libsonnet';

{
  new(config={}):
    local cfg = (import './config.libsonnet') + config;
    local signals = (import './signals/main.libsonnet')(cfg);
    local panels = (import './panels/main.libsonnet')(signals);
    local groups = (import './dashboards.libsonnet')(panels);
    local alerts = (import './alerts.libsonnet')(cfg);
    pack.build(cfg, signals, groups, alerts),
}
