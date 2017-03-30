# -*- coding: utf-8 -*-
"""Module containing the constants."""
ASSET_TYPES = ["bridges", "culverts", "leveecrosssections", "manholes",
               "outlets", "overflows", "pipes", "pressurepipes",
               "pumpstations", "wastewatertreatmentplants", "weirs"]
ASSET_GEOMETRY_TYPES = {"bridges": "Point", "culverts": "LineString",
                        "leveecrosssections": "LineString",
                        "manholes": "Point", "pipes": "LineString",
                        "pressurepipes": "LineString", "pumpstations": "Point",
                        "outlets": "Point", "overflows": "Point",
                        "wastewatertreatmentplants": "Point", "weirs": "Point"}

# The base_url used for getting the data (JSON)
BASE_URL = "https://demo.lizard.net/api/v2/"

# Add the reference to the CRS used in the Lizard client
WGS84 = "EPSG:4326"
