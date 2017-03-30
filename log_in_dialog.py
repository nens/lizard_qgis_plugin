import os

from PyQt4 import QtCore, QtGui, uic

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'log_in_dialog.ui'))


class LogInDialog(QtGui.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(LogInDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)

# # -*- coding: utf-8 -*-

# # Form implementation generated from reading ui file 'log_in_dialog.ui'
# #
# # Created by: PyQt4 UI code generator 4.11.4
# #
# # WARNING! All changes made in this file will be lost!

# class Ui_log_in_dialog(object):
    def setupUi(self, log_in_dialog):
        log_in_dialog.setObjectName(_fromUtf8("log_in_dialog"))
        log_in_dialog.resize(314, 145)
        self.user_name_label = QtGui.QLabel(log_in_dialog)
        self.user_name_label.setGeometry(QtCore.QRect(10, 10, 101, 31))
        self.user_name_label.setObjectName(_fromUtf8("user_name_label"))
        self.user_name_input = QtGui.QLineEdit(log_in_dialog)
        self.user_name_input.setGeometry(QtCore.QRect(120, 10, 181, 27))
        self.user_name_input.setObjectName(_fromUtf8("user_name_input"))
        self.user_password_label = QtGui.QLabel(log_in_dialog)
        self.user_password_label.setGeometry(QtCore.QRect(10, 60, 101, 31))
        self.user_password_label.setObjectName(
            _fromUtf8("user_password_label"))
        self.user_password_input = QtGui.QLineEdit(log_in_dialog)
        self.user_password_input.setGeometry(QtCore.QRect(120, 60, 181, 27))
        self.user_password_input.setInputMethodHints(
            QtCore.Qt.ImhHiddenText |
            QtCore.Qt.ImhNoAutoUppercase |
            QtCore.Qt.ImhNoPredictiveText)
        self.user_password_input.setEchoMode(QtGui.QLineEdit.Password)
        self.user_password_input.setObjectName(
            _fromUtf8("user_password_input"))
        self.log_in_button = QtGui.QPushButton(log_in_dialog)
        self.log_in_button.setGeometry(QtCore.QRect(120, 110, 99, 27))
        self.log_in_button.setObjectName(_fromUtf8("log_in_button"))

        self.retranslateUi(log_in_dialog)
        QtCore.QMetaObject.connectSlotsByName(log_in_dialog)

    def retranslateUi(self, log_in_dialog):
        log_in_dialog.setWindowTitle(
            _translate("log_in_dialog", "Log In", None))
        self.user_name_label.setText(
            _translate("log_in_dialog", "User name", None))
        self.user_password_label.setText(
            _translate("log_in_dialog", "User password", None))
        self.log_in_button.setText(_translate("log_in_dialog", "Log in", None))

    def clear_user_info(self):
        """Function to clear the user input."""
        self.user_name_input.clear()
        self.user_password_input.clear()
