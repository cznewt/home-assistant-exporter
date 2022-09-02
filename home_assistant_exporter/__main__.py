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
    ["manufacturer", "model", "sw_version", "hw_version", "id", "name"],
    registry=registry,
)
metric["hass_device_state"] = Gauge(
    "device_state",
    "Information about the device.",
    ["entity_id"],
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


async def connect(args: argparse.Namespace, session: aiohttp.ClientSession) -> None:
    """Connect to the server."""
    async with HomeAssistantClient(args.url, args.token, session) as client:
        client.register_event_callback(log_events)
        await client._request_full_state()
        LOGGER.debug(client._device_registry)
        await asyncio.sleep(360)


def log_events(hass: HomeAssistantClient, event: str, event_data: dict) -> None:
    """Log node value changes."""

    LOGGER.info("Received event: %s", event)
    LOGGER.debug(event_data)

    if "old_state" and "new_state" in event_data:
        try:
            metric["hass_device_state"].labels(event_data["entity_id"]).set(
                event_data["new_state"]["state"]
            )
        except Exception as e:
            LOGGER.warning(f"Could not set {event_data} event_data")


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
