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
    "hass_device",
    "Information about the device.",
    [
        "manufacturer",
        "model",
        "sw_version",
        "hw_version",
        "id",
        "entity_id",
        "name",
        "unit_of_measurement",
        "state_class",
        "device_class",
    ],
    registry=registry,
)


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


def _get_labels(device):
    attrs = device.get("attributes", {})
    LOGGER.debug(device)
    return {
        "manufacturer": device.get("manufacturer", "unknown"),
        "model": device.get("model", "unknown"),
        "sw_version": device.get("sw_version", "unknown"),
        "hw_version": device.get("hw_version", "unknown"),
        "id": device.get("id", "unknown"),
        "entity_id": device["entity_id"],
        "name": device.get("name", attrs.get("friendly_name", "unknown")),
        "unit_of_measurement": device.get(
            "unit_of_measurement", attrs.get("unit_of_measurement", "unknown")
        ),
        "state_class": attrs.get("state_class", "unknown"),
        "device_class": attrs.get("device_class", "unknown"),
    }


async def init_metrics(hass):
    for key, device in hass.get_all_entities().items():
        try:
            metric["hass_device_info"].labels(**_get_labels(device)).set(
                device["state"]
            )
        except Exception as e:
            LOGGER.warning(f"Could not set {key} - {e}")


async def connect(args: argparse.Namespace, session: aiohttp.ClientSession) -> None:
    """Connect to the server."""
    async with HomeAssistantClient(args.url, args.token, session) as client:
        client.register_event_callback(log_events)
        await client._request_full_state()
        await init_metrics(client)
        await asyncio.sleep(360)


def log_events(hass: HomeAssistantClient, event: str, event_data: dict) -> None:
    """Log node value changes."""

    LOGGER.debug("Received event: %s", event)
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
