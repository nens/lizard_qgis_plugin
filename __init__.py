# -*- coding: utf-8 -*-
""" This script initializes the plugin, making it known to QGIS."""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load LizardViewer class from file LizardViewer.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    from .lizard_viewer import LizardViewer
    return LizardViewer(iface)
