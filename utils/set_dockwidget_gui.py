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


def clear_user_info(self):
    """Function to clear the user input."""
    self.dockwidget.user_name_input.clear()
    self.dockwidget.user_password_input.clear()


def status_bar_text(self, string):
    """Set the text for the status bars."""
    self.dockwidget.status_bar.setText(string)
    self.dockwidget.status_bar.repaint()
    self.dockwidget.status_bar_2.setText(string)
    self.dockwidget.status_bar_2.repaint()
    self.dockwidget.status_bar_3.setText(string)
    self.dockwidget.status_bar_3.repaint()
