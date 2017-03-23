
# -*- coding: utf-8 -*-
"""Module for styling the layer."""
import os.path

from .constants import DATA_ROOT
from .constants import STYLES_ROOT


def apply_style(dockwidget, shapefile_name, shapefile_layer, asset_type):
    """Apply styling to a layer (QML)."""
    try:
        # Create the path to the styling
        qml_path_origin = os.path.join(
            STYLES_ROOT, "{}.qml".format(asset_type))
        # Add the styling to the shapefile layer (QML)
        shapefile_layer.loadNamedStyle(qml_path_origin)
        # Save the styling of the shapefile layer as the shapefile name (QML)
        try:
            qml_path_output = os.path.join(
                DATA_ROOT, "{}.qml".format(shapefile_name))
            shapefile_layer.saveNamedStyle(qml_path_output)
        except OSError:
            # Set the status bar text
            dockwidget.set_all_status_bars_text(
                "Cannot save QML styling.")
    except OSError:
        # Set the status bar text
        dockwidget.set_all_status_bars_text("QML path does not exist.")
