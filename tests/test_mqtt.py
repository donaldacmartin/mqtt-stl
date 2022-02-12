from unittest import TestCase
from unittest.mock import patch

from paho.mqtt import MQTTException

from mqtt_stl.model import MQTTConfig, Route
from mqtt_stl.mqtt import send_update


AUTH_CONFIG = MQTTConfig("abc", 1234, "def", "ghi", "jkl")
NO_AUTH_CONFIG = MQTTConfig("abc", 123, None, None, "def")

ROUTES = [Route("abc", "def", [])]
JSON = "[{'route': {'tag': 'abc', 'title': 'def', 'departures': []}}]"


class MQTTTest(TestCase):
    @patch("mqtt_stl.mqtt.MQTTv31")
    @patch("mqtt_stl.mqtt.routes_to_json")
    @patch("mqtt_stl.mqtt.single")
    def test_send_update_with_auth(self, mqtt_single, routes_to_json, mqttv31):
        routes_to_json.return_value = JSON
        mqtt_single.return_value = ""

        send_update(ROUTES, AUTH_CONFIG)

        routes_to_json.assert_called_with(ROUTES)

        mqtt_single.assert_called_with(
            topic=AUTH_CONFIG.topic,
            payload=JSON,
            hostname=AUTH_CONFIG.host,
            port=AUTH_CONFIG.port,
            auth={"username": AUTH_CONFIG.username, "password": AUTH_CONFIG.password},
            protocol=mqttv31,
        )

    @patch("mqtt_stl.mqtt.MQTTv31")
    @patch("mqtt_stl.mqtt.routes_to_json")
    @patch("mqtt_stl.mqtt.single")
    def test_send_update_without_auth(self, mqtt_single, routes_to_json, mqttv31):
        routes_to_json.return_value = JSON
        mqtt_single.return_value = ""

        send_update(ROUTES, NO_AUTH_CONFIG)

        routes_to_json.assert_called_with(ROUTES)

        mqtt_single.assert_called_with(
            topic=NO_AUTH_CONFIG.topic,
            payload=JSON,
            hostname=NO_AUTH_CONFIG.host,
            port=NO_AUTH_CONFIG.port,
            auth=None,
            protocol=mqttv31,
        )

    @patch("mqtt_stl.mqtt.MQTTv31")
    @patch("mqtt_stl.mqtt.routes_to_json")
    @patch("mqtt_stl.mqtt.single")
    def test_send_update_error_thrown(self, mqtt_single, routes_to_json, mqttv31):
        routes_to_json.return_value = JSON
        mqtt_single.side_effect = MQTTException("abc")

        send_update(ROUTES, AUTH_CONFIG)

        routes_to_json.assert_called_with(ROUTES)

        mqtt_single.assert_called_with(
            topic=AUTH_CONFIG.topic,
            payload=JSON,
            hostname=AUTH_CONFIG.host,
            port=AUTH_CONFIG.port,
            auth={"username": AUTH_CONFIG.username, "password": AUTH_CONFIG.password},
            protocol=mqttv31,
        )
