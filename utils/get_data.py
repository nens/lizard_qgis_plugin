# -*- coding: utf-8 -*-
"""
/***************************************************************************
 LizardDownloader
                                 A QGIS plugin
 This plug-in helps with downloading data fromLizard in QGIS.
                              -------------------
        begin                : 2017-01-25
        git sha              : $Format:%H$
        copyright            : (C) 2017 by Madeleine van Winkel
        email                : madeleine.vanwinkel@nelen-schuurmans.nl
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

# Import
import requests

from constants import BASE_URL


def get_data(asset_type, payload):
    """Function to get the JSON from the Lizard client."""
    # Set the url
    url = "{}{}/".format(BASE_URL, asset_type)

    # Get the JSON
    r = requests.get(url, params=payload).json()
    results = r["results"]

    # Return the results
    return results
