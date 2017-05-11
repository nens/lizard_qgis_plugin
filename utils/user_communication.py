# -*- coding: utf-8 -*-
"""Module for communicating with the user from QGIS."""

from qgis.utils import iface

from .constants import ERROR_LEVEL_CRITICAL
from .constants import ERROR_LEVEL_WARNING
from .constants import ERROR_LEVEL_INFO
from .constants import ERROR_LEVEL_SUCCESS


def show_message(error_level, message):
    """
    Function to show a message in a QGIS messagebar.

    Args:
        (str) error_level: Type of error. There are 4 kinds of error levels:
            "Critical", "Warning", "Info" and "Success".
        (str) message: The message that will be shown in the QGIS messagebar.
    """
    if error_level == ERROR_LEVEL_CRITICAL:
        iface.messageBar().pushCritical(ERROR_LEVEL_CRITICAL, message)
    elif error_level == ERROR_LEVEL_WARNING:
        iface.messageBar().pushWarning(ERROR_LEVEL_WARNING, message)
    elif error_level == ERROR_LEVEL_INFO:
        iface.messageBar().pushInfo(ERROR_LEVEL_INFO, message)
    elif error_level == ERROR_LEVEL_SUCCESS:
        iface.messageBar().pushSuccess(ERROR_LEVEL_SUCCESS, message)
