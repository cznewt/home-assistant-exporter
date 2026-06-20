// Render the Home Assistant dashboard to a Grafana v2 resource.
//   jsonnet -J vendor/github.com/cznewt/observ-viz -J . render.jsonnet
local ha = import 'home-assistant-observ-lib/main.libsonnet';
ha.new({}).grafana.dashboard.toResource()
