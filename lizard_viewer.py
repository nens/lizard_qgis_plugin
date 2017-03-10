# -*- coding: utf-8 -*-
"""Module containing the main file for the QGIS Lizard plug-in"""
import os.path
import urllib2

from PyQt4.QtCore import QCoreApplication
from PyQt4.QtCore import QSettings
from PyQt4.QtCore import Qt
from PyQt4.QtCore import QTranslator
from PyQt4.QtCore import qVersion
from PyQt4.QtGui import QAction
from PyQt4.QtGui import QIcon
from PyQt4.QtGui import QKeySequence
from PyQt4.QtGui import QLineEdit
from PyQt4.QtGui import QShortcut

import lizard_connector
# Initialize Qt resources from file resources.py
import resources
from .dockwidget import LizardViewerDockWidget
from .dockwidget import TAB_LOG_IN
from .dockwidget import TAB_SELECT_DATA
from .utils.constants import ASSET_TYPES
from .utils.get_data import get_data
from .utils.layer import create_layer


class LizardViewer:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'LizardViewer_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Lizard Viewer')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'LizardViewer')
        self.toolbar.setObjectName(u'LizardViewer')

        self.pluginIsActive = False
        self.dockwidget = None

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('LizardViewer', message)

    def add_action(self,
                   icon_path,
                   text,
                   callback,
                   enabled_flag=True,
                   add_to_menu=True,
                   add_to_toolbar=True,
                   status_tip=None,
                   whats_this=None,
                   parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """
        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""
        icon_path = ':/plugins/LizardViewer/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Lizard Viewer'),
            callback=self.run,
            add_to_toolbar=True,
            parent=self.iface.mainWindow())
        self.username = None

    def onClosePlugin(self):
        """Cleanup necessary items here when plugin dockwidget is closed."""
        # disconnects
        self.dockwidget.closingPlugin.disconnect(self.onClosePlugin)

        # remove this statement if dockwidget is to remain
        # for reuse if plugin is reopened
        # Commented next statement since it causes QGIS crashe
        # when closing the docked window:
        # self.dockwidget = None

        self.pluginIsActive = False

    def unload(self):
        """Remove the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Lizard Viewer'),
                action)
            self.iface.removeToolBarIcon(action)
        # Remove the toolbar
        del self.toolbar

    def run(self):
        """Run method that loads and starts the plugin."""
        if not self.pluginIsActive:
            self.pluginIsActive = True

            # dockwidget may not exist if:
            #    first run of plugin
            #    removed on close (see self.onClosePlugin method)
            if self.dockwidget is None:
                # Create the dockwidget (after translation) and keep reference
                self.dockwidget = LizardViewerDockWidget()
                # Password is shown in asterisks
                self.dockwidget.user_password_input.setEchoMode(
                    QLineEdit.Password)
                # Add the asset types to the data_types combobox
                self.dockwidget.datatypes_combobox.addItems(ASSET_TYPES)
                # Set the status bar text
                self.dockwidget.set_all_status_bars_text(
                    "Lizard Viewer started.")
                # Go to the select data tab
                self.dockwidget.change_tab(TAB_SELECT_DATA)
                # Connect the login_button with log_in()
                self.dockwidget.login_button.clicked.connect(
                    self.log_in)
                # Login by pressing Enter in user_password_input
                shortcut_login_enter = QShortcut(
                    QKeySequence(Qt.Key_Enter),
                    self.dockwidget.user_password_input)
                shortcut_login_enter.setContext(Qt.ApplicationShortcut)
                shortcut_login_enter.activated.connect(self.log_in)
                # Connect the view_data_button with show_data()
                self.dockwidget.view_data_button.clicked.connect(
                    self.show_data)
                # Connect the login_button with log_out()
                self.dockwidget.logout_button.clicked.connect(
                    self.log_out)
            # connect to provide cleanup on closing of dockwidget
            self.dockwidget.closingPlugin.connect(self.onClosePlugin)
            # show the dockwidget
            # TODO: fix to allow choice of dock location
            self.iface.addDockWidget(Qt.RightDockWidgetArea, self.dockwidget)
            self.dockwidget.show()

    def show_data(self):
        """Show the data as a new layer on the map."""
        # Get the selected asset_type
        asset_type_index = self.dockwidget.datatypes_combobox.currentIndex()
        asset_type = ASSET_TYPES[asset_type_index]
        # Set the status bar text
        self.dockwidget.set_all_status_bars_text(
            "Downloading {}...".format(asset_type))
        # Get a list with JSONs containing the data from the Lizard API
        payload = {"page_size": 100}
        list_of_assets = get_data(asset_type, payload)
        # Create a new vector layer
        self.layer = create_layer(asset_type, list_of_assets)
        # Set the status bar text
        self.dockwidget.set_all_status_bars_text(
            "{} downloaded.".format(asset_type.capitalize()))

    def log_in(self):
        """Handle the log in."""
        self.username = None
        # Reset the Data type combobox
        self.dockwidget.reset_datatypes_combobox()
        # Remove the organisations from the combobox
        self.dockwidget.remove_organisation_options()
        # Get the username
        self.username = self.dockwidget.user_name_input.text()
        # Check if the user exists
        try:
            # Get the possible users of the API the user has access to
            users = lizard_connector.connector.Endpoint(
                username=self.username,
                password=self.dockwidget.user_password_input.text(),
                endpoint="users")
            users_ = users.download()
            # Check whether the username and password match with those of
            # the API
            for key in users_:
                if key["username"] == self.username:
                    # Show logged in in the status bar
                    self.dockwidget.set_all_status_bars_text("Logged in.")
                    # Add organisation options
                    self.dockwidget.add_organisation_options(
                        self.username,
                        self.dockwidget.user_password_input.text())
                    # Go to the select data tab
                    self.dockwidget.change_tab(TAB_SELECT_DATA)
                    # Clear the user info
                    self.dockwidget.clear_user_info()
        except urllib2.HTTPError:
            # Show log in error in the status bar
            self.username = None
            self.dockwidget.set_all_status_bars_text(
                "User/password combination incorrect.")

    def log_out(self):
        """Handle the log out."""
        # Delete the username and password if they exist
        if self.username is not None:
            self.username = None
            # Show logged out in the status bar
            self.dockwidget.set_all_status_bars_text("Logged out.")
            # Go to the log in tab
            self.dockwidget.change_tab(TAB_LOG_IN)
        else:
            self.dockwidget.set_all_status_bars_text("User not found.")
        # Clear the user info
        self.dockwidget.clear_user_info()
        # Reset the Data type combobox
        self.dockwidget.reset_datatypes_combobox()
        # Remove the organisations from the combobox
        self.dockwidget.remove_organisation_options()
