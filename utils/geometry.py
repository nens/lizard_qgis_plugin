# -*- coding: utf-8 -*-
"""Module for handling geometry."""
from qgis.core import QgsGeometry
from qgis.core import QgsPoint


def apply_geometry(feature, geometry):
    """
    Function to set the geometry of a feature.

    Args:
        feature (QgsFeature): A QGIS feature on which the geometry will be
                              applied.
        geometry (dict): A geometry, containing the geometry types and the
                         coordinates that will be applied to the feature.
    """
    if str(geometry["type"]) == "Point":
        lat = float(geometry['coordinates'][0])
        lon = float(geometry['coordinates'][1])
        feature.setGeometry(QgsGeometry.fromPoint(QgsPoint(lat, lon)))
    elif str(geometry["type"]) == "LineString":
        lat1 = float(geometry['coordinates'][0][0])
        lon1 = float(geometry['coordinates'][0][1])
        lat2 = float(geometry['coordinates'][1][0])
        lon2 = float(geometry['coordinates'][1][1])
        feature.setGeometry(QgsGeometry.fromPolyline(
            [QgsPoint(lat1, lon1), QgsPoint(lat2, lon2)]))
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
