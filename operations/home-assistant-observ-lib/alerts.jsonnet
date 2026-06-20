// Render the Prometheus alert rules.
//   just alerts
local ha = import './main.libsonnet';
ha.new({ alertSelector: 'job="home-assistant-exporter"' }).prometheus.alerts
