// Render the Home Assistant dashboard to a Grafana v2 resource.
//   just render
local ha = import './main.libsonnet';
ha.new({ selector: 'job="home-assistant-exporter"' }).grafana.dashboard.toResource()
