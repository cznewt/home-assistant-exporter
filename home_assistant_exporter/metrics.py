from prometheus_client import Gauge, Counter
from prometheus_client import CollectorRegistry

registry = CollectorRegistry()
metric = {
    "hass_device_info": Gauge(
        "hass_device_info",
        "General information about the device",
        [
            "manufacturer",
            "model",
            "sw_version",
            "hw_version",
            "device",
            "name",
            'integration',
            'identifier',
        ],
        registry=registry,
    ),
    "hass_device_last_seen": Gauge(
        "hass_device_last_seen",
        "Last update time of entities connected to the device",
        [
            "device",
        ],
        registry=registry,
    ),
    "hass_device_battery_remaining": Gauge(
        "hass_device_battery_remaining",
        "The remaining percentage of device battery",
        [
            "device",
        ],
        registry=registry,
    ),
    "hass_esphome_device_signal_strength": Gauge(
        "hass_esphome_device_signal_strength",
        "ESPHome device signal strength with information about connected Access Point",
        [
            "device",
            "bssid",
            "essid",
        ],
        registry=registry,
    ),
    "hass_esphome_device_uptime": Gauge(
        "hass_esphome_device_uptime",
        "Number of seconds the device is running",
        [
            "device",
        ],
        registry=registry,
    ),
    "hass_device_zha_mesh_lqi": Gauge(
        "hass_device_zha_connection_lqi",
        "LQI info of neighbouring devices connected to the Zigbee device",
        [
            "device",
            "neighbour"
        ],
        registry=registry,
    ),
    "hass_entity_info": Gauge(
        "hass_entity_info",
        "Information about the entity.",
        [
            "entity",
            "area",
            "device",
            "class",
            "unit",
        ],
        registry=registry,
    ),
    "hass_entity_value": Gauge(
        "hass_entity_value",
        "Value of the entity.",
        [
            "entity",
        ],
        registry=registry,
    ),
    "hass_entity_available": Gauge(
        "hass_entity_available",
        "Availability of the entity value.",
        [
            "entity",
        ],
        registry=registry,
    ),
    "hass_entity_changed": Gauge(
        "hass_entity_changed",
        "Last time the entity value has changed.",
        [
            "entity",
        ],
        registry=registry,
    ),
    "hass_entity_updated": Gauge(
        "hass_entity_updated",
        "Last time the entity value has been updated.",
        [
            "entity",
        ],
        registry=registry,
    ),
}
