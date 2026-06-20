# home-assistant-observ-lib

An [observ-viz](https://github.com/cznewt/observ-viz) observ-lib for the
**home-assistant-exporter** (`hass_*` metrics). Generates a Grafana **v2**
dashboard for the Home Assistant estate, focused on the data this exporter is
good at: **wireless device properties** (ESPHome Wi-Fi RSSI/uptime, ZHA Zigbee
LQI/RSSI), **device batteries** (remaining %, voltage), and entity availability.

## Boards / signal groups

| Group | Signals |
|-------|---------|
| Overview | devices, areas, entities, available %, unavailable, stale |
| Batteries | `hass_device_battery_remaining`, `hass_device_battery_voltage`, low-battery count |
| ESPHome (Wi-Fi) | `hass_esphome_device_rssi`, `hass_esphome_device_uptime` |
| Zigbee (ZHA) | `hass_zha_device_rssi`, `hass_zha_device_lqi`, `hass_device_available` |

## Use

```sh
jb install                       # pulls observ-viz (see jsonnetfile.json)
jsonnet -J vendor/github.com/cznewt/observ-viz -J . render.jsonnet > home-assistant.json
```

```jsonnet
local ha = import 'home-assistant-observ-lib/main.libsonnet';
ha.new({ selector: 'job="home-assistant-exporter"' }).grafana.dashboard.toResource()
```

`new(config)` accepts `{ uid, dashboardTitle, datasource, selector, varMetric }`
and returns the observ-lib bundle (`signals`, `grafana.{elements,layout,dashboard}`,
`prometheus.alerts`, `asMonitoringMixin()`).
