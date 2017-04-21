# -*- coding: utf-8 -*-
"""Module for getting the data from the Lizard API."""
import json
import urllib2
import urllib

from .constants import BASE_URL
from .constants import WGS84
from .geometry import get_bbox_coords
from .geometry import get_crs
from .geometry import transform_coord


def get_data(asset_type, payload):
    """Function to get the JSON from the Lizard client."""
    # Encode the payload
    payload_encoded = urllib.urlencode(payload)

    # Set the url
    url = "{}{}/?{}".format(
        BASE_URL, asset_type,
        payload_encoded)

    # Get the JSON
    response = urllib2.urlopen(url)
    r = json.load(response)
    results = r["results"]

    # Return the results
    return results


def get_bbox(iface):
    """
    Get a tuple containing the bbox coordinates in the Lizard CRS.

    Args:
        (interface object) iface: QGIS interface.

    Returns:
        (tuple) bbox_bounds: A tuple containing the coordinates of
                             the southwestern and northeastern border
                             in the Lizard CRS.
    """
    # Get QGIS bbox coordinates
    south_west, north_east = get_bbox_coords(iface)
    # Get current QGIS CRS
    source_crs = get_crs(iface.mapCanvas())
    # Transform bbox from mapCanvas extent crs to the Lizard CRS
    dest_crs = WGS84
    south_west_transformed = transform_coord(south_west, source_crs, dest_crs)
    north_east_transformed = transform_coord(north_east, source_crs, dest_crs)
    # Return a tuple with the transformed coordinates
    lat1, lon1 = south_west_transformed
    lat2, lon2 = north_east_transformed
    bbox_bounds = (lat1, lon1, lat2, lon2)
    return bbox_bounds
