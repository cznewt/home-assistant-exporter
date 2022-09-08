from prometheus_client import Gauge, Counter
from prometheus_client import CollectorRegistry

registry = CollectorRegistry()

metric = {
    "hass_device_info": Gauge(
        "hass_device_info",
        "General information about the device",
        [
            "device_id",
            "device_name",
            "manufacturer",
            "model",
            "sw_version",
            "hw_version",
            'integration',
            'identifier',
        ],
        registry=registry,
    ),
    "hass_device_last_seen": Gauge(
        "hass_device_last_seen",
        "Last update time of entities connected to the device",
        [
            "device_id",
        ],
        registry=registry,
    ),
    "hass_device_battery_remaining": Gauge(
        "hass_device_battery_remaining",
        "The remaining percentage of device battery",
        [
            "device_id",
        ],
        registry=registry,
    ),
    "hass_esphome_device_signal_strength": Gauge(
        "hass_esphome_device_signal_strength",
        "ESPHome device signal strength with information about connected Access Point",
        [
            "device_id",
            "bssid",
            "essid",
        ],
        registry=registry,
    ),
    "hass_esphome_device_uptime": Gauge(
        "hass_esphome_device_uptime",
        "Number of seconds the device is running",
        [
            "device_id",
        ],
        registry=registry,
    ),
    "hass_zha_mesh_lqi": Gauge(
        "hass_zha_mesh_lqi",
        "LQI info of neighbouring devices connected to the Zigbee device",
        [
            "source_ieee",
            "target_ieee"
        ],
        registry=registry,
    ),
    "hass_entity_info": Gauge(
        "hass_entity_info",
        "Information about the entity.",
        [
            "entity_id",
            "entity_name",
            "area_id",
            "device_id",
            "class",
            "unit",
        ],
        registry=registry,
    ),
    "hass_entity_value": Gauge(
        "hass_entity_value",
        "Value of the entity.",
        [
            "entity_id",
        ],
        registry=registry,
    ),
    "hass_entity_available": Gauge(
        "hass_entity_available",
        "Availability of the entity value.",
        [
            "entity_id",
        ],
        registry=registry,
    ),
    "hass_entity_last_change": Gauge(
        "hass_entity_last_change",
        "Last time the entity value has changed.",
        [
            "entity_id",
        ],
        registry=registry,
    ),
    "hass_entity_last_update": Gauge(
        "hass_entity_last_update",
        "Last time the entity value has been updated.",
        [
            "entity_id",
        ],
        registry=registry,
    ),
}
