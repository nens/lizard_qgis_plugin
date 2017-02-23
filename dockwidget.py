# -*- coding: utf-8 -*-
"""Module containing the setup for the dockwidget."""

import os

from PyQt4 import QtGui, uic
from PyQt4.QtCore import pyqtSignal

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'dockwidget.ui'))

TAB_LOG_IN = "Log in"
TAB_SELECT_DATA = "Select data"
TAB_UPLOAD_DATA = "Upload data"


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
        if tab_constant == TAB_LOG_IN:
            self.tabWidget.setCurrentIndex(0)
        elif tab_constant == TAB_SELECT_DATA:
            self.tabWidget.setCurrentIndex(1)
        elif tab_constant == TAB_UPLOAD_DATA:
            self.tabWidget.setCurrentIndex(2)

    def set_all_status_bars_text(self, string):
        """Set the text for the status bars."""
        status_bars = self.all_status_bars()
        for status_bar in status_bars:
            status_bar.setText(string)
            status_bar.repaint()

    def all_status_bars(self):
        """Function to return all the status bars."""
        return [self.status_bar_log_in,
                self.status_bar_select_data,
                self.status_bar_upload_data]
