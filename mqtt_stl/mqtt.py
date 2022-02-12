"""mqtt_stl.mqtt

The interface to the MQTT service

Functions:
    send_update(List[Route], MQTTConfig) -> None
"""

from logging import warning
from typing import List

from paho.mqtt import MQTTException
from paho.mqtt.client import MQTTv31
from paho.mqtt.publish import single

from .model import MQTTConfig, Route
from .transform import routes_to_json


def send_update(routes: List[Route], config: MQTTConfig) -> None:
    """Publish an update to the MQTT consumer"""

    try:
        auth = (
            {"username": config.username, "password": config.password}
            if config.username
            else None
        )

        single(
            topic=config.topic,
            payload=routes_to_json(routes),
            hostname=config.host,
            port=config.port,
            auth=auth,
            protocol=MQTTv31,
        )
    except MQTTException as mqtt_exception:
        warning(f"Error publishing message: {mqtt_exception}")
