# -*- coding: utf-8 -*-
"""Module to change the dockwidget dynamically."""


def status_bar_text(self, string):
    """Set the text for the status bars."""
    self.dockwidget.status_bar_log_in.setText(string)
    self.dockwidget.status_bar_log_in.repaint()
    self.dockwidget.status_bar_select_data.setText(string)
    self.dockwidget.status_bar_select_data.repaint()
    self.dockwidget.status_bar_upload_data.setText(string)
    self.dockwidget.status_bar_upload_data.repaint()
