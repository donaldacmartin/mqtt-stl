"""mqtt_stl.model

Providing structure to the rest of the application.

Classes:
    MQTTConfig
    Config
    Route
"""
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


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
    depatures: List[datetime]
