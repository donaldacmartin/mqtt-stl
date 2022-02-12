"""mqtt_stl.stl

The main interface to the STL API

Functions:
    get_departures(int) -> List[Route]
"""

from logging import debug, info, warning
from typing import List, Optional
from xml.etree.ElementTree import Element, ParseError, fromstring

from requests import RequestException, get

from .model import Route
from .transform import xml_to_route


BASE_URL = "https://retro.umoiq.com/service/publicXMLFeed"
BASE_PARAMS = {"command": "predictions", "a": "stl"}
ENCODING = "utf-8"


def _call_api(stop_id: int) -> Optional[str]:
    try:
        debug(f"Calling {BASE_URL} for stop {stop_id}")
        params = BASE_PARAMS | {"stopId": stop_id}
        response = get(BASE_URL, params=params)

        if response.ok:
            debug("Got OK response from the API")
            return response.content.decode(ENCODING)

        warning(f"Response from the API was not ok: {response.status_code}")
    except RequestException as request_exception:
        warning(f"Error communicating with the API: {request_exception}")
    except UnicodeDecodeError as decode_error:
        warning(f"Failed to decode the string to {ENCODING}: {decode_error}")

    return None


def _get_stl_xml(stop_id: int) -> Element:
    try:
        xml_str = _call_api(stop_id)

        if xml_str:
            debug(f"Parsing XML object from {xml_str}")
            return fromstring(xml_str)
    except ParseError as parse_error:
        warning(f"Failed to parse XML from API: {parse_error}")

    return Element("body")


def get_departures(stop_id: int) -> List[Route]:
    """Get a list of predicted departures for this stop"""

    info(f"Getting predicted departures for stop {stop_id}")
    stl_xml = _get_stl_xml(stop_id)
    parsed_routes = [xml_to_route(predictions) for predictions in stl_xml]
    return [route for route in parsed_routes if route]
