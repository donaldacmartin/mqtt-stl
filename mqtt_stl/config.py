"""mqtt_stl.config

Retreive the configuration from environment variables.

Functions:
    get_config() -> Config
"""

from os import environ

from .model import Config, MQTTConfig, MQTTSTLException


def get_config() -> Config:
    """Get the config from environment variables"""

    try:
        mqtt_config = MQTTConfig(
            environ["MQTT_HOST"],
            int(environ["MQTT_PORT"]),
            environ["MQTT_USER"] if "MQTT_USER" in environ else None,
            environ["MQTT_PASS"]
            if "MQTT_USER" in environ and "MQTT_PASS" in environ
            else None,
            environ["MQTT_TOPIC"],
        )

        return Config(
            int(environ["STOP_ID"]), int(environ["POLL_DELAY_SECS"]), mqtt_config
        )
    except KeyError as key_error:
        failing_key = key_error.args[0]
        raise MQTTSTLException(f"Env variable {failing_key} not defined") from key_error
    except ValueError as value_error:
        raise MQTTSTLException("An env variable is not valid") from value_error
