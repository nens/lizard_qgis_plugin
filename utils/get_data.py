# -*- coding: utf-8 -*-
"""Module for getting the data from the Lizard API."""
import json
import urllib2
import urllib

from .constants import BASE_URL


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
