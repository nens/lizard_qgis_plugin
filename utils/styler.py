# -*- coding: utf-8 -*-
"""Module for styling the layer."""
import os.path

from .constants import STYLES_ROOT


def apply_style(layer, asset_type):
    """Apply styling to a layer (QML)."""
    # Create the path to the QML
    qml_path = os.path.join(STYLES_ROOT, "{}.qml".format(asset_type))
    # Check if the QML exists
    if os.path.exists(qml_path):
        # Add the style to the layer (QML)
        layer.loadNamedStyle(qml_path)
