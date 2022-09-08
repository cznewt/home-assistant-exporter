"""Basic CLI to provide Home Assistant exporter."""
import argparse
import asyncio
import logging
import sys
from datetime import datetime
from aiohttp import web, ClientSession

from home_assistant_exporter.client import HomeAssistantClient
from home_assistant_exporter.metrics import metric, registry
from prometheus_client import generate_latest

LOGGER = logging.getLogger(__package__)

ALLOWED_DOMAINS = ["sensor", "binary_sensor"]
FORBIDDEN_INTEGRATIONS = ["adguard", "met", "moon", "hassio", "garbage_collection"]

device_registry = {}
entity_registry = {}


def get_arguments() -> argparse.Namespace:
    """Get parsed passed in arguments."""

    parser = argparse.ArgumentParser(
        description="Home Assistant simple client for Python"
    )
    parser.add_argument("--debug", action="store_true", help="Log with debug level")
    parser.add_argument(
        "url",
        type=str,
        help="URL of server, ie http://homeassistant:8123",
        nargs="?",
        const=None,
    )
    parser.add_argument(
        "token",
        type=str,
        help="Long Lived Token",
        nargs="?",
        const=None,
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


async def metrics(request):
    metrics = generate_latest(registry)
    return web.Response(text=metrics.decode("utf-8"))


async def home(request):
    page = """
        <html>
        <head><title>Home Assistant Exporter</title></head>
        <body>
        <h1>Home Assistant Exporter</h1>
        <p><a href="/metrics">Metrics</a></p>
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
        "device_id": device["id"],
        "device_name": name,
        "manufacturer": device["manufacturer"],
        "model": device["model"],
        "sw_version": sw_version,
        "hw_version": hw_version,
        "integration": integration,
        "identifier": identifier,
    }


def _get_entity_info_labels(entity):
    attrs = entity.get("attributes", {})
    if entity.get("area_id", None) == None:
        area_id = ""
    else:
        area_id = entity["area_id"]
    if entity.get("device_id", None) == None:
        device_id = ""
    else:
        device_id = entity["device_id"]

    return {
        "area_id": area_id,
        "device_id": device_id,
        "entity_id": entity["entity_id"],
        "entity_name": attrs.get("friendly_name", entity["entity_id"]),
        "class": attrs.get("device_class", ""),
        "unit": entity.get("unit_of_measurement", attrs.get("unit_of_measurement", "")),
    }


async def init_metrics(hass):

    # for id, zha_device in hass.zha_device_registry.items():
    #    LOGGER.warning(zha_device)

    # for id, area in hass.area_registry.items():
    #    LOGGER.warning(area)

    for id, device in hass.device_registry.items():
        device_labels = _get_device_info_labels(device)
        if device_labels["integration"] not in FORBIDDEN_INTEGRATIONS:
            device_registry[id] = device
            device_registry[id]["entities"] = []
            if device_labels["integration"] == "zha":
                device_registry[id]["zha"] = hass.zha_device_registry[
                    device_labels["identifier"]
                ]
                for neighbor in device_registry[id]["zha"].get("neighbors", []):
                    metric["hass_zha_mesh_lqi"].labels(
                        source_ieee=device_labels["identifier"],
                        target_ieee=neighbor["ieee"],
                    ).set(1)

                    LOGGER.info(neighbor)
            metric["hass_device_info"].labels(**device_labels).set(1)

    for id, entity in hass.get_all_entities().items():
        if id.split(".")[0] not in ALLOWED_DOMAINS:
            pass
        entity_registry[id] = entity
        if entity.get("device_id", None) in device_registry:
            device_registry[entity["device_id"]]["entities"].append(entity)
            device_registry[entity["device_id"]]["last_seen"] = entity.get(
                "last_changed", None
            )
        try:
            labels = _get_entity_info_labels(entity)
            # LOGGER.warning(labels)
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
        if "last_seen" in device and device["last_seen"] != None:
            metric["hass_device_last_seen"].labels(device_id=id).set(
                datetime.fromisoformat(device["last_seen"]).timestamp()
            )

    # LOGGER.warning(device_registry)


async def connect(args: argparse.Namespace, session: ClientSession) -> None:
    """Connect to the server."""
    async with HomeAssistantClient(args.url, args.token, session) as client:
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
    app = web.Application()
    app.add_routes([web.get("/", home)])
    app.add_routes([web.get("/metrics", metrics)])
    loop = asyncio.new_event_loop()

    try:
        loop.create_task(start_cli())
        web.run_app(app, loop=loop)
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    sys.exit(0)


if __name__ == "__main__":
    main()
