from copy import deepcopy
from os import environ
from unittest import TestCase
from unittest.mock import patch

from mqtt_stl.config import get_config
from mqtt_stl.model import MQTTSTLException


ENV_VARS = {
    "MQTT_HOST": "abc123",
    "MQTT_PORT": "1883",
    "MQTT_USER": "def456",
    "MQTT_PASS": "ghi789",
    "MQTT_TOPIC": "abcdef",
    "STOP_ID": "1234",
    "POLL_DELAY_SECS": "60",
}

ENV_VARS_NO_HOST = {k: v for k, v in ENV_VARS.items() if k != "MQTT_HOST"}
ENV_VARS_NO_USER = {k: v for k, v in ENV_VARS.items() if k != "MQTT_USER"}
ENV_VARS_NO_PWD = {k: v for k, v in ENV_VARS.items() if k != "MQTT_PASS"}

ENV_VARS_BAD_PORT = {**deepcopy(ENV_VARS), **{"MQTT_PORT": "abcdef"}}
ENV_VARS_BAD_STOP_ID = {**deepcopy(ENV_VARS), **{"STOP_ID": "abcdef"}}
ENV_VARS_BAD_POLL_SECS = {**deepcopy(ENV_VARS), **{"POLL_DELAY_SECS": "abcdef"}}

EXPECTED_ERROR = "An env variable is not valid"


class ConfigTest(TestCase):
    @patch.dict(environ, ENV_VARS_NO_HOST, clear=True)
    def test_missing_parameter(self):
        with self.assertRaises(MQTTSTLException) as context:
            get_config()

        self.assertEqual("Env variable MQTT_HOST not defined", str(context.exception))

    @patch.dict(environ, ENV_VARS_BAD_PORT, clear=True)
    def test_invalid_mqtt_port(self):
        with self.assertRaises(MQTTSTLException) as context:
            get_config()

        self.assertEqual(EXPECTED_ERROR, str(context.exception))

    @patch.dict(environ, ENV_VARS_BAD_STOP_ID, clear=True)
    def test_invalid_stop_id(self):
        with self.assertRaises(MQTTSTLException) as context:
            get_config()

        self.assertEqual(EXPECTED_ERROR, str(context.exception))

    @patch.dict(environ, ENV_VARS_BAD_POLL_SECS, clear=True)
    def test_invalid_poll_secs(self):
        with self.assertRaises(MQTTSTLException) as context:
            get_config()

        self.assertEqual(EXPECTED_ERROR, str(context.exception))

    @patch.dict(environ, ENV_VARS_NO_USER, clear=True)
    def test_no_username(self):
        config = get_config()

        self.assertIsNone(config.mqtt.username)
        self.assertIsNone(config.mqtt.password)
        self.assertEqual(ENV_VARS["MQTT_HOST"], config.mqtt.host)
        self.assertEqual(int(ENV_VARS["MQTT_PORT"]), config.mqtt.port)
        self.assertEqual(ENV_VARS["MQTT_TOPIC"], config.mqtt.topic)
        self.assertEqual(int(ENV_VARS["STOP_ID"]), config.stop_id)
        self.assertEqual(int(ENV_VARS["POLL_DELAY_SECS"]), config.poll_delay_secs)

    @patch.dict(environ, ENV_VARS_NO_PWD, clear=True)
    def test_no_password(self):
        config = get_config()

        self.assertIsNone(config.mqtt.password)
        self.assertEqual(ENV_VARS["MQTT_HOST"], config.mqtt.host)
        self.assertEqual(int(ENV_VARS["MQTT_PORT"]), config.mqtt.port)
        self.assertEqual(ENV_VARS["MQTT_USER"], config.mqtt.username)
        self.assertEqual(ENV_VARS["MQTT_TOPIC"], config.mqtt.topic)
        self.assertEqual(int(ENV_VARS["STOP_ID"]), config.stop_id)
        self.assertEqual(int(ENV_VARS["POLL_DELAY_SECS"]), config.poll_delay_secs)

    @patch.dict(environ, ENV_VARS, clear=True)
    def test_ok_flow(self):
        config = get_config()

        self.assertEqual(ENV_VARS["MQTT_HOST"], config.mqtt.host)
        self.assertEqual(int(ENV_VARS["MQTT_PORT"]), config.mqtt.port)
        self.assertEqual(ENV_VARS["MQTT_USER"], config.mqtt.username)
        self.assertEqual(ENV_VARS["MQTT_PASS"], config.mqtt.password)
        self.assertEqual(ENV_VARS["MQTT_TOPIC"], config.mqtt.topic)
        self.assertEqual(int(ENV_VARS["STOP_ID"]), config.stop_id)
        self.assertEqual(int(ENV_VARS["POLL_DELAY_SECS"]), config.poll_delay_secs)
