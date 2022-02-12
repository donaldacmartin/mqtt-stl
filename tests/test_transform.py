from datetime import datetime
from unittest import TestCase
from xml.etree.ElementTree import fromstring

from mqtt_stl.model import Route
from mqtt_stl.transform import routes_to_json, xml_to_route


EXPECTED_TIME = datetime(2022, 1, 1, 12, 0)
EXPECTED_TAG = "1N"
EXPECTED_TITLE = "1 Nord"


XML_NO_TAG = f'<predictions routeTitle="{EXPECTED_TITLE}" />'
XML_NO_TITLE = f'<predictions routeTag="{EXPECTED_TAG}" />'
XML_NO_DEPS = f'<predictions routeTag="{EXPECTED_TAG}" routeTitle="{EXPECTED_TITLE}" />'

XML_NO_TIMESTAMP = f"""
<predictions routeTag=\"{EXPECTED_TAG}\" routeTitle=\"{EXPECTED_TITLE}\">
    <direction title=\"0\">
        <prediction />
    </direction>
</predictions>
"""

XML_INVALID_TIMESTAMP = f"""
<predictions routeTag=\"{EXPECTED_TAG}\" routeTitle=\"{EXPECTED_TITLE}\">
    <direction title=\"0\">
        <prediction epochTime=\"abc\" />
    </direction>
</predictions>
"""

XML_OK = f"""
<predictions routeTag=\"{EXPECTED_TAG}\" routeTitle=\"{EXPECTED_TITLE}\">
    <direction title=\"0\">
        <prediction epochTime=\"{int(EXPECTED_TIME.timestamp()) * 1000}\" />
    </direction>
</predictions>
"""


DEPARTURE = datetime.now()
DEPARTURE_STR = DEPARTURE.isoformat()
ROUTE = Route("abc", "def", [DEPARTURE])
ROUTES = [ROUTE]

EMPTY_JSON = "[]".encode("utf-8")
JSON = f'[{{"tag":"{ROUTE.tag}","title":"{ROUTE.title}","departures":["{DEPARTURE_STR}"]}}]'.encode(
    "utf-8"
)


class XMLToRouteTest(TestCase):
    def test_no_route_tag(self):
        route = xml_to_route(fromstring(XML_NO_TAG))

        self.assertEqual(EXPECTED_TITLE, route.title)
        self.assertEqual(0, len(route.departures))
        self.assertIsNone(route.tag)

    def test_no_title(self):
        route = xml_to_route(fromstring(XML_NO_TITLE))

        self.assertEqual(EXPECTED_TAG, route.tag)
        self.assertEqual(0, len(route.departures))
        self.assertIsNone(route.title)

    def test_no_departures(self):
        route = xml_to_route(fromstring(XML_NO_DEPS))

        self.assertEqual(EXPECTED_TAG, route.tag)
        self.assertEqual(EXPECTED_TITLE, route.title)
        self.assertEqual(0, len(route.departures))

    def test_departure_no_timestamp(self):
        route = xml_to_route(fromstring(XML_NO_TIMESTAMP))

        self.assertEqual(EXPECTED_TAG, route.tag)
        self.assertEqual(EXPECTED_TITLE, route.title)
        self.assertEqual(0, len(route.departures))

    def test_departure_invalid_timestamp(self):
        route = xml_to_route(fromstring(XML_INVALID_TIMESTAMP))

        self.assertEqual(EXPECTED_TAG, route.tag)
        self.assertEqual(EXPECTED_TITLE, route.title)
        self.assertEqual(0, len(route.departures))

    def test_ok_flow(self):
        route = xml_to_route(fromstring(XML_OK))

        self.assertEqual(EXPECTED_TAG, route.tag)
        self.assertEqual(EXPECTED_TITLE, route.title)
        self.assertEqual(1, len(route.departures))
        self.assertEqual(EXPECTED_TIME, route.departures[0])


class RoutesToJsonTest(TestCase):
    def test_no_routes(self):
        self.assertEqual(EMPTY_JSON, routes_to_json([]))

    def test_routes(self):
        self.assertEqual(JSON, routes_to_json(ROUTES))
