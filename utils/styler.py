# -*- coding: utf-8 -*-
"""Module for styling the layer."""
import os.path

from qgis.core import QgsSvgMarkerSymbolLayerV2

from .constants import STYLES_ROOT


def apply_style(layer, asset_type):
    """Apply styling to a layer (SVG/ QML)."""
    # Create the path to the styling (SVG/ QML).
    qml_path = os.path.join(STYLES_ROOT, "{}.qml".format(asset_type))
    svg_path = os.path.join(STYLES_ROOT, "{}.svg".format(asset_type))
    # Check if the QML exists
    if os.path.exists(qml_path):
        # Add the QML style to the layer
        layer.loadNamedStyle(qml_path)
    # Check if the SVG exists
    elif os.path.exists(svg_path):
            # Create the SVG style
            svg_style = {}
            svg_style["name"] = svg_path
            # Create a symbol layer with the SVG style
            symbol_layer = QgsSvgMarkerSymbolLayerV2.create(svg_style)
            # Apply the symbol layer to the layer
            layer.rendererV2().symbols()[0].changeSymbolLayer(0, symbol_layer)
