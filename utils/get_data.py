# -*- coding: utf-8 -*-
"""Module for getting the data from the Lizard API.

Created on: 2017-01-25
By:         Madeleine van Winkel
E-mail:     madeleine.vanwinkel@nelen-schuurmans.nl

Functions:
    get_data(asset_type, payload)
"""
import requests

from .constants import BASE_URL


def get_data(asset_type, payload):
    """Function to get the JSON from the Lizard client."""
    # Set the url
    url = "{}{}/".format(BASE_URL, asset_type)

    # Get the JSON
    r = requests.get(url, params=payload).json()
    results = r["results"]

    # Return the results
    return results
