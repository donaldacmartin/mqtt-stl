from dataclasses import dataclass
from datetime import datetime
from unittest import TestCase
from unittest.mock import patch

from requests import RequestException


from mqtt_stl.stl import get_departures


STOP_ID = 1234
TIME = datetime(2022, 1, 1, 12, 0)
TAG = "1N"
TITLE = "1 Nord"
ENCODING = "utf-8"

RANDOM_BYTES = b"\xf1"
INVALID_XML = "<predictions><a></predictions></a>".encode(ENCODING)
INCORRECT_XML = "<abc />".encode(ENCODING)

CORRECT_XML = f"""
<body>
    <predictions routeTag=\"{TAG}\" routeTitle=\"{TITLE}\">
        <direction title=\"0\">
            <prediction epochTime=\"{int(TIME.timestamp()) * 1000}\" />
        </direction>
    </predictions>
</body>
""".encode(ENCODING)


@dataclass
class MockResponse(object):
    ok: bool
    status_code: int
    content: bytes


class STLTest(TestCase):

    @patch("mqtt_stl.stl.get")
    def test_non_ok_response(self, requests_get):
        requests_get.return_value = MockResponse(False, 500, None)
        self.assertEqual([], get_departures(STOP_ID))

    @patch("mqtt_stl.stl.get")
    def test_request_exception(self, requests_get):
        requests_get.side_effect = RequestException("Abc")
        self.assertEqual([], get_departures(STOP_ID))

    @patch("mqtt_stl.stl.get")
    def test_unparseable_response(self, requests_get):
        requests_get.return_value = MockResponse(True, 200, RANDOM_BYTES)
        self.assertEqual([], get_departures(STOP_ID))

    @patch("mqtt_stl.stl.get")
    def test_invalid_xml(self, requests_get):
        requests_get.return_value = MockResponse(True, 200, INVALID_XML)
        self.assertEqual([], get_departures(STOP_ID))

    @patch("mqtt_stl.stl.get")
    def test_incorrect_xml(self, requests_get):
        requests_get.return_value = MockResponse(True, 200, INCORRECT_XML)
        self.assertEqual([], get_departures(STOP_ID))

    @patch("mqtt_stl.stl.get")
    def test_ok_flow(self, requests_get):
        requests_get.return_value = MockResponse(True, 200, CORRECT_XML)

        departures = get_departures(STOP_ID)

        self.assertEqual(1, len(departures))
        self.assertEqual(TAG, departures[0].tag)
        self.assertEqual(TITLE, departures[0].title)
        self.assertEqual(1, len(departures[0].departures))
        self.assertEqual(TIME, departures[0].departures[0])
