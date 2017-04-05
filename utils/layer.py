# -*- coding: utf-8 -*-
"""Module for creating a layer."""
from PyQt4.QtCore import QVariant
from qgis.core import QgsFeature
from qgis.core import QgsField
from qgis.core import QgsGeometry
from qgis.core import QgsMapLayerRegistry
from qgis.core import QgsPoint
from qgis.core import QgsVectorLayer

from .constants import ASSET_GEOMETRY_TYPES
from .constants import WGS84
from .styler import apply_style


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
        geometry = asset.pop("geometry")
        if str(geometry["type"]) == "Point":
            lat = float(geometry['coordinates'][0])
            lon = float(geometry['coordinates'][1])
            feature.setGeometry(QgsGeometry.fromPoint(QgsPoint(lat, lon)))
        elif str(geometry["type"]) == "LineString":
            lat1 = float(geometry['coordinates'][0][0])
            lon1 = float(geometry['coordinates'][0][1])
            lat2 = float(geometry['coordinates'][1][0])
            lon2 = float(geometry['coordinates'][1][1])
            feature.setGeometry(QgsGeometry.fromPolyline([
                QgsPoint(lat1, lon1),
                QgsPoint(lat2, lon2)]))
        elif str(geometry["type"]) == "Polygon":
            list_of_points = []
            for points in geometry["coordinates"]:
                for point in points:
                    lat = float(point[0])
                    lon = float(point[1])
                    list_of_points.append(QgsPoint(lat, lon))
                feature.setGeometry(QgsGeometry.fromPolygon([list_of_points]))
        elif str(geometry["type"]) == "MultiPolygon":
            list_of_polygons = []
            for polygons in geometry["coordinates"]:
                for polygon in polygons:
                    list_of_points = []
                    for point in polygon:
                        lat = float(point[0])
                        lon = float(point[1])
                        list_of_points.append(QgsPoint(lat, lon))
                    list_of_polygons.append(list_of_points)
                feature.setGeometry(QgsGeometry.fromMultiPolygon(
                    [list_of_polygons]))
        for attribute, value in asset.iteritems():
            feature.setAttribute(attribute, value)
        features.append(feature)

    # Add the features to the layer
    layer.dataProvider().addFeatures(features)
    layer.commitChanges()
