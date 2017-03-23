# -*- coding: utf-8 -*-
"""Module for creating a layer."""
import os.path

from PyQt4.QtCore import QVariant
from qgis.core import QgsFeature
from qgis.core import QgsField
from qgis.core import QgsGeometry
from qgis.core import QgsPoint
from qgis.core import QgsVectorFileWriter
from qgis.core import QgsVectorLayer

from .constants import ASSET_GEOMETRY_TYPES
from .constants import DATA_ROOT
from .constants import WGS84
from .styler import apply_style


def create_layer(self, shapefile_name, asset_type, list_of_assets):
    """Function to create a new (memory) layer."""
    # Create a memory layer
    geometry_type = ASSET_GEOMETRY_TYPES[asset_type]
    memory_layer = QgsVectorLayer("{}?crs={}".format(geometry_type, WGS84),
                                  shapefile_name, "memory")
    # Add the attributes to the memory layer
    add_attributes(memory_layer, list_of_assets)

    # Create the shapefile
    # Create the data directory ot save the shapefile if it does not exist
    if not os.path.isdir(DATA_ROOT):
        os.mkdir(DATA_ROOT)
    # Creat the path to save the shapefile
    shapefile_path = os.path.join(DATA_ROOT, "{}.shp".format(shapefile_name))
    # Create the shapefile
    create_shapefile(memory_layer, shapefile_name, shapefile_path, asset_type,
                     list_of_assets)
    # Add the shapefile_as layer to the map registry
    shapefile_layer = self.iface.addVectorLayer(
        shapefile_path, shapefile_name, "ogr")
    # Add the styling of the asset_type to the shapefile layer and shapefile
    # (QML)
    apply_style(self.dockwidget, shapefile_name, shapefile_layer, asset_type)

    # Return the shapefile layer
    return shapefile_layer


def add_attributes(layer, list_of_assets):
    """Function to add attributes to the layer."""
    # Create the attributes
    fields = [QgsField(attr, QVariant.String) for attr in list_of_assets[
        0] if attr != "geometry"]

    # Add the attributes to the layer
    layer.dataProvider().addAttributes(fields)
    layer.updateFields()


def create_shapefile(memory_layer, shapefile_name, shapefile_path,
                     asset_type, list_of_assets):
    """Function to create a shapefile."""
    # Provide the layer and fields for creating the shapefile
    provider = memory_layer.dataProvider()
    fields = provider.fields()
    # Create the shapefile
    writer = QgsVectorFileWriter(
        shapefile_path, "CP1250", fields, provider.geometryType(),
        provider.crs(), "ESRI shapefile")
    # Add the features to the shapefile
    add_features(writer, list_of_assets, asset_type)
    # Flush the shapefile to disk
    del writer


def add_features(shapefile, list_of_assets, asset_type):
    """Function to add features to the shapefile."""
    for result in list_of_assets:
        # Create the feature
        feature = QgsFeature()
        # Set the geometry of the feature
        geometry = result.pop("geometry")
        lat = float(geometry['coordinates'][0])
        lon = float(geometry['coordinates'][1])
        feature.setGeometry(QgsGeometry.fromPoint(QgsPoint(lat, lon)))
        # Create a list of values per feature
        value_list = []
        for attribute, value in result.iteritems():
            if attribute == "timeseries":
                value = ";".join(timeseries["uuid"] for timeseries in value)
            elif attribute == "pumps":
                value = ";".join(str(pumps["id"]) for pumps in value)
            value_list.append(value)
        # Add the values to the feature
        feature.setAttributes(value_list)
        # Add the feature to the shapefile
        shapefile.addFeature(feature)
