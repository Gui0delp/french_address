# -*- coding: utf-8 -*-
"""
/***************************************************************************
 FrenchAddress
                                 A QGIS plugin
 Recherche et localisation d'adresse française.
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2020-04-20
        git sha              : $Format:%H$
        copyright            : (C) 2020 by Guillaume DELPLANQUE
        email                : delpro.guillaume@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 3 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
import os.path

from qgis.core import QgsApplication, Qgis
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication, Qt
from qgis.PyQt.QtGui import QIcon, QCursor, QPixmap
from qgis.PyQt.QtWidgets import QAction, QApplication
from .modules.catch_tool import CatchTool
from .modules.coordinates import Coordinates
from .modules.address import Address
from .modules.api_address import ApiAddress
from .resources import *

from .french_address_dockwidget import FrenchAddressDockWidget


class FrenchAddress:
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
        self.canvas = self.iface.mapCanvas()

        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)

        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'FrenchAddress_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr('&French Address ')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'FrenchAddress')
        self.toolbar.setObjectName(u'FrenchAddress')

        #print "** INITIALIZING FrenchAddress"
        self.pluginIsActive = False
        self.dockwidget = None

        self.data_from_api = ""
        self.tool = None
        self.catch_tool_activate = False
        self.catch_tool_icon = QgsApplication.iconPath("cursors/mCapturePoint.svg")
        self.copy_icon = QgsApplication.iconPath("mActionEditCopy.svg")
        self.show_url_icon = QgsApplication.iconPath("mLayoutItemMap.svg")
        self.clipboard = QApplication.clipboard()

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
        return QCoreApplication.translate('FrenchAddress', message)

    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar."""

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

        icon_path = ':/plugins/french_address/icon.png'
        self.add_action(
            icon_path,
            text=self.tr('French Address'),
            callback=self.run,
            parent=self.iface.mainWindow())

    #--------------------------------------------------------------------------

    def onClosePlugin(self):
        """Cleanup necessary items here when plugin dockwidget is closed"""

        # disconnects
        self.dockwidget.closingPlugin.disconnect(self.onClosePlugin)
        self.canvas.unsetMapTool(self.tool)
        self.dockwidget.tb_catch_tool.setChecked(False)
        self.dockwidget.pb_locate_search.setEnabled(True)
        self.catch_tool_activate = False
        self.tool = None

        # remove this statement if dockwidget is to remain
        # for reuse if plugin is reopened
        # Commented next statement since it causes QGIS crashe
        # when closing the docked window:
        # self.dockwidget = None

        self.pluginIsActive = False

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""

        #print "** UNLOAD FrenchAddress"
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr('&French Address'),
                action)
            self.iface.removeToolBarIcon(action)

        if self.tool:
            self.canvas.unsetMapTool(self.tool)
            self.dockwidget.tb_catch_tool.setChecked(False)
            self.catch_tool_activate = False

        # remove the toolbar
        del self.toolbar

    def clear(self):
        """Permit to clean the differents items from the GUI"""
        self.dockwidget.le_input_address.clear()

    def enable_disable_catch_tool(self):
        if not self.catch_tool_activate:
            if self.tool is None:
                self.tool = CatchTool(self.iface, self.dockwidget, self)
                self.canvas.setMapTool(self.tool)
                self.canvas.setCursor(QCursor(QPixmap(self.catch_tool_icon)))
                self.catch_tool_activate = True
            self.dockwidget.pb_locate_search.setEnabled(False)
            self.dockwidget.tb_catch_tool.setChecked(True)
        else:
            QApplication.restoreOverrideCursor()
            self.canvas.unsetMapTool(self.tool)
            self.tool = None
            self.catch_tool_activate = False
            self.dockwidget.pb_locate_search.setEnabled(True)
            self.dockwidget.tb_catch_tool.setChecked(False)

    def address_processing(self):
        """Launch the address processing"""
        address_entry = self.dockwidget.le_input_address.toPlainText()

        if self.address.test_address_entry(address_entry):
            self.address.format_address_entry()
            if self.address.test_obligatory_field():

                self.api_address.set_search_url(
                    self.address.house_number,
                    self.address.name_road,
                    self.address.postcode,
                    )
                if self.api_address.test_request():
                    self.api_address.set_request()
                    self.api_address.decode_response()
                    self.api_address.json_to_dictionnary()
                    point_wgs84 = self.api_address.take_search_response_label()
                    self.coord.set_canvas_project(self.canvas)
                    self.coord.set_destination_crs()
                    self.coord.take_crs_from_project(self.iface)
                    self.coord.set_x_transform_reverse()
                    self.coord.set_latitude_longitude_crs(point_wgs84)
                    self.coord.zoom_to_canvas(self.canvas)

    def set_visible_properties(self, state):

        if state == Qt.Checked:
            self.dockwidget.tw_details.setVisible(True)
        else:
            self.dockwidget.tw_details.setVisible(False)

    def copy_to_clipboard(self):
        text_to_copy = self.dockwidget.le_input_address.toPlainText()
        message = ' Nothing copying to the clipboard'

        if text_to_copy != '':
            self.clipboard.setText(text_to_copy)
            message = f' {text_to_copy}, copied to the clipboard'

        self.iface.messageBar().pushMessage('Address',
                                            message,
                                            level=Qgis.Info,
                                            )

    def open_map_url(self):
        try:
            latitude_house = self.data_from_api['features'][0]['geometry']['coordinates'][1]
            longitude_house = self.data_from_api['features'][0]['geometry']['coordinates'][0]
            id_house = self.data_from_api['features'][0]['properties']['id']
            url = self.api_address.set_map_url(longitude_house, latitude_house, id_house)
            self.api_address.open_map_url(url)
        except:
            message = ' Nothing to open in browser'
            self.iface.messageBar().pushMessage('Address',
                                                message,
                                                level=Qgis.Info,
                                                )

    def set_connections(self):
        self.dockwidget.tb_catch_tool.clicked.connect(
            self.enable_disable_catch_tool
            )
        self.dockwidget.pb_locate_search.clicked.connect(
            self.address_processing
            )
        self.dockwidget.chb_view_details.stateChanged.connect(
            self.set_visible_properties
            )
        self.dockwidget.pb_copy.clicked.connect(
            self.copy_to_clipboard
            )
        self.dockwidget.tb_open_url.clicked.connect(
            self.open_map_url
            )

    def run(self):
        """Run method that loads and starts the plugin"""

        if not self.pluginIsActive:
            self.pluginIsActive = True

            if self.dockwidget is None:
                self.dockwidget = FrenchAddressDockWidget()
                self.dockwidget.tw_details.setVisible(False)
                self.coord = Coordinates(self.dockwidget)
                self.address = Address(self.dockwidget)
                self.api_address = ApiAddress()
                self.dockwidget.tb_catch_tool.setIcon(QIcon(self.catch_tool_icon))
                self.dockwidget.pb_copy.setIcon(QIcon(self.copy_icon))
                self.dockwidget.tb_open_url.setIcon(QIcon(self.show_url_icon))
                self.set_connections()

            self.dockwidget.closingPlugin.connect(self.onClosePlugin)

            # TODO: fix to allow choice of dock location
            self.iface.addDockWidget(Qt.LeftDockWidgetArea, self.dockwidget)
            self.dockwidget.show()
