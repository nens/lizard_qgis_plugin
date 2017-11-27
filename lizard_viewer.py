# -*- coding: utf-8 -*-
"""Module containing the main file for the QGIS Lizard plug-in."""
import os.path
import time
import urllib2

from PyQt4.QtCore import pyqtSignal
from PyQt4.QtCore import QCoreApplication
from PyQt4.QtCore import QSettings
from PyQt4.QtCore import Qt
from PyQt4.QtCore import QThread
from PyQt4.QtCore import QTranslator
from PyQt4.QtCore import qVersion
from PyQt4.QtGui import QAction
from PyQt4.QtGui import QIcon
# Initialize Qt resources from file resources.py
import resources  # noqa

from .dockwidget import AREA_FILTER_CURRENT_VIEW
from .dockwidget import LizardViewerDockWidget
from .dockwidget import TAB_PRIVATE_DATA
from .dockwidget import TAB_PUBLIC_DATA
from .log_in_dialog import LogInDialog
from .utils.constants import ASSET_TYPES
from .utils.constants import DATA_TYPES
from .utils.constants import RASTER_TYPES
from .utils.constants import ERROR_LEVEL_CRITICAL
from .utils.constants import ERROR_LEVEL_SUCCESS
from .utils.constants import ERROR_LEVEL_WARNING
from .utils.constants import STYLES_ROOT
from .utils.get_data import retrieve_data_from_lizard
from .utils.geometry import add_area_filter
from .utils.geometry import get_bbox
from .utils.layer import create_layer
from .utils.user_communication import show_message
from .utils.rasters import fetch_layer_from_server
from .utils.rasters import BoundingBox
from .utils.rasters import calc_request_width_height


class AssetWorker(QThread):
    """This class creates a worker thread for getting the data."""

    output = pyqtSignal(object)

    def __init__(self, parent=None):
        """Initiate the AssetWorker."""
        super(AssetWorker, self).__init__(parent)

    def start_(self, asset_type, payload, username, password):
        """
        Thin wrapper around the start() method which starts the thread.

        Args:
            (str) asset_type: Get data from the Lizard API from this
                              asset type.
            (dict) payload: A dictionary containing a possible payload add to
                            the API call.
            (str) username: The username of the Lizard account.
            (str) password: The password of the Lizard account.
        """
        self.asset_type = asset_type
        self.payload = payload
        self.username = username
        self.password = password
        self.start()

    def run(self):
        """Called indirectly by PyQt if you call start().

        This method retrieves the data from Lizard and emits it via the
        output signal as dictionary.
        """
        data = self._get_data()
        self.output.emit(data)

    def _get_data(self):
        """
        Get the data from the Lizard API.

        Returns:
            (dict) data: A data dictionary containing the
                         asset type (data['asset_type']),
                         max_amount of results (data['max_amount']),
                         list of assets (data['list_of_assets']),
                         error_message (data['error_message'])
        """
        data = retrieve_data_from_lizard(
            self.username, self.password, self.asset_type, self.payload)
        return data


