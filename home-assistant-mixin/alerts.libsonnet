{
  prometheusAlerts+:: {
    groups+: [
      {
        name: 'home-assistant',
        rules:
          (if $._config.hassZhaSignalAlerts then [
             {
               alert: 'HassZhaDeviceLowLQI',
               expr: 'hass_zha_device_lqi < 170',
               'for': '5m',
               labels: {
                 severity: 'warning',
               },
               annotations: {
                 display_name: 'Device has too low LQI',
                 description: 'Device {{ $labels.device_name }} has LQI only {{ $value }}.',
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
                 description: 'Device {{ $labels.device_name }} has LQI only {{ $value }}.',
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
                 description: 'Device {{ $labels.device_name }} has RSSI only {{ $value }} dB.',
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
                 description: 'Device {{ $labels.device_name }} has RSSI only {{ $value }} dB.',
               },
             },
           ] else []) + [

          ],
      },
    ],
  },
}
