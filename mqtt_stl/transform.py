"""mqtt_stl.transform

Utilities for transforming XML to objects and objects to JSON

Functions:
    xml_to_route(Element) -> Optional[Route]
    routes_to_json(List[Route]) -> str
"""

from dataclasses import asdict
from datetime import datetime
from logging import warning
from typing import List, Optional
from xml.etree.ElementTree import Element

from orjson import dumps  # pylint: disable=no-name-in-module

from .model import Route


def _parse_prediction(prediction: Element) -> Optional[datetime]:
    try:
        timestamp = int(prediction.attrib["epochTime"]) / 1000
        return datetime.fromtimestamp(timestamp)
    except ValueError as value_error:
        warning(f"Could not parse timestamp: {value_error}")
    except KeyError:
        warning(f"Prediction does not have an epochTime: has {prediction.attrib}")

    return None


def _parse_departures(direction: Element) -> List[datetime]:
    parsed_departures = [_parse_prediction(prediction) for prediction in direction]
    return [departure for departure in parsed_departures if departure]


def xml_to_route(predictions: Element) -> Optional[Route]:
    """Parses an XML node to a route, or returns nothing"""

    return Route(
        predictions.attrib["routeTag"] if "routeTag" in predictions.attrib else None,
        predictions.attrib["routeTitle"]
        if "routeTitle" in predictions.attrib
        else None,
        _parse_departures(predictions[0]) if len(predictions) > 0 else [],
    )


def routes_to_json(routes: List[Route]) -> bytes:
    """Convert a list of routes to JSON"""

    dicts = [asdict(route) for route in routes] if routes else []
    return dumps(dicts, default=str)
