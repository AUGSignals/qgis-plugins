# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Histogram
                                 A QGIS plugin
 This plugin creates a histogram of selected image.
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2020-07-27
        git sha              : $Format:%H$
        copyright            : (C) 2020 by Tomas/AUG Signals
        email                : tomas@augsignals.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
import subprocess
import os

from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QMenu, QFileDialog
from qgis.core import QgsMessageLog, Qgis, QgsProject, QgsRasterLayer, QgsMapLayer

# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .histogram_dialog import HistogramDialog
import os.path


class Histogram:
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
            'Histogram_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Histogram')

        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.first_start = None

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
        return QCoreApplication.translate('Histogram', message)


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
            # Adds plugin icon to Plugins toolbar
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def addToCustomMenu(self):
        self.menu = self.iface.mainWindow().findChild(QMenu, '&AUG Plugins')
        if not self.menu:
            self.menu = QMenu(self.iface.mainWindow())
            self.menu.setObjectName('&AUG Plugins')
            self.menu.setTitle('&AUG Plugins')
        self.action = QAction(QIcon(":/plugins/lee_sigma_filter/icon.png"),
                                    "Histogram",
                                    self.iface.mainWindow())
        self.action.setObjectName("histogram")
        self.action.setWhatsThis("Configuration for test plugin")
        self.action.setStatusTip("This is status tip")
        self.action.triggered.connect(self.run)

        # Create list containing submenu actions from main menu
        submenus = []
        for item in self.menu.actions():
            if item.text() == '&Feature Extraction':
                submenus.append(item.menu())
                print(item)

        # If 'MySubMenu' is not in above list (i.e. does not exist), create it
        if submenus:
            self.subMenu = submenus[0]
        if not submenus:
            self.subMenu = self.menu.addMenu( '&Feature Extraction')

        self.subMenu.setObjectName("&Feature Extraction")

        self.subMenu.addAction(self.action)

        menuBar = self.iface.mainWindow().menuBar()
        menuBar.insertMenu(self.iface.firstRightStandardMenu().menuAction(),
                       self.menu)

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""
        self.addToCustomMenu()

        """
        icon_path = ':/plugins/histogram/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u''),
            callback=self.run,
            parent=self.iface.mainWindow())
        """

        # will be set False in run()
        self.first_start = True


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Histogram'),
                action)
            self.iface.removeToolBarIcon(action)

    def display_bands(self):
        curr_layer = self.dlg.inputQgsMapLayerComboBox.currentLayer()
        if curr_layer.type() == QgsMapLayer.RasterLayer:
            self.dlg.bandIndexQgsRasterBandComboBox.setEnabled(True)
            self.dlg.bandIndexQgsRasterBandComboBox.setLayer(curr_layer)
        else:
            self.dlg.bandIndexQgsRasterBandComboBox.setDisabled(True)


    def run(self):
        """Run method that performs all the real work"""

        # Create the dialog with elements (after translation) and keep reference
        # Only create GUI ONCE in callback, so that it will only load when the plugin is started
        if self.first_start == True:
            self.first_start = False
            self.dlg = HistogramDialog()
            self.dlg.inputQgsMapLayerComboBox.layerChanged.connect(self.display_bands)
            self.dlg.bandIndexQgsRasterBandComboBox.setLayer(self.dlg.inputQgsMapLayerComboBox.currentLayer())

        self.arguments = {}
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            self.arguments['-i'] = self.dlg.inputQgsMapLayerComboBox.currentLayer().dataProvider().dataSourceUri()
            self.arguments["-o"] = self.dlg.outputQgsFileWidget.filePath()

            self.arguments["-b"] = str(self.dlg.bandIndexQgsRasterBandComboBox.currentBand())
            self.arguments["-n"] = str(self.dlg.numberOfBinsSpinBox.text())

            self.arguments["-v"] = self.dlg.verboseCheckBox.isChecked()

            args = []
            for key, value in self.arguments.items():
                if(value == False):
                    continue
                if (value == True):
                    args.append(key)
                else:
                    args.append(key)
                    args.append(value)

            s = QSettings()
            path = s.value("qgis-exe/path")
            exeName = "Histogram.exe"
            path = path + "/" + exeName
            args.insert(0, path)

            QgsMessageLog.logMessage("Your plugin code has been executed correctly", 'MyPlugin', Qgis.Info)
            QgsMessageLog.logMessage(str(args), 'MyPlugin', Qgis.Info)
            popen = subprocess.Popen(args)
            popen.wait()
            output_path = self.dlg.outputQgsFileWidget.filePath()
            rlayer = QgsRasterLayer(output_path, os.path.basename(output_path))
            if not rlayer.isValid():
                QgsMessageLog.logMessage("Layer failed to load!", 'MyPlugin', Qgis.Info)
