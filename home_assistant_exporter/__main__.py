"""Basic CLI to test Home Assistant client."""
import argparse
import asyncio
import logging
from os import device_encoding
import sys
from aiohttp import web

from datetime import datetime

import aiohttp

from home_assistant_exporter.client_org import HomeAssistantClient
from prometheus_client import Gauge, Counter, Summary, Histogram
from prometheus_client import generate_latest, CollectorRegistry

LOGGER = logging.getLogger(__package__)

ALLOWED_DOMAINS = ['sensor', 'binary_sensor']
FORBIDDEN_INTEGRATIONS = ['met', 'moon']

device_registry = {}
entity_registry = {}
registry = CollectorRegistry()
metric = {
    "hass_device_info": Gauge(
        "hass_device_info",
        "Information about the device.",
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
    "hass_device_esphome_signal_strength": Gauge(
        "hass_device_esphome_signal_strength",
        "Information about the device.",
        [
            "device",
            "essid",
        ],
        registry=registry,
    ),
    "hass_device_esphome_uptime": Gauge(
        "hass_device_esphome_uptime",
        "Information about the device.",
        [
            "device",
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
            "unit_of_measurement",
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


def get_arguments() -> argparse.Namespace:
    """Get parsed passed in arguments."""

    parser = argparse.ArgumentParser(
        description="Home Assistant simple client for Python"
    )
    parser.add_argument("--debug", action="store_true",
                        help="Log with debug level")
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
    async with aiohttp.ClientSession() as session:
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


def _get_device_labels(device):
    if device['hw_version'] == None:
        hw_version = ''
    else:
        hw_version = device['hw_version']
    if device['sw_version'] == None:
        sw_version = ''
    else:
        sw_version = device['sw_version']
    if device['name_by_user'] == None:
        name = device['name']
    else:
        name = device['name_by_user']
    LOGGER.warning(device.get('identifiers'))
    identifiers = device.get('identifiers', '')
    integration = ''
    identifier = ''
    if identifiers != []:
        identifiers = identifiers[0]
        integration = identifiers[0]
        if len(identifiers) > 1:
            identifier = identifiers[1]
    else:
        if device['model'].startswith("PLATFORMIO"):
            integration = 'esphome'
    return {
        'manufacturer': device['manufacturer'],
        'model': device['model'],
        'sw_version': sw_version,
        'hw_version': hw_version,
        'device': device['id'],
        'name': name,
        'integration': integration,
        'identifier': identifier,
    }


def _get_entity_labels(entity):
    attrs = entity.get("attributes", {})
    # LOGGER.warning(entity)
    return {
        "area": entity.get("area_id", ''),
        "device": entity.get("device_id", ''),
        "entity": entity["entity_id"],
        "unit_of_measurement": entity.get(
            "unit_of_measurement", attrs.get("unit_of_measurement", "")
        ),
        "class": attrs.get("device_class", ""),
    }


async def init_metrics(hass):

    # for id, area in hass.area_registry.items():
    #    LOGGER.warning(area)

    for id, device in hass.device_registry.items():
        device_labels = _get_device_labels(device)
        if device_labels['integration'] not in FORBIDDEN_INTEGRATIONS:
            device_registry[id] = device
            device_registry[id]['entities'] = []
            metric['hass_device_info'].labels(**device_labels).set(1)

    for id, entity in hass.get_all_entities().items():
        if id.split('.')[0] not in ALLOWED_DOMAINS:
            pass
        entity_registry[id] = entity
        if entity.get('device_id', None) in device_registry:
            device_registry[entity['device_id']]['entities'].append(entity)
        try:
            labels = _get_entity_labels(entity)
            # LOGGER.warning(labels)
            metric["hass_entity_info"].labels(**labels).set(1)
            metric["hass_entity_updated"].labels(entity=id).set(
                datetime.fromisoformat(entity['last_updated']).timestamp()
            )
            metric["hass_entity_changed"].labels(entity=id).set(
                datetime.fromisoformat(entity['last_changed']).timestamp()
            )
            if labels['unit_of_measurement'] != '':
                metric["hass_entity_value"].labels(entity=id).set(
                    entity["state"]
                )
        except Exception as e:
            LOGGER.warning(f"Could not set {id} - {e}")
    # LOGGER.warning(device_registry)


async def connect(args: argparse.Namespace, session: aiohttp.ClientSession) -> None:
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
        if entity['entity_id'].split('.')[0] in ALLOWED_DOMAINS:
            try:
                metric["hass_entity_value"].labels(entity=entity['entity_id']).set(
                    event_data["new_state"]["state"]
                )
            except Exception as e:
                LOGGER.warning(
                    f"Could not set {entity['entity_id']} event_data - {e}")


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
