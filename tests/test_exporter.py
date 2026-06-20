"""Unit tests for the exporter's pure helpers.

These import the package (no network); the websocket client itself is exercised
against a live Home Assistant, not here. Run them in the built image or in CI
where the deps (and Python >= 3.11 for hass-client) are present.
"""
from prometheus_client import generate_latest

from home_assistant_exporter import metrics
from home_assistant_exporter.__main__ import (
    _as_float,
    _get_device_info_labels,
    _get_entity_by_ids,
)


def test_as_float():
    assert _as_float("12.5") == 12.5
    assert _as_float(3) == 3.0
    assert _as_float("on") is None
    assert _as_float(None) is None
    assert _as_float("unavailable") is None


def test_device_info_labels_tolerates_missing_fields():
    # A device missing hw/sw/name_by_user/manufacturer/model/id must not KeyError.
    labels = _get_device_info_labels({"name": "Lamp"})
    assert labels["device_name"] == "Lamp"
    assert labels["device_id"] == "Lamp"  # falls back to name when no identifier
    assert labels["manufacturer"] == ""
    assert labels["hass_id"] == ""


def test_device_info_labels_name_by_user_wins():
    labels = _get_device_info_labels({"name": "raw", "name_by_user": "Kitchen"})
    assert labels["device_name"] == "Kitchen"


def test_device_info_labels_esphome_by_manufacturer():
    labels = _get_device_info_labels({"name": "x", "manufacturer": "Espressif Inc."})
    assert labels["integration"] == "esphome"


def test_get_entity_by_ids_suffix_match():
    ents = [
        {"entity_id": "sensor.kitchen_bssid"},
        {"entity_id": "sensor.kitchen_wifi_signal"},
    ]
    assert _get_entity_by_ids(ents, ["wifi_signal"])["entity_id"].endswith("wifi_signal")
    # "_ssid" must not match "_bssid"
    assert _get_entity_by_ids(ents, ["_ssid"]) is False
    assert _get_entity_by_ids(ents, ["nope"]) is False


def test_clear_metrics_resets_label_series():
    metrics.metric["hass_entity_available"].labels(entity_id="sensor.x").set(1)
    assert "sensor.x" in generate_latest(metrics.registry).decode()
    metrics.clear_metrics()
    body = generate_latest(metrics.registry).decode()
    assert "sensor.x" not in body
    # the metric families stay registered (HELP lines remain)
    assert "# HELP hass_entity_available" in body
