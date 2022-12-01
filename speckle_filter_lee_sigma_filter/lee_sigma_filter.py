# -*- coding: utf-8 -*-
"""
/***************************************************************************
 LeeSigmaFilter
                                 A QGIS plugin
 This plugin launches the Lee Sigma Filter.
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        copyright            : (C) 2020 by AUG Signals
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
from qgis.core import QgsMessageLog, Qgis, QgsProject, QgsRasterLayer

# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .lee_sigma_filter_dialog import LeeSigmaFilterDialog
from .output_dialog import OutputDialog
import os.path


class LeeSigmaFilter:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        self.output_dialog = OutputDialog()
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'LeeSigmaFilter_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Lee Sigma Filter')

        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.first_start = None

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        return QCoreApplication.translate('LeeSigmaFilter', message)


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

    def initGui(self):
        self.addToCustomMenu()

        # will be set False in run()
        self.first_start = True

    def addToCustomMenu(self):
        self.menu = self.iface.mainWindow().findChild(QMenu, '&Image Registration')
        if not self.menu:
            self.menu = QMenu(self.iface.mainWindow())
            self.menu.setObjectName('&Image Registration')
            self.menu.setTitle('&Image Registration')
        self.action = QAction(QIcon(":/plugins/lee_sigma_filter/icon.png"),
                                    "Lee Sigma Filter",
                                    self.iface.mainWindow())
        self.action.setObjectName("LeeSigma")
        self.action.setWhatsThis("Configuration for test plugin")
        self.action.setStatusTip("This is status tip")
        self.action.triggered.connect(self.run)
        self.actions.append(self.action)

        # Create list containing submenu actions from main menu
        submenus = []
        for item in self.menu.actions():
            if item.text() == '&Speckle Filters':
                submenus.append(item.menu())
                print(item)

        # If 'MySubMenu' is not in above list (i.e. does not exist), create it
        if submenus:
            self.subMenu = submenus[0]
        if not submenus:
            self.subMenu = self.menu.addMenu( '&Speckle Filters')

        self.subMenu.setObjectName("&Speckle Filters")

        self.subMenu.addAction(self.action)

        menuBar = self.iface.mainWindow().menuBar()
        menuBar.insertMenu(self.iface.firstRightStandardMenu().menuAction(),
                       self.menu)

    def unload(self):
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Lee Sigma Filter'),
                action)
            self.iface.removeToolBarIcon(action)

    def run(self):
        
        if self.first_start == True:
            self.first_start = False
            self.dlg = LeeSigmaFilterDialog()

        kernelsizes = ["5x5", "7x7", "9x9", "11x11", "13x13", "15x15", "17x17"]
        self.dlg.kernelSizeComboBox.clear()
        self.dlg.kernelSizeComboBox.addItems(kernelsizes)

        sigmas = ["0.5", "0.6", "0.7", "0.8", "0.9"]
        self.dlg.sigmaComboBox.clear()
        self.dlg.sigmaComboBox.addItems(sigmas)

        targets = ["3x3", "5x5"]
        self.dlg.targetWindowSizeComboBox.clear()
        self.dlg.targetWindowSizeComboBox.addItems(targets)

        looks = ["1", "2", "3", "4"]
        self.dlg.numLooksComboBox.clear()
        self.dlg.numLooksComboBox.addItems(looks)

        self.arguments = {}

        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            selected_layer = self.dlg.inputQgsMapLayerComboBox.currentLayer()
            self.arguments['-i'] = selected_layer.dataProvider().dataSourceUri()
            self.arguments["-b"] = str(self.dlg.bandIndexQgsRasterBandComboBox.currentBand())
            self.arguments["-c"] = str(selected_layer.width())
            self.arguments["-r"] = str(selected_layer.height())
            kernelsize = 5 + 2*self.dlg.kernelSizeComboBox.currentIndex() #currently hardcoved. #TODO - change
            self.arguments["-k"] = str(kernelsize)

            self.arguments["-n"] = looks[self.dlg.numLooksComboBox.currentIndex()]
            self.arguments["-o"] = self.dlg.outputQgsFileWidget.filePath()
            output_path = self.dlg.outputQgsFileWidget.filePath()

            target = targets[self.dlg.targetWindowSizeComboBox.currentIndex()]
            self.arguments["-t"] = target

            self.arguments["-s"] = sigmas[self.dlg.sigmaComboBox.currentIndex()]
            
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
            exeName = "LeeSigma.exe"
            path = path + "/" + exeName
            args.insert(0, path)
            args_message = " ".join(arg for arg in args)

            if self.arguments["-v"] == False:
                popen = subprocess.Popen(args, stdout=subprocess.PIPE)
                popen.wait()
                out, err = popen.communicate()
            else:
                popen = subprocess.Popen(args)
                popen.wait()
                out, err = popen.communicate()

            output_dialog_text = ""
            if out is not None:
                output_dialog_text += out.decode('utf-8')
            if err is not None:
                output_dialog_text += err.decode('utf-8')
        
            QgsMessageLog.logMessage("Your plugin code has been executed correctly", 'MyPlugin', Qgis.Info)
            QgsMessageLog.logMessage(str(args), 'MyPlugin', Qgis.Info)
            print("output is", out, err)
            QgsMessageLog.logMessage(str(out), 'MyPlugin', Qgis.Info)
            QgsMessageLog.logMessage(str(err), 'MyPlugin', Qgis.Info)
            self.output_dialog.commandText.setText(args_message)
            self.output_dialog.outputText.setText(output_dialog_text)
            test = self.output_dialog.exec_()
            output_path = self.dlg.outputQgsFileWidget.filePath()
            rlayer = QgsRasterLayer(output_path, os.path.basename(output_path))
            if not rlayer.isValid():
                QgsMessageLog.logMessage("Layer failed to load!", 'MyPlugin', Qgis.Info)