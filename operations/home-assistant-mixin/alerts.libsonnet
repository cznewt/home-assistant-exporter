{
  prometheusAlerts+:: {
    groups+: [
      {
        name: 'home-assistant',
        rules:
          [
            {
              alert: 'HassDeviceBatteryLow',
              expr: |||
                predict_linear(hass_device_battery_remaining[2h], 24 * 3600) < 0
              |||,
              'for': '15m',
              labels: {
                severity: 'warning',
              },
              annotations: {
                summary: 'The device battery discharges in 24 hours.',
                description: 'Device {{$labels.device_name}} will discharge in 24 hours.',
              },
            },
            {
              alert: 'HassDeviceBatteryLow',
              expr: |||
                predict_linear(hass_device_battery_remaining[2h], 4 * 3600) < 0
              |||,
              'for': '15m',
              labels: {
                severity: 'critical',
              },
              annotations: {
                summary: 'The device battery discharges in 4 hours',
                description: 'Device {$labels.object}} discharges in 2 hours.',
              },
            },
            {
              alert: 'HassDeviceUnreachable',
              expr: |||
                hass_device_available == 0
              |||,
              'for': '15m',
              labels: {
                severity: 'critical',
              },
              annotations: {
                summary: 'Device is unreachable.',
                description: 'Device {{$labels.device_name}} is unreachable for more than 15 minutes.',
              },
            },
          ] +
          (if $._config.hassEsphomeAlerts then [
             {
               alert: 'HassEsphomeDeviceLowRSSI',
               expr: 'hass_esphome_device_rssi < 60',
               'for': '5m',
               labels: {
                 severity: 'warning',
               },
               annotations: {
                 display_name: 'Device has too low RSSI',
                 description: 'Device {{$labels.device_name}} has RSSI only {{ $value }} dB.',
               },
             },
             {
               alert: 'HassEsphomeDeviceLowRSSI',
               expr: 'hass_esphome_device_rssi < 70',
               'for': '5m',
               labels: {
                 severity: 'critical',
               },
               annotations: {
                 display_name: 'Device has too low RSSI',
                 description: 'Device {{$labels.device_name}} has RSSI only {{ $value }} dB.',
               },
             },
           ] else []) +
          (if $._config.hassZhaAlerts then [
             {
               alert: 'HassZhaDeviceLowLQI',
               expr: 'hass_zha_device_lqi < 170',
               'for': '5m',
               labels: {
                 severity: 'warning',
               },
               annotations: {
                 display_name: 'Device has too low LQI',
                 description: 'Device {{$labels.device_name}} has LQI only {{ $value }}.',
               },
             },
             {
               alert: 'HassZhaDeviceLowLQI',
               expr: 'hass_zha_device_lqi < 85',
               'for': '5m',
               labels: {
                 severity: 'critical',
               },
               annotations: {
                 display_name: 'Device has too low LQI',
                 description: 'Device {{$labels.device_name}} has LQI only {{ $value }}.',
               },
             },
             {
               alert: 'HassZhaDeviceLowRSSI',
               expr: 'hass_zha_device_rssi < 60',
               'for': '5m',
               labels: {
                 severity: 'warning',
               },
               annotations: {
                 display_name: 'Device has too low RSSI',
                 description: 'Device {{$labels.device_name}} has RSSI only {{ $value }} dB.',
               },
             },
             {
               alert: 'HassZhaDeviceLowRSSI',
               expr: 'hass_zha_device_rssi < 70',
               'for': '5m',
               labels: {
                 severity: 'critical',
               },
               annotations: {
                 display_name: 'Device has too low RSSI',
                 description: 'Device {{$labels.device_name}} has RSSI only {{ $value }} dB.',
               },
             },
           ] else []) + [
          ],
      },
    ],
  },
}
