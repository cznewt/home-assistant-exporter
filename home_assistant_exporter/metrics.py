from prometheus_client import Gauge, Counter, Info, Enum
from prometheus_client import CollectorRegistry

registry = CollectorRegistry()

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
            "hass_id",
            "manufacturer",
            "model",
            "sw_version",
            "hw_version",
            "integration",
        ],
        registry=registry,
    ),
    "hass_device_available": Gauge(
        "hass_device_available",
        "Availability of the device",
        ["device_id", "device_name"],
        registry=registry,
    ),
    "hass_device_last_activity": Gauge(
        "hass_device_last_activity",
        "Last time when entities connected to the device were updated",
        [
            "device_id",
            "device_name",
        ],
        registry=registry,
    ),
    "hass_device_battery_remaining": Gauge(
        "hass_device_battery_remaining",
        "The remaining percentage of device battery",
        [
            "device_id",
            "device_name",
        ],
        registry=registry,
    ),
    "hass_device_battery_voltage": Gauge(
        "hass_device_battery_voltage",
        "The remaining voltage of device battery",
        [
            "device_id",
            "device_name",
        ],
        registry=registry,
    ),
    "hass_device_ip_address": Gauge(
        "hass_device_ip_address",
        "IP address of the device",
        [
            "device_id",
            "device_name",
            "ip_address",
        ],
        registry=registry,
    ),
    "hass_esphome_device_info": Gauge(
        "hass_esphome_device_info",
        "ESPHome device info and information about connected WiFi AP",
        [
            "device_id",
            "device_name",
            "bssid",
            "essid",
        ],
        registry=registry,
    ),
    "hass_esphome_device_rssi": Gauge(
        "hass_esphome_device_rssi",
        "Received signal strength indicator (RSSI) of the ESPHome device",
        [
            "device_id",
            "device_name",
        ],
        registry=registry,
    ),
    "hass_esphome_device_uptime": Gauge(
        "hass_esphome_device_uptime",
        "Number of seconds the device is running",
        [
            "device_id",
            "device_name",
        ],
        registry=registry,
    ),
    "hass_zha_device_info": Gauge(
        "hass_zha_device_info",
        "General information about the Zigbee device",
        [
            "device_id",
            "device_name",
            "power_source",
            "device_type",
        ],
        registry=registry,
    ),
    "hass_zha_device_lqi": Gauge(
        "hass_zha_device_lqi",
        "The link quality indicator (LQI) of the Zigbee device",
        ["device_id", "device_name"],
        registry=registry,
    ),
    "hass_zha_device_rssi": Gauge(
        "hass_zha_device_rssi",
        "Received signal strength indicator (RSSI) of the Zigbee device",
        ["device_id", "device_name"],
        registry=registry,
    ),
    "hass_zha_mesh_lqi": Gauge(
        "hass_zha_mesh_lqi",
        "The link quality indicator (LQI) of the entire Zigbee mesh network",
        ["source_id", "target_id"],
        registry=registry,
    ),
    "hass_entity_info": Gauge(
        "hass_entity_info",
        "Information about the entity",
        [
            "entity_id",
            "entity_name",
            "area_id",
            # "area_name",
            "device_id",
            "device_name",
            "class",
            "unit",
        ],
        registry=registry,
    ),
    "hass_entity_value": Gauge(
        "hass_entity_value",
        "Value of the entity",
        [
            "entity_id",
        ],
        registry=registry,
    ),
    "hass_entity_available": Gauge(
        "hass_entity_available",
        "Availability of the entity value",
        [
            "entity_id",
        ],
        registry=registry,
    ),
    "hass_entity_last_change": Gauge(
        "hass_entity_last_change",
        "Last time the entity value has changed",
        [
            "entity_id",
        ],
        registry=registry,
    ),
    "hass_entity_last_update": Gauge(
        "hass_entity_last_update",
        "Last time the entity value has been updated",
        [
            "entity_id",
        ],
        registry=registry,
    ),
}
