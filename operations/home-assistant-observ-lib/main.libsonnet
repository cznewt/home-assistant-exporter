// home-assistant-observ-lib — an observ-viz observ-lib for the
// home-assistant-exporter (hass_* metrics). Wireless device properties (ESPHome
// Wi-Fi RSSI, ZHA Zigbee LQI/RSSI), device batteries and entity availability.
// observ-viz renders the Grafana v2 dashboard — there is no grafonnet.
//
//   local ha = import 'home-assistant-observ-lib/main.libsonnet';
//   (ha.new() + ha.withConfigMixin({ selector: 'job="home-assistant-exporter"' }))
//     .grafana.dashboard
//
// Structure (grafana observ-lib shape):
//   config.libsonnet      inputs + signal wiring (signals+)
//   signals/              hass_* signal definitions, one file per group
//   panels/               panel elements built from signals, one file per group
//   dashboards.libsonnet  board layout (rows of panels)
//   alerts.libsonnet      Prometheus alert rules from the same signals
//   mixin.libsonnet       monitoring-mixin entrypoint
local pack = import 'libs/common-lib/pack.libsonnet';
local config = import './config.libsonnet';
local panels = import './panels/main.libsonnet';
local dashboards = import './dashboards.libsonnet';
local alerts = import './alerts.libsonnet';
local rules = import './rules.libsonnet';

{
  new(): {
    local this = self,
    config: config,
    // flatten the grouped config.signals into one map (observ-viz pack wants flat)
    signals:
      std.foldl(
        function(acc, g) acc + this.config.signals[g],
        std.objectFields(this.config.signals),
        {},
      ),
    local builtPanels = panels(this.signals),
    local groups = dashboards(builtPanels),
    local alertGroups = alerts(this.config),
    local recordGroups = rules(this.config),
    local built = pack.build(this.config, this.signals, groups, alertGroups, recordGroups),
    grafana: built.grafana,
    prometheus: {
      alerts: built.prometheus.alerts,
      recordingRules: built.prometheus.rules,
    },
    asMonitoringMixin():: built.asMonitoringMixin(),
  },

  withConfigMixin(config): {
    config+: config,
  },
}
