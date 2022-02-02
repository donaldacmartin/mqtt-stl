"""mqtt_stl.config

Retreive the configuration from environment variables.

Functions:
    get_config() -> Config
"""
from os import environ

from .model import Config, MQTTConfig


def get_config() -> Config:
    """Get the config from environment variables"""
    mqtt_config = MQTTConfig(
        environ["MQTT_HOST"],
        int(environ["MQTT_PORT"]),
        environ["MQTT_USER"] if "MQTT_USER" in environ else None,
        environ["MQTT_PASS"] if "MQTT_PASS" in environ else None,
        environ["MQTT_TOPIC"],
    )

    return Config(int(environ["STOP_ID"]), int(environ["POLL_DELAY_SECS"]), mqtt_config)
