# -*- coding: utf-8 -*-
"""Module containing the constants."""

import os.path

AREA_FILTERS = ["Current view", "All data"]
ASSET_TYPES = ["bridges", "culverts", "fixeddrainagelevelareas",
               "groundwaterstations", "leveecrosssections", "manholes",
               "measuringstations", "monitoringwells", "outlets", "overflows",
               "pipes", "pressurepipes", "pumpstations", "sluices",
               "wastewatertreatmentplants", "weirs"]
ASSET_GEOMETRY_TYPES = {"bridges": "Point", "culverts": "LineString",
                        "fixeddrainagelevelareas": "Polygon",
                        "groundwaterstations": "Point",
                        "leveecrosssections": "LineString",
                        "manholes": "Point", "measuringstations": "Point",
                        "monitoringwells": "Point", "pipes": "LineString",
                        "pressurepipes": "LineString", "pumpstations": "Point",
                        "outlets": "Point", "overflows": "Point",
                        "pumpstations": "Point", "sluices": "Point",
                        "wastewatertreatmentplants": "Point", "weirs": "Point"}

# The base_url used for getting the data (JSON)
BASE_URL = "https://demo.lizard.net/api/v2/"

PAYLOAD_BBOX_KEY_TIMESERIES = "geom__within"
PAYLOAD_BBOX_KEY_OTHER = "in_bbox"
PRIVATE = "private"
PUBLIC = "public"

# Add reference to layer_styles directory
STYLES_ROOT = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                           os.path.pardir, 'layer_styles')

# Add the reference to the CRS used in the Lizard client
WGS84 = "EPSG:4326"
