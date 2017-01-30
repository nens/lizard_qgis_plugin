# -*- coding: utf-8 -*-
"""Module for styling the layer."""
import os.path

from qgis.core import QgsSvgMarkerSymbolLayerV2

# Add reference to layer_styles directory
STYLES_ROOT = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                           os.path.pardir, 'layer_styles')


def apply_style(layer, asset_type):
    """Apply styling to a layer (SVG)."""
    # Create the SVG style
    svg_style = {}
    svg_path = os.path.join(STYLES_ROOT, "{}.svg".format(asset_type))
    if os.path.exists(svg_path):
        svg_style["name"] = svg_path

        # Create a symbol layer with the SVG style
        symbol_layer = QgsSvgMarkerSymbolLayerV2.create(svg_style)

        # Apply the symbol layer to the layer
        layer.rendererV2().symbols()[0].changeSymbolLayer(0, symbol_layer)
