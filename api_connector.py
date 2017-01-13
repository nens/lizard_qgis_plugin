# -*- coding: utf-8 -*-
"""
/***************************************************************************
 LizardDownloader
                                 A QGIS plugin
 This plug-in helps with downloading data fromLizard in QGIS.
                              -------------------
        begin                : 2017-01-12
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

# Python script to connect with the Lizard API and get the [pumpstation]data
# Import libraries
import requests
import json

def getPumpstations():
	"""
	Function to return a json object with data about pump stations.
	"""

	url = "https://demo.lizard.net/api/v2/pumpstations/1/" #?format=json achter link plakken # hiermee gelijk json downloaden, niet nodig om nog hele html formatting te downloaden, sneller, maar werkt mogelijk nog niet overal(?)

	json_ = requests.get(url).json()
	print json_['geometry']['coordinates'][1]

    return json_
