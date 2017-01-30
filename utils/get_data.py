# -*- coding: utf-8 -*-
"""Module for getting the data from the Lizard API."""
import json
import urllib2

from .constants import BASE_URL


def get_data(asset_type, payload):
    """Function to get the JSON from the Lizard client."""
    # Set the payload key
    page_size = payload.keys()[0]

    # Set the url
    url = "{}{}/?{}={}".format(
        BASE_URL, asset_type,
        page_size, payload[page_size])

    # # Get the JSON
    response = urllib2.urlopen(url)
    r = json.load(response)
    results = r["results"]
    # count = r["count"]

    # Return the results
    return results
