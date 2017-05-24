# -*- coding: utf-8 -*-
"""Module for creating a layer."""
from PyQt4.QtCore import QVariant
from qgis.core import QgsFeature
from qgis.core import QgsField
from qgis.core import QgsMapLayerRegistry
from qgis.core import QgsVectorLayer

from .constants import ASSET_GEOMETRY_TYPES
from .constants import WGS84
from .constants import ERROR_LEVEL_WARNING
from .geometry import create_geometry
from .styler import apply_style
from .user_communication import show_message


def create_layer(asset_type, list_of_assets):
    """Function to create a new (memory) layer."""
    # Create the layer
    geometry_type = ASSET_GEOMETRY_TYPES[asset_type]
    layer = QgsVectorLayer("{}?crs={}".format(geometry_type, WGS84),
                           asset_type, "memory")
    # Add Lizard style (SVG/ QML)
    apply_style(layer, asset_type)
    # Add the layer
    QgsMapLayerRegistry.instance().addMapLayer(layer)
    # Add the attributes to the layer
    add_attributes(layer, list_of_assets)
    # Add the features to the layer
    add_features(layer, list_of_assets)
    # Return the layer
    return layer


def add_attributes(layer, assets):
    """
    Function to add attributes to the layer.

    Arguments:
        qgis_layer layer: This is a layer in QGIS.
        list assets: This is a list of assets (GeoJSONs).
    """
    # Create the attributes
    fields = [QgsField(attr, QVariant.String) for attr in assets[
        0] if attr != "geometry"]

    # Add the attributes to the layer
    layer.dataProvider().addAttributes(fields)
    layer.updateFields()


def add_features(layer, list_of_assets):
    """Function to add features to the layer."""
    # Create the feature(s)
    layer.startEditing()
    features = []
    for asset in list_of_assets:
        feature = QgsFeature(layer.pendingFields())
        try:
            geometry = asset["geometry"]
            qgs_geometry = create_geometry(geometry)
            feature.setGeometry(qgs_geometry)
        except TypeError:
            show_message("Id {} has no geometry.".format(asset['id']),
                         ERROR_LEVEL_WARNING)
        set_attributes(feature, asset)
        features.append(feature)

    # Add the features to the layer
    layer.dataProvider().addFeatures(features)
    layer.commitChanges()


def set_attributes(feature, asset):
    """
    Function to set the attributes of a QGIS feature.

    Nested assets (filters, timeseries and pumps) are taken into account.
    They are shown with ";" in between.

    Arguments:
        feature (QgsFeature): A QGIS feature to add attributes to.
        asset (JSON): A JSON, containing data about the asset.
    """
    # Create a list of values per feature
    for attribute, value in asset.iteritems():
        if attribute != "geometry":
            if attribute == "filters":
                value = ";".join(str(filters["id"]) for filters in value)
            elif attribute == "pumps":
                value = ";".join(str(pumps["id"]) for pumps in value)
            elif attribute == "timeseries":
                value = ";".join(timeseries["uuid"] for timeseries in value)
            feature.setAttribute(attribute, value)
