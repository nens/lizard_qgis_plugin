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
DATETIME_PATTERN = "%Y-%m-%d %H:%M:%S"
RASTER_TYPES = [
    'DEM Netherlands',
    'Land use',
    'Rain'
]
RASTER_WINDOWS = {
    '5min': 300,
    'hour': 3600,
    'day': 86400
}
RASTER_INFO = {
    'DEM Netherlands': {
        'uuid': '1d65a4e1-ac2f-4e66-9e52-1d130d870a34',
        'raster_name': 'Hoogte',
        'temporal': False
    },
    'Land use': {
        'uuid': 'b464c2e4-b1f4-4af4-b9b8-6282461e941e',
        'raster_name': 'Landgebruik (oud)',
        'temporal': False,
    },
    'Rain': {
        'uuid': '730d6675-35dd-4a35-aa9b-bfb8155f9ca7',
        'raster_name': 'Regen',
        'temporal': True,
    }
}

DATA_TYPES = ASSET_TYPES + RASTER_TYPES

# The base_url used for getting the data (JSON)
BASE_URL = "https://demo.lizard.net/api/v2/"

ERROR_LEVEL_CRITICAL = "Critical"
ERROR_LEVEL_WARNING = "Warning"
ERROR_LEVEL_INFO = "Info"
ERROR_LEVEL_SUCCESS = "Success"

PAYLOAD_BBOX_KEY_TIMESERIES = "geom__within"
PAYLOAD_BBOX_KEY_OTHER = "in_bbox"

# Add reference to layer_styles directory
STYLES_ROOT = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                           os.path.pardir, 'layer_styles')

# Add the reference to the CRS used in the Lizard client
WGS84 = "EPSG:4326"
