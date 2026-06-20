// dashboards — board layout. One row per group, each referencing panels from
// panels/. Consumed by pack.build as the `groups` argument.
function(panels) [
  {
    title: 'Overview',
    width: 4,
    height: 5,
    elements: {
      devices: panels.devices,
      areas: panels.areas,
      entities: panels.entities,
      entitiesAvailable: panels.entitiesAvailable,
      unavailable: panels.unavailable,
      stale: panels.stale,
    },
  },
  {
    title: 'Batteries',
    width: 8,
    height: 8,
    elements: {
      battery: panels.battery,
      batteryVoltage: panels.batteryVoltage,
      lowBattery: panels.lowBattery,
    },
  },
  {
    title: 'ESPHome (Wi-Fi)',
    width: 12,
    height: 8,
    elements: {
      esphomeRssi: panels.esphomeRssi,
      esphomeUptime: panels.esphomeUptime,
    },
  },
  {
    title: 'Zigbee (ZHA)',
    width: 6,
    height: 8,
    elements: {
      zhaRssi: panels.zhaRssi,
      zhaLqi: panels.zhaLqi,
      zhaMeshLqi: panels.zhaMeshLqi,
      zhaAvailable: panels.zhaAvailable,
    },
  },
]
