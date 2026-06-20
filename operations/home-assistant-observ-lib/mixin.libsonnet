// Monitoring-mixin entrypoint (grafana observ-lib shape). Renders to
// grafanaDashboards / prometheusAlerts / prometheusRules — the resources the
// justfile (and grafana's Makefile_mixin) generate.
//
// Override config via the standard mixin pattern:
//   (import 'mixin.libsonnet') { _config+:: { alertSelector: 'job="home-assistant-exporter"' } }
local halib = import './main.libsonnet';
{
  // capture the mixin object so nested literals / computed keys (which rebind
  // `self`) can still reach _halib / _config.
  local mixin = self,

  _config:: {},
  _halib::
    halib.new()
    + halib.withConfigMixin(mixin._config),

  grafanaDashboards+:: {
    [mixin._halib.config.uid + '.json']: mixin._halib.grafana.dashboard.toSpec(),
  },
  prometheusAlerts+:: { groups: mixin._halib.prometheus.alerts },
  prometheusRules+:: mixin._halib.prometheus.recordingRules,
}
