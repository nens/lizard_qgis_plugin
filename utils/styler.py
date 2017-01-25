# -*- coding: utf-8 -*-
"""
/***************************************************************************
 LizardDownloader
                                 A QGIS plugin
 This plug-in helps with downloading data fromLizard in QGIS.
                              -------------------
        begin                : 2017-01-24
        git sha              : $Format:%H$
        copyright            : (C) 2017 by Madeleine van Winkel
        email                : madeleine.vanwinkel@nelen-schuurmans.nl
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

# Import
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
