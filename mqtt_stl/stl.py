"""mqtt_stl.stl

The main interface to the STL API

Functions:
    get_departures(int) -> List[Route]
"""
from datetime import datetime
from typing import List, Optional
from xml.etree.ElementTree import Element, fromstring

from requests import get

from .model import Route


BASE_URL = "https://retro.umoiq.com/service/publicXMLFeed"
BASE_PARAMS = {"command": "predictions", "a": "stl"}
ENCODING = "utf-8"


def _get_stl_xml(stop_id: int) -> Optional[str]:
    params = BASE_PARAMS | {"stopId": stop_id}
    response = get(BASE_URL, params=params)
    return response.content.decode(ENCODING) if response.ok else None


def _parse_prediction(prediction: Element) -> datetime:
    return datetime.fromtimestamp(int(prediction.attrib["epochTime"]) / 1000)


def _parse_departures(direction: Element) -> List[datetime]:
    return [_parse_prediction(prediction) for prediction in direction]


def _parse_predictions(predictions: Element) -> Route:
    return Route(
        predictions.attrib["routeTag"],
        predictions.attrib["routeTitle"],
        _parse_departures(predictions[0]) if len(predictions) > 0 else [],
    )


def get_departures(stop_id: int) -> List[Route]:
    """Get a list of predicted departures for this stop"""

    stl_xml = _get_stl_xml(stop_id)
    xml_body = fromstring(stl_xml) if stl_xml else Element("body")
    return [_parse_predictions(predictions) for predictions in xml_body]
