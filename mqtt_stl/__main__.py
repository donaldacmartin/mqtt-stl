"""mqtt_stl.__main__

The main entrypoint to the application

Functions:
    app() -> None
"""

from logging import DEBUG, basicConfig
from time import sleep

from .config import get_config
from .mqtt import send_update
from .stl import get_departures


LOG_FORMAT = "%(asctime)s %(levelname)-8s %(funcName)s: %(message)s"


def app() -> None:
    """Run the main application"""
    config = get_config()

    while True:
        route_departures = get_departures(config.stop_id)
        send_update(route_departures, config.mqtt)
        sleep(config.poll_delay_secs)


if __name__ == "__main__":
    basicConfig(format=LOG_FORMAT, level=DEBUG)
    app()
