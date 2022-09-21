"""Home Assistant exporter main"""

import argparse
import asyncio
import logging
from sre_compile import isstring
import sys
from yaml import load, dump
from datetime import datetime
from aiohttp import web, ClientSession

from home_assistant_exporter.client import HomeAssistantClient
from home_assistant_exporter.metrics import metric, registry
from prometheus_client import generate_latest

LOGGER = logging.getLogger(__package__)

ALLOWED_DOMAINS = ["sensor", "binary_sensor"]
FORBIDDEN_INTEGRATIONS = [
    "adguard",
    "met",
    "moon",
    "hassio",
    "garbage_collection",
    "dlna_dmr",
]

device_registry = {}
entity_registry = {}


def get_arguments() -> argparse.Namespace:
    """Get parsed passed in arguments."""

    parser = argparse.ArgumentParser(description="Home Assistant Exporter")
    parser.add_argument("--debug", action="store_true", help="Log with debug level")
    parser.add_argument(
        "--hass.url",
        type=str,
        help="The URL address of target Home Assistant service.",
        dest="hass_url",
    )
    parser.add_argument(
        "--hass.token",
        type=str,
        help="The long-lived API token of target Home Assistant service.",
        dest="hass_token",
    )
    parser.add_argument(
        "--hass.mapping-config",
        type=str,
        help="Metric mapping configuration file name.",
        dest="hass_config",
    )
    parser.add_argument(
        "--web.listen-port",
        type=int,
        help="The port on which to expose the web interface and generated Prometheus metrics.",
        default=8080,
        dest="web_port",
    )
    parser.add_argument(
        "--web.telemetry-path",
        type=str,
        help="Path under which to expose metrics.",
        default="/metrics",
        dest="web_path",
    )
    arguments = parser.parse_args()
    return arguments


async def start_cli() -> None:
    """Run main."""
    args = get_arguments()
    level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(level=level)
    async with ClientSession() as session:
        await connect(args, session)


async def metrics_handler(request):
    metrics = generate_latest(registry)
    return web.Response(text=metrics.decode("utf-8"))


async def device_registry_handler(request):

    # return web.Response(text=metrics.decode("utf-8"))
    return web.json_response(device_registry)


async def home(request):
    page = """
        <html>
        <head><title>Home Assistant Exporter</title></head>
        <body>
        <h1>Home Assistant Exporter</h1>
        <p><a href="/metrics">metrics</a></p>
        </body>
        </html>
    """
    return web.Response(text=page, content_type="text/html")


def _get_device_info_labels(device):
    if device["hw_version"] == None:
        hw_version = ""
    else:
        hw_version = device["hw_version"]
    if device["sw_version"] == None:
        sw_version = ""
    else:
        sw_version = device["sw_version"]
    if device["name_by_user"] == None:
        name = device["name"]
    else:
        name = device["name_by_user"]
    identifiers = device.get("identifiers", "")
    integration = ""
    identifier = ""
    if identifiers != []:
        identifiers = identifiers[0]
        integration = identifiers[0]
        if len(identifiers) > 1:
            identifier = identifiers[1]
    else:
        if device["manufacturer"] in ["espressif", "Espressif Inc."]:
            integration = "esphome"
    return {
        "device_id": identifier if identifier is not None else name,
        "device_name": name,
        "hass_id": device["id"],
        "manufacturer": device["manufacturer"],
        "model": device["model"],
        "sw_version": sw_version,
        "hw_version": hw_version,
        "integration": integration,
    }


def _get_entity_info_labels(entity):
    attrs = entity.get("attributes", {})
    if entity.get("area_id", None) == None:
        area_id = ""
    else:
        area_id = entity["area_id"]
    if entity.get("device_id", None) == None:
        device_id = ""
        device_name = ""
    else:
        device_id = device_registry[entity.get("device_id")]["labels"]["device_id"]
        device_name = device_registry[entity.get("device_id")]["labels"]["device_name"]

    return {
        "area_id": area_id,
        "device_id": device_id,
        "device_name": device_name,
        "entity_id": entity["entity_id"],
        "entity_name": attrs.get("friendly_name", entity["entity_id"]),
        "class": attrs.get("device_class", ""),
        "unit": entity.get("unit_of_measurement", attrs.get("unit_of_measurement", "")),
    }


def _get_entity_by_ids(entities, ids):
    for entity in entities:
        for id in ids:
            if entity["entity_id"].endswith(id):
                return entity
    return False


