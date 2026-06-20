// Estate overview panels.
function(signals) {
  devices: signals.devices.asStat('Devices'),
  areas: signals.areas.asStat('Areas'),
  entities: signals.entities.asStat('Entities'),
  entitiesAvailable: signals.entitiesAvailable.asStat('Available'),
  unavailable: signals.unavailable.asStat('Unavailable'),
  stale: signals.stale.asStat('Stale'),
}
