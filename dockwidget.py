# -*- coding: utf-8 -*-
"""Module containing the setup for the dockwidget."""

import os

from PyQt4 import QtGui, uic
from PyQt4.QtCore import pyqtSignal
from PyQt4.QtCore import QDateTime

from .utils.constants import AREA_FILTERS
from .utils.constants import ASSET_TYPES
from .utils.constants import RASTER_TYPES
from .utils.constants import STYLES_ROOT

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'dockwidget.ui'))

AREA_FILTER_CURRENT_VIEW = "Current view"
TAB_PRIVATE_DATA = "Private data"
TAB_PUBLIC_DATA = "Public data"

# Mark assets that have no styling.
UNSTYLED_POSTFIX = " (not styled)"


class LizardViewerDockWidget(QtGui.QDockWidget, FORM_CLASS):
    """Module for creating the dockwidget."""

    closingPlugin = pyqtSignal()

    def __init__(self, parent=None):
        """Constructor."""
        super(LizardViewerDockWidget, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)

    def closeEvent(self, event):
        """Module for closing the dockwidget."""
        self.closingPlugin.emit()
        event.accept()

    def change_tab(self, tab_constant):
        """Function to dynamically change tabs.

        Args:
            tab_constans (str): Name of the tab. There are three possible
                options: TAB_LOGIN for "Log in", TAB_SELECT_DATA for
                "Select data" and TAB_UPLOAD_DATA for "Upload data".

        """
        if tab_constant == TAB_PRIVATE_DATA:
            self.tabWidget.setCurrentIndex(0)
        elif tab_constant == TAB_PUBLIC_DATA:
            self.tabWidget.setCurrentIndex(1)

    def add_datatypes_to_combobox(self):
        """Add an asterisk for asset types that don't have styling."""
        for asset_type in ASSET_TYPES:
            qml_path = os.path.join(STYLES_ROOT, "{}.qml".format(asset_type))
            svg_path = os.path.join(STYLES_ROOT, "{}.svg".format(asset_type))
            # Check if the QML exists
            if not os.path.exists(qml_path) and not os.path.exists(svg_path):
                asset_type = "{}{}".format(asset_type, UNSTYLED_POSTFIX)
            self.data_type_combobox_private.addItem(asset_type)
            self.data_type_combobox_public.addItem(asset_type)
        for raster_type in RASTER_TYPES:
            qml_path = os.path.join(STYLES_ROOT, "{}.qml".format(raster_type))
            svg_path = os.path.join(STYLES_ROOT, "{}.svg".format(raster_type))
            # Check if the QML exists
            if not os.path.exists(qml_path) and not os.path.exists(svg_path):
                raster_type = "{}{}".format(raster_type, UNSTYLED_POSTFIX)
            self.data_type_combobox_private.addItem(raster_type)

    def add_areafilters_to_combobox(self):
        """Add the area filters to the combobox."""
        for area_filter in AREA_FILTERS:
            self.area_combobox_private.addItem(area_filter)
            self.area_combobox_public.addItem(area_filter)

    def reset_datatypes_combobox(self):
        """Function to reset the data."""
        self.data_type_combobox_private.setCurrentIndex(0)
        self.data_type_combobox_public.setCurrentIndex(0)

    def set_maximum_datetime(self):
        """
        Set the maximum datetime of the QDateTimeEdit to the current day 23:59.
        """
        current_datetime = QDateTime.currentDateTime()
        self.from_date_dateTimeEdit.setMaximumDateTime(current_datetime)
        self.to_date_dateTimeEdit.setMaximumDateTime(current_datetime)

    def set_all_status_bars_text(self, string):
        """Set the text for the status bars."""
        status_bars = self.all_status_bars()
        for status_bar in status_bars:
            status_bar.setText(string)
            status_bar.repaint()

    def all_status_bars(self):
        """Function to return all the status bars."""
        return [self.status_bar_private,
                self.status_bar_public]
