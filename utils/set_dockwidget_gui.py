# -*- coding: utf-8 -*-
"""Module to change the dockwidget dynamically."""


def status_bar_text(self, string):
    """Set the text for the status bars."""
    self.dockwidget.status_bar.setText(string)
    self.dockwidget.status_bar.repaint()
    self.dockwidget.status_bar_2.setText(string)
    self.dockwidget.status_bar_2.repaint()
    self.dockwidget.status_bar_3.setText(string)
    self.dockwidget.status_bar_3.repaint()
