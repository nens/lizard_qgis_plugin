# -*- coding: utf-8 -*-
"""Module for handling geometry."""
from qgis.core import QgsGeometry
from qgis.core import QgsPoint


def create_geometry(geometry):
    """
    Function to create a QGIS geometry.

    Arguments:
        geometry (dict): Geometry, containing the geometry types and the
                         coordinates that will be used to create the geometry.
    """
    geometry_type = geometry["type"]
    if geometry_type == "Point":
        lat = float(geometry['coordinates'][0])
        lon = float(geometry['coordinates'][1])
        return QgsGeometry.fromPoint(QgsPoint(lat, lon))
    elif geometry_type == "LineString":
        list_of_points = []
        for point in geometry["coordinates"]:
            lat = float(point[0])
            lon = float(point[1])
            list_of_points.append(QgsPoint(lat, lon))
        return QgsGeometry.fromPolyline(list_of_points)
    elif geometry_type == "Polygon":
        list_of_polygon_boundaries = []
        for polygon_boundary in geometry["coordinates"]:
            list_of_points = []
            for point in polygon_boundary:
                lat = float(point[0])
                lon = float(point[1])
                list_of_points.append(QgsPoint(lat, lon))
            list_of_polygon_boundaries.append(list_of_points)
        return QgsGeometry.fromPolygon(list_of_polygon_boundaries)
    elif geometry_type == "MultiPolygon":
        list_of_polygons = []
        for polygon in geometry["coordinates"]:
            list_of_polygon_boundaries = []
            for polygon_boundary in polygon:
                list_of_points = []
                for point in polygon_boundary:
                    lat = float(point[0])
                    lon = float(point[1])
                    list_of_points.append(QgsPoint(lat, lon))
                list_of_polygon_boundaries.append(list_of_points)
            list_of_polygons.append(list_of_polygon_boundaries)
        return QgsGeometry.fromMultiPolygon(list_of_polygons)
