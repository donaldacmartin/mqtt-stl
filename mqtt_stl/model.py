"""mqtt_stl.model

Providing structure to the rest of the application.

Classes:
    MQTTSTLException
    MQTTConfig
    Config
    Route
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


class MQTTSTLException(Exception):
    """Exception wrapper for the app"""


@dataclass
class MQTTConfig:
    """The config for the MQTT consumer"""

    host: str
    port: int
    username: Optional[str]
    password: Optional[str]
    topic: str


@dataclass
class Config:
    """Overall application config"""

    stop_id: int
    poll_delay_secs: int
    mqtt: MQTTConfig


@dataclass
class Route:
    """A route containing a list of expected departure times"""

    tag: str
    title: str
    departures: List[datetime]
