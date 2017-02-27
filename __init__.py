# -*- coding: utf-8 -*-
""" This script initializes the plugin, making it known to QGIS."""
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
    from .lizard_viewer import LizardViewer
    return LizardViewer(iface)
