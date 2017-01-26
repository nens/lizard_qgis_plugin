# -*- coding: utf-8 -*-
"""Module containing the constants.

Created on: 2017-01-25
By:         Madeleine van Winkel
E-mail:     madeleine.vanwinkel@nelen-schuurmans.nl

"""
ASSET_TYPES = ["pumpstations"]
ASSET_GEOMETRY_TYPES = {"pumpstations": "Point"}

# The base_url used for getting the data (JSON)
BASE_URL = "https://demo.lizard.net/api/v2/"

# Add the reference to the CRS used in the Lizard client
WGS84 = "EPSG:4326"
