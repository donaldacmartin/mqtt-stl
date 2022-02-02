"""mqtt_stl.mqtt

The interface to the MQTT service

Functions:
    send_update(List[Route], MQTTConfig) -> None
"""
from dataclasses import asdict
from typing import List

from orjson import dumps
from paho.mqtt.client import MQTTv31
from paho.mqtt.publish import single

from .model import MQTTConfig, Route


def _to_payload(routes: List[Route]) -> str:
    dicts = [asdict(route) for route in routes]
    return dumps(dicts, default=str)


def send_update(routes: List[Route], config: MQTTConfig) -> None:
    """Publish an update to the MQTT consumer"""
    auth = (
        {"username": config.username, "password": config.password}
        if config.username
        else None
    )

    single(
        topic=config.topic,
        payload=_to_payload(routes),
        hostname=config.host,
        port=config.port,
        auth=auth,
        protocol=MQTTv31,
    )
