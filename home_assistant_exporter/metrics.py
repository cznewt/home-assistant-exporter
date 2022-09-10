from prometheus_client import Gauge, Counter, Info, Enum
from prometheus_client import CollectorRegistry

registry = CollectorRegistry()

ID_SUFFIX = "id"

metric = {
    "hass_area_info": Gauge(
        "hass_area_info",
        "General information about the area",
        [
            "area_id",
            "area_name",
        ],
        registry=registry,
    ),
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
            "integration",
            "identifier",
        ],
        registry=registry,
    ),
    "hass_device_last_activity": Gauge(
        "hass_device_last_activity",
        "Last time of entities connected to the device were updated",
        [
            f"device_{ID_SUFFIX}",
        ],
        registry=registry,
    ),
    "hass_device_battery_remaining": Gauge(
        "hass_device_battery_remaining",
        "The remaining percentage of device battery",
        [
            f"device_{ID_SUFFIX}",
        ],
        registry=registry,
    ),
    "hass_esphome_device_signal_strength": Gauge(
        "hass_esphome_device_signal_strength",
        "ESPHome device signal strength with information about connected WiFi AP",
        [
            f"device_{ID_SUFFIX}",
            "bssid",
            "essid",
        ],
        registry=registry,
    ),
    "hass_esphome_device_uptime": Gauge(
        "hass_esphome_device_uptime",
        "Number of seconds the device is running",
        [
            f"device_{ID_SUFFIX}",
        ],
        registry=registry,
    ),
    "hass_zha_device_info": Gauge(
        "hass_zha_device_info",
        "General information about the Zigbee device",
        [
            f"device_{ID_SUFFIX}",
            "power_source",
            "device_type",
        ],
        registry=registry,
    ),
    "hass_zha_device_lqi": Gauge(
        "hass_zha_device_lqi",
        "The link quality indicator (LQI) of the Zigbee device is an indication of the quality of the data packets received by the receiver",
        [
            f"device_{ID_SUFFIX}",
        ],
        registry=registry,
    ),
    "hass_zha_device_rssi": Gauge(
        "hass_zha_device_rssi",
        "Received signal strength indicator (RSSI) of the Zigbee device is a measurement of the power present in a received radio signal",
        [
            f"device_{ID_SUFFIX}",
        ],
        registry=registry,
    ),
    "hass_zha_mesh_lqi": Gauge(
        "hass_zha_mesh_lqi",
        "The link quality indicator (LQI) of the entire Zigbee mesh network",
        ["source_ieee", "target_ieee"],
        registry=registry,
    ),
    "hass_entity_info": Gauge(
        "hass_entity_info",
        "Information about the entity",
        [
            "entity_id",
            "entity_name",
            f"area_{ID_SUFFIX}",
            f"device_{ID_SUFFIX}",
            "class",
            "unit",
        ],
        registry=registry,
    ),
    "hass_entity_value": Gauge(
        "hass_entity_value",
        "Value of the entity",
        [
            f"entity_{ID_SUFFIX}",
        ],
        registry=registry,
    ),
    "hass_entity_available": Gauge(
        "hass_entity_available",
        "Availability of the entity value",
        [
            f"entity_{ID_SUFFIX}",
        ],
        registry=registry,
    ),
    "hass_entity_last_change": Gauge(
        "hass_entity_last_change",
        "Last time the entity value has changed",
        [
            f"entity_{ID_SUFFIX}",
        ],
        registry=registry,
    ),
    "hass_entity_last_update": Gauge(
        "hass_entity_last_update",
        "Last time the entity value has been updated",
        [
            f"entity_{ID_SUFFIX}",
        ],
        registry=registry,
    ),
}
