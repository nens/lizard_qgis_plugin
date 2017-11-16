# -*- coding: utf-8 -*-
"""
Mostly copied from the threedi radar rain module.
"""
import logging
import math
import os
import tempfile
import urllib
import urllib2
import urlparse

from .constants import RASTER_INFO
from .get_data import use_header

# 1 pixel is 1 km x 1 km, so we should be good for now; if rain resolution
# increases, we might want to redefine this desired array size
DESIRED_ARRAY_SIZE_FOR_RASTER_REQUEST = 512  # for width and height

logger = logging.getLogger(__name__)


def determine_zoomlevel(
        width, height, desired_size=DESIRED_ARRAY_SIZE_FOR_RASTER_REQUEST):
    """
    Calculate a zoom level for the given width, height and the desired array
    size (in one dimension).
    """
    total_pixels = width * height
    return math.sqrt(total_pixels / (desired_size ** 2))


def calc_request_width_height(bbox):
    """
    Set parameters used for rain request: zoomlevel, request_width and
    request_height.
    """
    zoomlevel = determine_zoomlevel(bbox.width, bbox.height)
    # use a scaled raster width and height for the rain radar request
    request_width = int(math.ceil(bbox.width / zoomlevel))
    request_height = int(math.ceil(bbox.height / zoomlevel))
    return (request_width, request_height)


class BoundingBox(object):
    """BoundingBox class."""

    GEOM = 'POLYGON (({x1} {y1},{x2} {y1},{x2} {y2},{x1} {y2},{x1} {y1}))'

    def __init__(self, extent):
        """
        Initializer method.
        :param extent: tuple of bbox coordinates (xmin, ymin, xmax, ymax):
            xmin,ymax     xmax,ymax
                +-------------+
                |             |
                |             |
                +-------------+
            xmin,ymin     xmax,ymin
        """

        self.xmin, self.ymin, self.xmax, self.ymax = extent
        self.width = abs(self.xmax - self.xmin)
        self.height = abs(self.ymax - self.ymin)
        self.geom = self.GEOM.format(
            x1=self.xmin, y1=self.ymin, x2=self.xmax, y2=self.ymax)


def fetch_layer_from_server(
        bbox, width, height, dt=None, srs='epsg:4326',
        layer='DEM (Netherlands)', username=None, password=None,
        server='https://demo.lizard.net/api/v3/rasters/'):
    """
    Fetches rain data from raster server.
    :param bbox: instance of BoundingBox class
    :param width/height: request width and height in pixels; the response
        width and height will be the same
    :param dt: datetime instance used for the time parameter for
        the raster store request
    :param srs: epsg string (default = 'epsg:4326' (wgs84))
    :param layer: get parameters specifying the requested layer from the
        raster store
    :param server: server used for the raster store request
    :param resolution: temporal resolution of the requested layer in seconds
    :return error code and numpy instance of the rain radar data (or None in
        case of an error)
    """
    logger.debug("bbox, width, height, datetime: %s, %f, %f, %s",
                 str(bbox), width, height, str(dt))

    if dt:
        dt_rep_official = dt.isoformat()
        try:
            dt_rep, _ = dt_rep_official.split("+")
        except ValueError:
            dt_rep = dt_rep_official
    else:
        dt_rep = ''

    parameters = {
        'srs': srs,
        'width': width,
        'height': height,
        'format': 'geotiff',
        'geom': bbox.geom
    }

    is_temporal = RASTER_INFO[layer]['temporal']

    # unfortunately, raster endpoint doesn't like to accept all parameters,
    # which is why it's done like this
    if is_temporal:
        parameters.update({
            'time': dt_rep,
            'start': '',
            'stop': '',
        })

    layer_uuid = RASTER_INFO[layer]['uuid']

    url = '{path}?{pars}'.format(
        pars=urllib.urlencode(parameters),
        path=urlparse.urljoin(server, layer_uuid + '/data/'))
    logger.info('Raster-store API call: fetching rain data from %s' % url)

    request = urllib2.Request(url)
    request = use_header(request, username, password)
    try:
        response = urllib2.urlopen(request)
    except urllib2.HTTPError as e:
        print("Failed to fetch layer. Error: %s" % e)
        return

    fileno, path = tempfile.mkstemp()
    os.write(fileno, response.read())
    os.close(fileno)
    return path
