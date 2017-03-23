# -*- coding: utf-8 -*-
"""Module containing the constants."""
import os.path

ASSET_TYPES = ["bridges", "manholes", "outlets", "overflows", "pumpstations",
               "wastewatertreatmentplants", "weirs"]
ASSET_GEOMETRY_TYPES = {"pumpstations": "Point", "manholes": "Point",
                        "bridges": "Point", "outlets": "Point",
                        "overflows": "Point",
                        "wastewatertreatmentplants": "Point", "weirs": "Point"}

# The base_url used for getting the data (JSON)
BASE_URL = "https://demo.lizard.net/api/v2/"

# Add reference to the data directory
DATA_ROOT = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                         os.path.pardir, 'data')
# Add reference to layer_styles directory
STYLES_ROOT = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                           os.path.pardir, 'layer_styles')

# Add the reference to the CRS used in the Lizard client
WGS84 = "EPSG:4326"
