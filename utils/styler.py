# -*- coding: utf-8 -*-
"""Module for styling the layer."""
import os.path

# Add reference to layer_styles directory
STYLES_ROOT = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                           os.path.pardir, 'layer_styles')


def apply_style(layer, asset_type):
    """Apply styling to a layer (QML)."""
    # Create the path to the QML
    qml_path = os.path.join(STYLES_ROOT, "{}.qml".format(asset_type))
    # Check if the QML exists
    if os.path.exists(qml_path):
        # Add the style to the layer (QML)
        layer.loadNamedStyle(qml_path)
