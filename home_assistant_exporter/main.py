#!/usr/bin/env python3

import time
import random
import asyncio
import logging
import threading
from os import _exit, environ
import yaml
from flask import Flask, Response
from prometheus_client import Gauge, Counter, Summary, Histogram
from prometheus_client import generate_latest, CollectorRegistry
from home_assistant_exporter.client import HomeAssistantClient
from aiohttp import ClientSession, TCPConnector

port = environ.get("EXPORTER_PORT", "9000")

if "EXPORTER_LOG_LEVEL" in environ:
    supported_log_levels = ["INFO", "ERROR", "DEBUG"]
    if environ["EXPORTER_LOG_LEVEL"].upper() not in supported_log_levels:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s.%(msecs)03d %(levelname)s - %(funcName)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        logger = logging.getLogger("home-assistant-exporter")
    logging.basicConfig(
        format="%(asctime)s.%(msecs)03d %(levelname)s - %(funcName)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logger = logging.getLogger("home-assistant-exporter")
    logger.setLevel(environ["EXPORTER_LOG_LEVEL"].upper())
else:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s.%(msecs)03d %(levelname)s - %(funcName)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logger = logging.getLogger("home-assistant-exporter")


def read_configuration():
    """
    Read configuration from the environmental variable EXPORTER_PATH.
    """
    if "EXPORTER_PATH" in environ:
        path = environ["EXPORTER_PATH"]
    else:
        path = "/config/.storage"
    device_config = yaml.safe_load(
        open(path + '/core.device_registry')).get('data').get('devices')
    entity_config = yaml.safe_load(
        open(path + '/core.entity_registry')).get('data').get('entities')
    return {'devices': device_config, 'entities': entity_config}



class HomeAssistantExporter:
    def __init__(self):
        """
        Initialize the flask endpoint and launch the function that will throw
        the threads that will update the metrics.
        """
        self.loop = asyncio.get_event_loop()

        self.hass = self.init_hass_client()
        self.app = Flask(__name__)
        self.metric = {}
        self.serve_metrics()
        self.init_metrics()

    async def init_hass_client(self):
        return HomeAssistantClient(
            url=environ["EXPORTER_HASS_URL"], token=environ["EXPORTER_HASS_TOKEN"],
            aiohttp_session=ClientSession(
                loop=self.loop, connector=TCPConnector(
                    enable_cleanup_closed=True)
            ))

    def init_metrics(self):
        """
        Launch the threads that will update the metrics.
        """
        self.registry = CollectorRegistry()

        self.metric['hass_device_info'] = Gauge(
            'device_info',
            'Information about the device.',
            ["manufacturer", "model", "sw_version", "hw_version", "id", "name"],
            registry=self.registry)

    def update_metrics(self):
        """
        Updates the metrics.
        """

        self.data = read_configuration()
        for device in self.data['devices']:
            kwargs = {
                'manufacturer': device['manufacturer'],
                'model': device['model'],
                'sw_version': device['sw_version'],
                'hw_version': device['hw_version'],
                'id': device['id'],
                'name': '',
            }
            self.metric['hass_device_info'].labels(**kwargs).set(1)

    def serve_metrics(self):
        """
        Main method to serve the metrics. It's used mainly to get the self
        parameter and pass it to the next function.
        """

        @self.app.route("/")
        def root():
            logger.info(self.hass.ws_server_url)

            """
            Exposes a html page with a link to the metrics.
            """
            page = """
                <html>
                <head><title>Home Assistant Exporter</title></head>
                <body>
                <h1>Home Assistant Exporter</h1>
                <p><a href="/metrics">Metrics</a></p>
                </body>
                </html>
            """
            return page

        @self.app.route("/metrics/")
        def metrics():
            """
            Plain method to expose the prometheus metrics. Every time it's
            called it will recollect the metrics and generate the rendering.
            """
            self.update_metrics()
            metrics = generate_latest(self.registry)
            return Response(metrics,
                            mimetype="text/plain",
                            content_type="text/plain; charset=utf-8")

        @self.app.route("/-/reload")
        def reload():
            """
            Stops the threads and restarts them.
            """
            self.stopped = True
            for thread in self.threads:
                thread.join()
            self.init_metrics()
            logger.info("Configuration reloaded. Metrics will be restarted.")
            return Response("OK")

    def run_webserver(self):
        """
        Launch the flask webserver on a thread.
        """
        threading.Thread(
            target=self.app.run,
            kwargs={"port": port, "host": "0.0.0.0"}
        ).start()


if __name__ == "__main__":
    PROM = HomeAssistantExporter()
    PROM.run_webserver()