class RasterWorker(AssetWorker):
    def start_(self, layer, bbox,
               from_datetime, to_datetime, time_interval,
               username, password):
        self.layer = layer
        self._bbox = bbox
        self.bbox = BoundingBox(self._bbox)
        self.width, self.height = calc_request_width_height(self.bbox)
        self.from_datetime = from_datetime
        self.to_datetime = to_datetime
        self.time_interval = time_interval
        self.username = username
        self.password = password
        self.start()

    def _get_data(self):
        path = fetch_layer_from_server(
            self.bbox, self.width, self.height,
            from_datetime=self.from_datetime,
            to_datetime=self.to_datetime,
            time_interval=self.time_interval,
            layer=self.layer,
            username=self.username, password=self.password)
        layer_name = self.layer
        if self.layer == 'Rain':
            layer_name = '{} {}'.format(self.layer, self.from_datetime)
        return {'layer': self.layer, 'path': path,
                'layer_name': layer_name}


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
        self.asset_worker = AssetWorker()
        self.raster_worker = RasterWorker()
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
        self.login_dialog = LogInDialog()
        self.username = None
        self.password = None

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
                # Add the asset types to the data type comboboxes
                self.dockwidget.add_datatypes_to_combobox()
                # Add the asset types to the data type comboboxes
                self.dockwidget.add_areafilters_to_combobox()
                # Go to the select data tab
                self.dockwidget.change_tab(TAB_PRIVATE_DATA)
                # Connect the login button of the private data tab with
                # the login dialog
                self.dockwidget.login_button_private.clicked.connect(
                    self.show_login_dialog)
                # Connect the View data buttons with the show data functions
                self.dockwidget.view_data_button_private.clicked.connect(
                    self.show_private_data_async)
                self.dockwidget.view_data_button_public.clicked.connect(
                    self.show_public_data_async)
                # Connect the output of the worker thread to the display_layer
                # function
                self.asset_worker.output.connect(self.display_asset_layer)
                self.raster_worker.output.connect(self.display_raster_layer)
                # Connect the log_in function to the Log in button of the
                # Log in dialog
                self.login_dialog.log_in_button.clicked.connect(self.log_in)
            # connect to provide cleanup on closing of dockwidget
            self.dockwidget.closingPlugin.connect(self.onClosePlugin)
            # show the dockwidget
            # TODO: fix to allow choice of dock location
            self.iface.addDockWidget(Qt.RightDockWidgetArea, self.dockwidget)
            self.dockwidget.show()

    def show_private_data_async(self):
        """Show private data asynchronously."""
        area_type = self.dockwidget.area_combobox_private.currentText()
        type_index = self.dockwidget.data_type_combobox_private.currentIndex()
        data_type = DATA_TYPES[type_index]
        self.show_data_async(data_type, area_type)

    def show_public_data_async(self):
        """Show public data asynchronously."""
        area_type = self.dockwidget.area_combobox_public.currentText()
        type_index = self.dockwidget.data_type_combobox_public.currentIndex()
        data_type = DATA_TYPES[type_index]
        self.show_data_async(data_type, area_type)

    def show_data_async(self, data_type, area_type):
        """Show data asynchronically."""
        # Check whether a layer is active
        if(self.iface.activeLayer() is None and
           area_type == AREA_FILTER_CURRENT_VIEW):
            # Show message that there is no active layer with an extent
            show_message(
                "Please add a base layer in order to get the \
                'Current view'.", ERROR_LEVEL_WARNING)
            return
        # Check required extent for rasters
        if data_type in RASTER_TYPES and area_type != AREA_FILTER_CURRENT_VIEW:
            show_message(
                "Rasters only work with current view for now.",
                ERROR_LEVEL_WARNING)
            return

        show_message("Downloading from Lizard API...")
        if data_type in ASSET_TYPES:
            payload = add_area_filter(self.iface, data_type, area_type)
            self.asset_worker.start_(
                data_type, payload, self.username, self.password)
        elif data_type in RASTER_TYPES:
            bbox = get_bbox(self.iface)
            # Start datetime
            from_datetime = self.dockwidget.from_date_dateTimeEdit.dateTime()\
                .toString("yyyy-MM-dd HH:mm:00")
            print from_datetime  # 2000-01-01 00:00
            pattern = "%Y-%m-%d %H:%M:%S"
            from_epoch = int(time.mktime(time.strptime(
                from_datetime, pattern)))
            print from_epoch  # 1325286000
            from_datetime2 = time.strftime(pattern, time.localtime(from_epoch))
            print from_datetime2  # 2000-01-01 00:00
            # Stop datetime
            to_datetime = self.dockwidget.to_date_dateTimeEdit.dateTime()\
                .toString("yyyy-MM-dd HH:mm:00")  # 2000-01-01 00:00
            # ook mogelijk als yyyy-MM-ddTHH:mm:00Z
            # (volgens docs raster store)?
            to_epoch = int(time.mktime(time.strptime(to_datetime, pattern)))
            print to_epoch
            time_interval = str(self.dockwidget.time_interval_combobox
                                .currentText())
            if data_type == 'Rain':
                window = 0
                if time_interval == "5min":
                    window = 300
                elif time_interval == "hour":
                    window = 3600
                elif time_interval == "day":
                    window = 86400
                else:
                    window = 86400
                current_epoch = from_epoch
                while current_epoch < to_epoch:
                    print current_epoch
                    from_datetime = time.strftime(
                        '%Y-%m-%d %H:%M:%S', time.localtime(current_epoch))
                    self.raster_worker = RasterWorker()
                    self.raster_worker.start_(
                        data_type, bbox,
                        from_datetime,  # current_epoch
                        to_datetime,
                        time_interval,
                        self.username, self.password)
                    current_epoch += window
                    self.raster_worker.output.connect(
                        self.display_raster_layer)  # creates the same raster
                    print current_epoch, to_epoch
            # if self.from_date and self.to_date:
            # elif self.from_date:
            else:
                self.raster_worker.start_(
                    data_type, bbox,
                    from_datetime,
                    to_datetime,
                    time_interval,
                    self.username, self.password)

    def display_asset_layer(self, data):
        """
        Display asset data as a layer.

        Args:
            (dict) data: A data dictionary containing the
                         asset type (data['asset_type']),
                         max_amount of results (data['max_amount']),
                         list of assets (data['list_of_assets']),
                         error_message (data['error_message'])
        """
        if data["error_message"] != "":
            show_message(data["error_message"], ERROR_LEVEL_CRITICAL)
            return
        asset_type = data["asset_type"]
        max_amount = data["max_amount"]
        list_of_assets = data["list_of_assets"]
        if list_of_assets:
            # Create a new vector layer
            self.layer = create_layer(asset_type, list_of_assets)
            # Show how many and which asset type is downloaded.
            show_message("{} {} downloaded.".format(
                max_amount, asset_type), ERROR_LEVEL_SUCCESS)
        else:
            # Show that there are no assets
            show_message("No {} found".format(asset_type))

    def display_raster_layer(self, data):
        if data['path']:
            self.iface.addRasterLayer(data['path'], data['layer_name'])
            qml_path = os.path.join(STYLES_ROOT,
                                    "{}.qml".format(data['layer']))
            if os.path.exists(qml_path):
                self.iface.activeLayer().loadNamedStyle(qml_path)
                self.iface.legendInterface().refreshLayerSymbology(
                    self.iface.activeLayer())
            show_message(
                "Downloaded %s" % data['layer'], ERROR_LEVEL_SUCCESS)
        else:
            show_message(
                "Failed to download %s" % data['layer'], ERROR_LEVEL_CRITICAL)

    def show_login_dialog(self):
        """Function to show the login dialog."""
        # Check whether the user is logged in
        if self.username is None:
            # The user_name_input QLineEdit becomes the active part of the
            # login dialog
            self.login_dialog.user_name_input.setFocus()
            # Show the dialog
            self.login_dialog.show()
        else:
            self.log_out()

    def log_in(self):
        """Function to handle logging in."""
        # Get the username
        self.username = self.login_dialog.user_name_input.text()
        # Get the password
        self.password = self.login_dialog.user_password_input.text()
        # Check if the user exists
        try:
            # Get the possible users of the API the user has access to
            asset_type = "users"
            payload = {}
            users = retrieve_data_from_lizard(
                self.username, self.password, asset_type, payload)
            # Check whether the username and password match with those of
            # the API
            for user in users["list_of_assets"]:
                if user["username"] == self.username:
                    # Go to the Private data tab
                    self.dockwidget.change_tab(TAB_PRIVATE_DATA)
                    # Clear the user info
                    self.login_dialog.clear_user_info()
                    # Close the dialog
                    self.login_dialog.close()
                    # Set the login button text to log out
                    self.dockwidget.login_button_private.setText("Log out")
                    # Show a logged in message
                    show_message("Logged in.")
        except urllib2.HTTPError:
            # Reset the user credentials
            self.username = None
            self.password = None
            # Show log in error in the message bar
            show_message("User/password combination incorrect.",
                         ERROR_LEVEL_WARNING)

    def log_out(self):
        """Function to log out the user."""
        # Reset the user credentials
        self.username = None
        self.password = None
        # Reset the Data type combobox
        self.dockwidget.reset_datatypes_combobox()
        # Set the text of the login button to log in
        self.dockwidget.login_button_private.setText("Log in")
        # Go to the public data tab
        self.dockwidget.change_tab(TAB_PUBLIC_DATA)
        # Show a logged out message
        show_message("Logged out.")
