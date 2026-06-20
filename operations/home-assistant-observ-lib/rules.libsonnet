// rules — Prometheus recording rules over the hass_* metrics. Like alerts, they
// use the static cfg.alertSelector. Consumed by pack.build as the `rules`
// (5th) argument.
local alert = import 'libs/common-lib/alert/main.libsonnet';

function(cfg)
  local sel = if cfg.alertSelector != '' then '{' + cfg.alertSelector + '}' else '';
  [
    alert.rule.group('home-assistant.rules', [
      alert.rule.record('hass:entity_available:ratio', 'avg(hass_entity_available' + sel + ')'),
      alert.rule.record('hass:device_battery_remaining:min', 'min by (device_name) (hass_device_battery_remaining' + sel + ')'),
      alert.rule.record('hass:devices:count', 'count(hass_device_info' + sel + ')'),
    ]),
  ]
