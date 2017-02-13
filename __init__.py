# -*- coding: utf-8 -*-
"""
/***************************************************************************
 LizardDownloader
                                 A QGIS plugin
 This plug-in helps with downloading data fromLizard in QGIS.
                             -------------------
        begin                : 2017-01-11
        copyright            : (C) 2017 by Madeleine van Winkel
        email                : madeleine.vanwinkel@nelen-schuurmans.nl
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""
import os.path
import sys

# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load LizardDownloader class from file LizardDownloader.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    sys.path.append(os.path.join(os.path.dirname(__file__), "libs",
                                 "lizard-connector"))
    from .lizard_downloader import LizardDownloader
    return LizardDownloader(iface)
