# -*- coding: utf-8 -*-
"""Module for handling geometry."""
from qgis.core import QgsCoordinateReferenceSystem
from qgis.core import QgsCoordinateTransform
from qgis.core import QgsGeometry
from qgis.core import QgsPoint

from ..dockwidget import AREA_FILTER_CURRENT_VIEW
from .constants import PAYLOAD_BBOX_KEY_TIMESERIES
from .constants import PAYLOAD_BBOX_KEY_OTHER
from .constants import WGS84


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


def add_area_filter(iface, asset_type, area_type):
    """Function to add an area filter to the payload."""
    payload = {}
    if area_type == AREA_FILTER_CURRENT_VIEW:
        if asset_type == "timeseries":
            payload_bbox_key = PAYLOAD_BBOX_KEY_TIMESERIES
        else:
            payload_bbox_key = PAYLOAD_BBOX_KEY_OTHER
        lat1, lon1, lat2, lon2 = get_bbox(iface)
        payload[payload_bbox_key] = ','.join([
            str(lat1), str(lon1), str(lat2), str(lon2)])
    return payload


def get_bbox(iface):
    """
    Get a tuple containing the bbox coordinates in the Lizard CRS.

    Args:
        (interface object) iface: QGIS interface.

    Returns:
        (tuple) bbox_bounds: A tuple containing the coordinates of
                             the southwestern and northeastern border
                             in the Lizard CRS.
    """
    # Get QGIS bbox coordinates
    south_west, north_east = get_bbox_coords(iface)
    # Get current QGIS CRS
    source_crs = get_crs(iface.mapCanvas())
    # Transform bbox from mapCanvas extent crs to the Lizard CRS
    dest_crs = WGS84
    south_west_transformed = transform_coord(south_west, source_crs, dest_crs)
    north_east_transformed = transform_coord(north_east, source_crs, dest_crs)
    # Return a tuple with the transformed coordinates
    lat1, lon1 = south_west_transformed
    lat2, lon2 = north_east_transformed
    bbox_bounds = (lat1, lon1, lat2, lon2)
    return bbox_bounds


def get_bbox_coords(iface):
    """
    Function to get the current extent of QGIS as 2 tuples.

    This function gets the coordinates of the extent of the mapCanvas of
    QGIS, and turns them into 2 tuples, containing the southwestern and
    northeastern border of the bbox.

    Args:
        (interface object) iface: QGIS interface.

    Returns:
        (tuple) south_west: A tuple containing the coordinates of the
                            southwestern border of the bounding box.
        (tuple) north_east: A tuple containing the coordinates of the
                            northeastern border of the bounding box.
    """
    # Get the coordinates of the bbox in QGIS
    x_min = iface.mapCanvas().extent().xMinimum()
    x_max = iface.mapCanvas().extent().xMaximum()
    y_min = iface.mapCanvas().extent().yMinimum()
    y_max = iface.mapCanvas().extent().yMaximum()
    # Create 2 tuples for the southwestern and northeastern border of the
    # bounding box
    south_west = (x_min, y_min)
    northeast = (x_max, y_max)
    # Return the southwestern and northeastern coordinates
    return south_west, northeast


def transform_coord(coord, source_crs, dest_crs):
    """
    Function to transform a (tuple) coordinate.

    Args:
        (tuple) coords: Tuple containing the latitude and longitude of a
                        coordinate.
        (string) source_crs: The CRS of the coordinate.
        (string) dest_crs: The CRS that will be applied to the coordinate.

    Returns:
        (tuple) coord_transformed: The transformed coordinate.
    """
    # Create QGIS CRS for the source coordinate and the destiny coordinate
    source_crs_qgs = QgsCoordinateReferenceSystem(source_crs)
    dest_crs_qgs = QgsCoordinateReferenceSystem(dest_crs)
    # Set the transformation
    transformation = QgsCoordinateTransform(source_crs_qgs, dest_crs_qgs)
    # Apply the transformation
    lat, lon = coord
    coord_transformed = transformation.transform(lat, lon)
    # Return the transformed coordinates
    return coord_transformed


def get_crs(map_canvas):
    """
    Function to get the CRS of the QGIS mapCanvas.

    Args:
        (builtin_function_or_method) map_canvas: The mapCanvas that is shown in
                                                QGIS.

    Returns:
        (string) crs: The CRS of the mapCanvas.
    """
    crs = map_canvas.mapRenderer().destinationCrs().authid()
    return crs
