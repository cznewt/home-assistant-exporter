from hass_client import HomeAssistantClient
from typing import Any, Awaitable, Callable, Dict, List, Optional, Union


class HomeAssistantClient(HomeAssistantClient):
    def __init__(self, *args, **kwargs):
        self._states = {}
        self._zha_device_registry = {}
        self._device_registry = {}
        self._entity_registry = {}
        self._area_registry = {}
        super().__init__(*args, **kwargs)

    async def _request_full_state(self):
        """Request full state."""
        for item in await self.send_command("zha/devices"):
            # item_id = item["ieee"]
            item_id = item["ieee"]
            # if "00:15:8d:00:04:05:72:6a" == item_id:
            #     raise Exception(item)
            self._zha_device_registry[item_id] = item
        for item in await self.get_states():
            entity_id = item["entity_id"]
            self._states[entity_id] = item

        # Request area registry
        for item in await self.get_area_registry():
            item_id = item["area_id"]
            self._area_registry[item_id] = item

        # Request device registry
        for item in await self.get_device_registry():
            item_id = item["id"]
            self._device_registry[item_id] = item
        # Request entity registry
        for item in await self.get_entity_registry():
            item_id = item["entity_id"]
            self._entity_registry[item_id] = item
        # Request ZHA device registry

        # raise Exception(self._entity_registry)

    @property
    def zha_device_registry(self) -> dict:
        """Return ZHA device registry."""
        if not self._zha_device_registry:
            raise NotConnected("Please call connect first.")
        return self._zha_device_registry

    @property
    def device_registry(self) -> dict:
        """Return device registry."""
        if not self._device_registry:
            raise NotConnected("Please call connect first.")
        return self._device_registry

    @property
    def entity_registry(self) -> dict:
        """Return device registry."""
        if not self._entity_registry:
            raise NotConnected("Please call connect first.")
        return self._entity_registry

    @property
    def area_registry(self) -> dict:
        """Return device registry."""
        if not self._area_registry:
            raise NotConnected("Please call connect first.")
        return self._area_registry

    @property
    def states(self) -> dict:
        """Return all hass states."""
        if not self._states:
            raise NotConnected("Please call connect first.")
        return self._states

    @property
    def lights(self) -> List[dict]:
        """Return all light entities."""
        return self.items_by_domain("light")

    @property
    def switches(self) -> List[dict]:
        """Return all switch entities."""
        return self.items_by_domain("switch")

    @property
    def media_players(self) -> List[dict]:
        """Return all media_player entities."""
        return self.items_by_domain("media_player")

    @property
    def sensors(self) -> List[dict]:
        """Return all sensor entities."""
        return self.items_by_domain("sensor")

    @property
    def binary_sensors(self) -> List[dict]:
        """Return all binary_sensor entities."""
        return self.items_by_domain("binary_sensor")

    def items_by_domain(self, domain: str) -> List[dict]:
        """Retrieve all items for a domain."""
        if not self.connected:
            raise NotConnected("Please call connect first.")
        return [value for key, value in self._states.items() if key.startswith(domain)]

    def get_full_entity(self, entity_id: str):
        entity = self.states.get(entity_id, {}) | self.entity_registry.get(
            entity_id, {}
        )

        device_id = entity.get("device_id", None)
        return entity | self.device_registry.get(device_id, {})

    def get_all_entities(self) -> dict:
        return {key: self.get_full_entity(key) for key, state in self.states.items()}
