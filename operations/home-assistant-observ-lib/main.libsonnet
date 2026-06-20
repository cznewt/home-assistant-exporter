// home-assistant-observ-lib — an observ-viz observ-lib for the
// home-assistant-exporter (hass_* metrics). Climate/energy come from entities;
// the interesting bits are wireless device properties (ESPHome WiFi RSSI, ZHA
// Zigbee LQI/RSSI) and device batteries.
//
// Built on observ-viz common-lib (vendor github.com/cznewt/observ-viz, then
// `-J vendor/github.com/cznewt/observ-viz`).
//   local ha = import 'home-assistant-observ-lib/main.libsonnet';
//   ha.new({ selector: 'job="home-assistant-exporter"' }).grafana.dashboard
//   ha.new({ alertSelector: 'job="home-assistant-exporter"' }).prometheus.alerts
local pack = import 'libs/common-lib/pack.libsonnet';
local signal = import 'libs/common-lib/signal/main.libsonnet';
local alert = import 'libs/common-lib/alert/main.libsonnet';

{
  new(config={}):
    local cfg = {
      uid: 'home-assistant',
      dashboardTitle: 'Home Assistant',
      dashboardTags: ['home-assistant', 'iot', 'esphome', 'zha'],
      datasource: '${datasource}',
      selector: 'job=~"$job"',
      varMetric: 'hass_device_info',
      // alerting — rules use a STATIC selector (Prometheus rules can't use the
      // $job dashboard variable). Leave empty to match every instance.
      alertSelector: '',
      lowBatteryThreshold: '20',  // %
      criticalBatteryThreshold: '10',  // %
      staleSeconds: '3600',  // entity last_update age (1h)
      esphomeRssiLow: '-80',  // dBm
      zhaLqiLow: '32',  // LQI (0..255)
    } + config;

    local sig(name, expr, unit, desc='') =
      signal.new(name, 'prometheus', cfg.datasource, expr, unit).filteringSelector(cfg.selector).withDescription(desc);

    local signals = {
      // --- estate overview ---
      devices: sig('Devices', 'count(hass_device_info{%(queriesSelector)s})', 'short', 'Registered devices.'),
      areas: sig('Areas', 'count(hass_area_info{%(queriesSelector)s})', 'short', 'Configured areas.'),
      entities: sig('Entities', 'count(hass_entity_info{%(queriesSelector)s})', 'short', 'Registered entities.'),
      entitiesAvailable: sig('Entities available', 'avg(hass_entity_available{%(queriesSelector)s})', 'percentunit', 'Fraction of entities reporting available.'),
      unavailable: sig('Unavailable entities', 'count(hass_entity_available{%(queriesSelector)s} == 0)', 'short', 'Entities currently unavailable.'),
      stale: sig('Stale entities', 'count((time() - hass_entity_last_update{%(queriesSelector)s}) > ' + cfg.staleSeconds + ')', 'short', 'Entities not updated within the stale window.'),

      // --- device batteries ---
      battery: sig('Battery remaining', 'hass_device_battery_remaining{%(queriesSelector)s}', 'percent', 'Remaining battery charge per device.'),
      batteryVoltage: sig('Battery voltage', 'hass_device_battery_voltage{%(queriesSelector)s}', 'volt', 'Battery voltage per device.'),
      lowBattery: sig('Low batteries', 'count(hass_device_battery_remaining{%(queriesSelector)s} < ' + cfg.lowBatteryThreshold + ')', 'short', 'Devices below the low-battery threshold.'),

      // --- ESPHome (WiFi) ---
      esphomeRssi: sig('ESPHome Wi-Fi RSSI', 'hass_esphome_device_rssi{%(queriesSelector)s}', 'dBm', 'WiFi signal strength of ESPHome devices.'),
      esphomeUptime: sig('ESPHome uptime', 'hass_esphome_device_uptime{%(queriesSelector)s}', 's', 'ESPHome device uptime.'),

      // --- ZHA (Zigbee) ---
      zhaRssi: sig('Zigbee RSSI', 'hass_zha_device_rssi{%(queriesSelector)s}', 'dBm', 'Received signal strength of Zigbee devices.'),
      zhaLqi: sig('Zigbee LQI', 'hass_zha_device_lqi{%(queriesSelector)s}', 'short', 'Link quality of Zigbee devices.'),
      zhaMeshLqi: sig('Zigbee mesh LQI', 'hass_zha_mesh_lqi{%(queriesSelector)s}', 'short', 'Link quality between neighbouring Zigbee nodes.'),
      zhaAvailable: sig('ZHA availability', 'avg(hass_device_available{%(queriesSelector)s})', 'percentunit', 'Fraction of ZHA devices available.'),
    };

    // Alert rules mirror the signals above (same hass_* metrics), scoped by the
    // static cfg.alertSelector.
    local asel = if cfg.alertSelector != '' then '{' + cfg.alertSelector + '}' else '';
    local alerts = [
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
    ];

    pack.build(cfg, signals, [
      {
        title: 'Overview',
        width: 4,
        height: 5,
        elements: {
          devices: signals.devices.asStat('Devices'),
          areas: signals.areas.asStat('Areas'),
          entities: signals.entities.asStat('Entities'),
          entitiesAvailable: signals.entitiesAvailable.asStat('Available'),
          unavailable: signals.unavailable.asStat('Unavailable'),
          stale: signals.stale.asStat('Stale'),
        },
      },
      {
        title: 'Batteries',
        width: 8,
        height: 8,
        elements: {
          battery: signals.battery.asTable('Battery remaining'),
          batteryVoltage: signals.batteryVoltage.asTimeSeries('Battery voltage'),
          lowBattery: signals.lowBattery.asStat('Low batteries'),
        },
      },
      {
        title: 'ESPHome (Wi-Fi)',
        width: 12,
        height: 8,
        elements: {
          esphomeRssi: signals.esphomeRssi.asTimeSeries('Wi-Fi RSSI'),
          esphomeUptime: signals.esphomeUptime.asTimeSeries('Uptime'),
        },
      },
      {
        title: 'Zigbee (ZHA)',
        width: 6,
        height: 8,
        elements: {
          zhaRssi: signals.zhaRssi.asTimeSeries('Zigbee RSSI'),
          zhaLqi: signals.zhaLqi.asTimeSeries('Zigbee LQI'),
          zhaMeshLqi: signals.zhaMeshLqi.asTimeSeries('Mesh LQI'),
          zhaAvailable: signals.zhaAvailable.asStat('ZHA available'),
        },
      },
    ], alerts),
}
