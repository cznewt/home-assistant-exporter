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
| Zigbee (ZHA) | `hass_zha_device_rssi`, `hass_zha_device_lqi`, `hass_zha_mesh_lqi`, `hass_device_available` |

## Alerts

`prometheus.alerts` ships rules built from the same signals (group
`home-assistant`):

| Alert | Expr | Severity |
|-------|------|----------|
| `HassDeviceBatteryLow` / `HassDeviceBatteryCritical` | `hass_device_battery_remaining < 20` / `< 10` | warning / critical |
| `HassDeviceUnavailable` | `hass_device_available == 0` | warning |
| `HassEntityStale` | `time() - hass_entity_last_update > 3600` | warning |
| `HassEsphomeWifiWeak` | `hass_esphome_device_rssi < -80` | warning |
| `HassZigbeeLinkQualityLow` | `hass_zha_device_lqi < 32` | warning |

Thresholds and the (static) alert selector are configurable — see `new(config)`.

## Structure

Same shape as grafana's observ-libs (e.g. `windows-observ-lib`), but built on
observ-viz — its own Grafana v2 `gen/` does all rendering, so there is no
grafonnet.

```
config.libsonnet      inputs + signal wiring (signals+)
signals/              hass_* signal definitions, one file per group
  signal.libsonnet      signal factory bound to config
panels/               panel elements built from signals, one file per group
dashboards.libsonnet  board layout (rows of panels)
alerts.libsonnet      Prometheus alert rules from the same signals
rules.libsonnet       Prometheus recording rules from the same signals
main.libsonnet        new() + withConfigMixin(config)
mixin.libsonnet       monitoring-mixin entrypoint (grafanaDashboards / …)
render-*.jsonnet      manifests the observ-lib image renders
justfile              render the mixin via the observ-lib image
```

## Use

Render the mixin via the `justfile` — the **observ-lib** image (from
[observ-viz](https://github.com/cznewt/observ-viz)) bakes the library in on the
jpath, so there's **no `jb`/vendor** and nothing installed locally:

```sh
just build        # render dashboards_out/ + prometheus_alerts.yaml + prometheus_rules.yaml
# or individually: just dashboards | just alerts | just rules
```

Or embed it — `new()` then override config with `withConfigMixin`:

```jsonnet
local ha = import 'home-assistant-observ-lib/main.libsonnet';
(ha.new() + ha.withConfigMixin({ selector: 'job="home-assistant-exporter"' }))
  .grafana.dashboard.toResource()
```

Config (`config.libsonnet`) accepts `{ uid, dashboardTitle, datasource, selector,
varMetric, alertSelector, lowBatteryThreshold, criticalBatteryThreshold,
staleSeconds, esphomeRssiLow, zhaLqiLow }`. The lib bundle exposes `signals`,
`grafana.{elements,layout,dashboard}`, `prometheus.alerts` and
`asMonitoringMixin()`. Alert rules use `alertSelector` — a *static* selector,
since Prometheus rules can't reference the `$job` dashboard variable.
