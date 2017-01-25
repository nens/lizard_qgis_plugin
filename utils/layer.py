# -*- coding: utf-8 -*-
"""
/***************************************************************************
 LizardDownloader
                                 A QGIS plugin
 This plug-in helps with downloading data fromLizard in QGIS.
                              -------------------
        begin                : 2017-01-24
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
from PyQt4.QtCore import QVariant
from qgis.core import QgsFeature
from qgis.core import QgsField
from qgis.core import QgsGeometry
from qgis.core import QgsMapLayerRegistry
from qgis.core import QgsPoint
from qgis.core import QgsVectorLayer

from constants import ASSET_GEOMETRY_TYPES
from constants import WGS84
from styler import apply_style


def create_layer(asset_type, list_of_assets):
    """Function to create a new (memory) layer."""
    # Create the layer
    geometry_type = ASSET_GEOMETRY_TYPES[asset_type]
    layer = QgsVectorLayer("{}?crs={}".format(geometry_type, WGS84),
                           asset_type, "memory")

    # Add Lizard style (SVG)
    apply_style(layer, asset_type)

    # Add the layer
    QgsMapLayerRegistry.instance().addMapLayer(layer)

    # Add the attributes to the layer
    add_attributes(layer, list_of_assets)

    # Add the features to the layer
    add_features(layer, list_of_assets)

    # Return the layer
    return layer


def add_attributes(layer, list_of_assets):
    """Function to add attributes to the layer."""
    # Create the attributes
    fields = [QgsField(attr, QVariant.String) for attr in list_of_assets[
        0] if attr != "geometry"]

    # Add the attributes to the layer
    layer.dataProvider().addAttributes(fields)
    layer.updateFields()


def add_features(layer, list_of_assets):
    """Function to add features to the layer."""
    # Create the feature(s)
    layer.startEditing()
    features = []
    for result in list_of_assets:
        feature = QgsFeature(layer.pendingFields())
        geometry = result.pop("geometry")
        lat = float(geometry['coordinates'][0])
        lon = float(geometry['coordinates'][1])
        feature.setGeometry(QgsGeometry.fromPoint(QgsPoint(lat, lon)))
        for attribute, value in result.iteritems():
            feature.setAttribute(attribute, value)
        features.append(feature)

    # Add the features to the layer
    layer.dataProvider().addFeatures(features)
    layer.commitChanges()