async def init_metrics(hass):

    for id, area in hass.area_registry.items():
        metric["hass_area_info"].labels(
            area_id=area["area_id"], area_name=area["name"]
        ).set(1)

    for id, device in hass.device_registry.items():
        device_labels = _get_device_info_labels(device)
        if device_labels["integration"] not in FORBIDDEN_INTEGRATIONS:
            device_registry[id] = device
            device_registry[id]["labels"] = device_labels
            device_registry[id]["entities"] = []
            if device_labels["integration"] == "zha":
                device_registry[id]["zha"] = hass.zha_device_registry[
                    device_labels["device_id"]
                ]
                metric["hass_device_available"].labels(
                    device_id=device_labels["device_id"],
                    device_name=device_labels["device_name"],
                ).set(1 if device["zha"]["available"] else 0)
                for neighbor in device_registry[id]["zha"].get("neighbors", []):
                    metric["hass_zha_mesh_lqi"].labels(
                        source_id=device_labels["device_id"],
                        target_id=neighbor["ieee"],
                    ).set(neighbor["lqi"])
                metric["hass_zha_device_info"].labels(
                    device_id=device_labels["device_id"],
                    device_name=device_labels["device_name"],
                    device_type=device["zha"]["device_type"],
                    power_source=device["zha"]["power_source"],
                ).set(1)
                if device["zha"]["lqi"] is not None:
                    metric["hass_zha_device_lqi"].labels(
                        device_id=device_labels["device_id"],
                        device_name=device_labels["device_name"],
                    ).set(device["zha"]["lqi"])
                if device["zha"]["rssi"] is not None:
                    metric["hass_zha_device_rssi"].labels(
                        device_id=device_labels["device_id"],
                        device_name=device_labels["device_name"],
                    ).set(device["zha"]["rssi"])
                # LOGGER.info(device["zha"])

    for id, entity in hass.get_all_entities().items():
        if id.split(".")[0] not in ALLOWED_DOMAINS:
            pass
        entity_registry[id] = entity
        if entity.get("device_id", None) in device_registry:
            device_registry[entity["device_id"]]["entities"].append(entity)
            device_registry[entity["device_id"]]["last_activity"] = entity.get(
                "last_changed", None
            )
        try:
            labels = _get_entity_info_labels(entity)
            metric["hass_entity_info"].labels(**labels).set(1)
            metric["hass_entity_last_update"].labels(entity_id=id).set(
                datetime.fromisoformat(entity["last_updated"]).timestamp()
            )
            metric["hass_entity_last_change"].labels(entity_id=id).set(
                datetime.fromisoformat(entity["last_changed"]).timestamp()
            )
            if labels["unit"] != "":
                metric["hass_entity_value"].labels(entity_id=id).set(entity["state"])
        except Exception as e:
            LOGGER.warning(f"Could not set {id} - {e}")

    for id, device in device_registry.items():
        if "last_activity" in device and device["last_activity"] != None:
            metric["hass_device_last_activity"].labels(
                device_id=device["labels"]["device_id"],
                device_name=device["labels"]["device_name"],
            ).set(datetime.fromisoformat(device["last_activity"]).timestamp())

        if device["labels"]["integration"] == "esphome":
            entity_mac_address = _get_entity_by_ids(device["entities"], ["mac_address"])
            if entity_mac_address:
                device["labels"]["device_id"] = entity_mac_address["state"]

            entity_ap_essid = _get_entity_by_ids(device["entities"], ["bssid"])
            entity_ap_bssid = _get_entity_by_ids(device["entities"], ["essid"])
            entity_wifi_signal = _get_entity_by_ids(device["entities"], ["wifi_signal"])

            if entity_mac_address:
                device["labels"]["device_id"] = entity_mac_address["state"]

        entity_battery = _get_entity_by_ids(device["entities"], ["battery"])
        if entity_battery:
            # LOGGER.warning(entity_battery)
            if entity_battery["state"] != "unavailable":
                metric["hass_device_battery_remaining"].labels(
                    device_id=device["labels"]["device_id"],
                    device_name=device["labels"]["device_name"],
                ).set(entity_battery["state"])
        metric["hass_device_info"].labels(**device["labels"]).set(1)


async def connect(args: argparse.Namespace, session: ClientSession) -> None:
    """Connect to the server."""
    async with HomeAssistantClient(args.hass_url, args.hass_token, session) as client:
        client.register_event_callback(log_events)
        await client._request_full_state()
        await init_metrics(client)
        await asyncio.sleep(60)


def log_events(hass: HomeAssistantClient, event: str, event_data: dict) -> None:
    """Log node value changes."""

    LOGGER.debug("Received event: %s", event)
    LOGGER.debug(event_data)

    if "old_state" and "new_state" in event_data:

        entity = hass.get_full_entity(event_data["entity_id"])
        if entity["entity_id"].split(".")[0] in ALLOWED_DOMAINS:
            try:
                metric["hass_entity_value"].labels(entity_id=entity["entity_id"]).set(
                    event_data["new_state"]["state"]
                )
            except Exception as e:
                LOGGER.warning(f"Could not set {entity['entity_id']} event_data - {e}")


def main() -> None:
    """Run main."""
    args = get_arguments()
    app = web.Application()
    app.add_routes([web.get("/", home)])
    app.add_routes([web.get("/metrics", metrics_handler)])
    if args.debug:
        app.add_routes([web.get("/devices", device_registry_handler)])
    loop = asyncio.new_event_loop()

    try:
        loop.create_task(start_cli())
        web.run_app(app, loop=loop, port=args.web_port)
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    sys.exit(0)


if __name__ == "__main__":
    main()
