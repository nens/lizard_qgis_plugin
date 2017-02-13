# -*- coding: utf-8 -*-
"""Module to change the dockwidget dynamically."""


def change_tab(self, string):
    """Function to dynamically change tabs."""
    if string == "Log in":
        self.dockwidget.tabWidget.setCurrentIndex(0)
    elif string == "Select data":
        self.dockwidget.tabWidget.setCurrentIndex(1)
    elif string == "Uploaden":
        self.dockwidget.tabWidget.setCurrentIndex(2)
