"""Basic CLI to test Home Assistant client."""
import argparse
import asyncio
import logging
import sys
from aiohttp import web

import aiohttp

from home_assistant_exporter.client_org import HomeAssistantClient
from prometheus_client import Gauge, Counter, Summary, Histogram
from prometheus_client import generate_latest, CollectorRegistry

LOGGER = logging.getLogger(__package__)

metric = {}
registry = CollectorRegistry()

metric["hass_device_info"] = Gauge(
    "device_info",
    "Information about the device.",
    ["manufacturer", "model", "sw_version", "hw_version", "id", "entity_id", "name"],
    registry=registry,
)


def get_arguments() -> argparse.Namespace:
    """Get parsed passed in arguments."""

    parser = argparse.ArgumentParser(
        description="Home Assistant simple client for Python"
    )
    parser.add_argument("--debug", action="store_true", help="Log with debug level")
    parser.add_argument(
        "url", type=str, help="URL of server, ie http://homeassistant:8123"
    )
    parser.add_argument("token", type=str, help="Long Lived Token")
    arguments = parser.parse_args()
    return arguments


async def start_cli() -> None:
    """Run main."""
    args = get_arguments()
    level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(level=level)

    async with aiohttp.ClientSession() as session:
        await connect(args, session)


async def hello(request):
    metrics = generate_latest(registry)
    return web.Response(text=metrics.decode("utf-8"))


def _get_labels(device):
    return {
        "manufacturer": device.get("manufacturer", "unknown"),
        "model": device.get("model", "unknown"),
        "sw_version": device.get("sw_version", "unknown"),
        "hw_version": device.get("hw_version", "unknown"),
        "id": device.get("id", "unknown"),
        "entity_id": device["entity_id"],
        "name": device.get("name", "unknown"),
    }


async def init_hw_info(hass):
    """
    {'entity_id': 'sensor.mi10t_battery_power', 'state': '0.82', 'attributes': {'state_class': 'measurement', 'current': 0.19287, 'voltage': 4.24, 'unit_of_measurement': 'W', 'device_class': 'power', 'icon': 'mdi:battery-plus', 'friendly_name': 'mi10t Battery Power'}, 'last_changed': '2022-09-02T13:50:20.829672+00:00', 'last_updated': '2022-09-02T13:50:20.829672+00:00', 'context': {'id': '01GBZ7F04XVHB4BD2E43EZRPCG', 'parent_id': None, 'user_id': None}, 'area_id': None, 'config_entry_id': '598503b8cba66bf08613d2af749d1ba0', 'device_id': 'fa939d9a7d730fe3ccb23cbe015139b3', 'disabled_by': None, 'has_entity_name': False, 'entity_category': 'diagnostic', 'hidden_by': None, 'icon': None, 'name': 'mi10t', 'original_name': 'mi10t Battery Power', 'platform': 'mobile_app', 'configuration_url': None, 'config_entries': ['598503b8cba66bf08613d2af749d1ba0'], 'connections': [], 'entry_type': None, 'id': 'fa939d9a7d730fe3ccb23cbe015139b3', 'identifiers': [['mobile_app', '6eb682d56ab657e0']], 'manufacturer': 'Xiaomi', 'model': 'M2007J3SY', 'name_by_user': None, 'sw_version': '31', 'hw_version': None, 'via_device_id': No
    """
    for key, device in hass.get_all_entities().items():
        try:
            metric["hass_device_info"].labels(**_get_labels(device)).set(
                device["state"]
            )
        except Exception as e:
            LOGGER.warning(f"Could not set {key} - {e}")

        # LOGGER.info(f"State: {key} - {state}")

    # for key, state in hass.states.items():
    #     LOGGER.info(f"State: {key} - {state}")
    # for key, entity in hass._entity_registry.items():
    #     LOGGER.info(f"Entity: {key} - {entity}")
    # for key, device in hass._device_registry.items():
    #     LOGGER.info(f"Device: {key} - {device}")


async def connect(args: argparse.Namespace, session: aiohttp.ClientSession) -> None:
    """Connect to the server."""
    async with HomeAssistantClient(args.url, args.token, session) as client:
        client.register_event_callback(log_events)
        await client._request_full_state()
        await init_hw_info(client)
        await asyncio.sleep(360)


def log_events(hass: HomeAssistantClient, event: str, event_data: dict) -> None:
    """Log node value changes."""

    LOGGER.info("Received event: %s", event)
    LOGGER.debug(event_data)

    if "old_state" and "new_state" in event_data:

        entity = hass.get_full_entity(event_data["entity_id"])

        try:
            metric["hass_device_info"].labels(**_get_labels(entity)).set(
                event_data["new_state"]["state"]
            )
        except Exception as e:
            LOGGER.warning(f"Could not set {entity['entity_id']} event_data - {e}")


def main() -> None:
    """Run main."""
    app = web.Application()
    app.add_routes([web.get("/", hello)])
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
