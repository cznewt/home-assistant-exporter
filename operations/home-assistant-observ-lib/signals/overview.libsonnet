// Estate overview signals.
local mksig = import './signal.libsonnet';

function(this)
  local sig = mksig(this);
  {
    devices: sig('Devices', 'count(hass_device_info{%(queriesSelector)s})', 'short', 'Registered devices.'),
    areas: sig('Areas', 'count(hass_area_info{%(queriesSelector)s})', 'short', 'Configured areas.'),
    entities: sig('Entities', 'count(hass_entity_info{%(queriesSelector)s})', 'short', 'Registered entities.'),
    entitiesAvailable: sig('Entities available', 'avg(hass_entity_available{%(queriesSelector)s})', 'percentunit', 'Fraction of entities reporting available.'),
    unavailable: sig('Unavailable entities', 'count(hass_entity_available{%(queriesSelector)s} == 0)', 'short', 'Entities currently unavailable.'),
    stale: sig('Stale entities', 'count((time() - hass_entity_last_update{%(queriesSelector)s}) > ' + this.staleSeconds + ')', 'short', 'Entities not updated within the stale window.'),
  }
