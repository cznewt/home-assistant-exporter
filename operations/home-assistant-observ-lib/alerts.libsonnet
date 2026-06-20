// alerts — Prometheus alert rules built from the same hass_* metrics as the
// signals, scoped by the static cfg.alertSelector. Consumed by pack.build as
// the `alerts` argument (a list of rule groups).
local alert = import 'libs/common-lib/alert/main.libsonnet';

function(cfg)
  local asel = if cfg.alertSelector != '' then '{' + cfg.alertSelector + '}' else '';
  [
    alert.rule.group('home-assistant', [
      alert.rule.new(
        'HassDeviceBatteryLow',
        'hass_device_battery_remaining' + asel + ' < ' + cfg.lowBatteryThreshold,
        '1h',
        'warning',
        {},
        {
          summary: 'Home Assistant device battery low.',
          description: '{{ $labels.device_name }} is at {{ $value | printf "%.0f" }}% battery.',
        },
      ),
      alert.rule.new(
        'HassDeviceBatteryCritical',
        'hass_device_battery_remaining' + asel + ' < ' + cfg.criticalBatteryThreshold,
        '30m',
        'critical',
        {},
        {
          summary: 'Home Assistant device battery critically low.',
          description: '{{ $labels.device_name }} is at {{ $value | printf "%.0f" }}% battery.',
        },
      ),
      alert.rule.new(
        'HassDeviceUnavailable',
        'hass_device_available' + asel + ' == 0',
        '15m',
        'warning',
        {},
        {
          summary: 'Home Assistant device unavailable.',
          description: '{{ $labels.device_name }} has been unavailable for 15m.',
        },
      ),
      alert.rule.new(
        'HassEntityStale',
        '(time() - hass_entity_last_update' + asel + ') > ' + cfg.staleSeconds,
        '15m',
        'warning',
        {},
        {
          summary: 'Home Assistant entity is stale.',
          description: '{{ $labels.entity_id }} has not updated within ' + cfg.staleSeconds + 's.',
        },
      ),
      alert.rule.new(
        'HassEsphomeWifiWeak',
        'hass_esphome_device_rssi' + asel + ' < ' + cfg.esphomeRssiLow,
        '15m',
        'warning',
        {},
        {
          summary: 'ESPHome device has weak Wi-Fi.',
          description: '{{ $labels.device_name }} Wi-Fi RSSI is {{ $value | printf "%.0f" }} dBm.',
        },
      ),
      alert.rule.new(
        'HassZigbeeLinkQualityLow',
        'hass_zha_device_lqi' + asel + ' < ' + cfg.zhaLqiLow,
        '15m',
        'warning',
        {},
        {
          summary: 'Zigbee device link quality low.',
          description: '{{ $labels.device_name }} LQI is {{ $value | printf "%.0f" }}.',
        },
      ),
    ]),
  ]
