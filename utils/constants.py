# -*- coding: utf-8 -*-
"""Module containing the constants."""
ASSET_TYPES = ["bridges", "groundwaterstations", "manholes",
               "measuringstations", "monitoringwells", "outlets", "overflows",
               "pumpstations", "sluices", "wastewatertreatmentplants", "weirs"]
ASSET_GEOMETRY_TYPES = {"bridges": "Point", "groundwaterstations": "Point",
                        "manholes": "Point", "measuringstations": "Point",
                        "monitoringwells": "Point", "outlets": "Point",
                        "overflows": "Point", "pumpstations": "Point",
                        "sluices": "Point",
                        "wastewatertreatmentplants": "Point", "weirs": "Point"}

# The base_url used for getting the data (JSON)
BASE_URL = "https://demo.lizard.net/api/v2/"

# Add the reference to the CRS used in the Lizard client
WGS84 = "EPSG:4326"
