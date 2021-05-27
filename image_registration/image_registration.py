# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ImageRegistration
                                 A QGIS plugin
 This plugin performs Image Registration
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2020-12-08
        git sha              : $Format:%H$
        copyright            : (C) 2020 by Chris
        email                : chris@augsignals.com
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
import toml
from pathlib import Path

from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QWidget, QMenu
from qgis.core import QgsMessageLog, Qgis, QgsProject, QgsRasterLayer, QgsMapLayer

# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .image_registration_dialog import ImageRegistrationDialog
from .output_dialog import OutputDialog
import os.path

class ImageRegistration:
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
            'ImageRegistration_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Image Registration')

        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.first_start = None

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('Multilayer Registration', message)


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
        self.menu = self.iface.mainWindow().findChild(QMenu, '&Image Registration')
        if not self.menu:
            self.menu = QMenu(self.iface.mainWindow())
            self.menu.setObjectName('&Image Registration')
            self.menu.setTitle('&Image Registration')
        self.action = QAction(QIcon(":/plugins/lee_sigma_filter/icon.png"),
                                    "Multilayer Registration",
                                    self.iface.mainWindow())
        self.action.setObjectName("Multilayer Registration")
        self.action.setWhatsThis("Configuration for test plugin")
        self.action.setStatusTip("This is the Image Registration config setup")
        self.action.triggered.connect(self.run)

        self.menu.addAction(self.action)

        menuBar = self.iface.mainWindow().menuBar()
        menuBar.insertMenu(self.iface.firstRightStandardMenu().menuAction(),
                       self.menu)

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""
        self.addToCustomMenu()

        # will be set False in run()
        self.first_start = True


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Multilayer Registration'),
                action)
            self.iface.removeToolBarIcon(action)

    def pageChange(self, pagesToChange):
        curIndex = self.dlg.stackedWidget.currentIndex()
        curIndex += pagesToChange
        if curIndex < 0:
            curIndex = 0
        if curIndex >= self.dlg.stackedWidget.count():
            curIndex = self.dlg.stackedWidget.count() - 1
        self.dlg.stackedWidget.setCurrentIndex(curIndex)

    def scalingAdd(self):
        scalingPair = (self.dlg.scalingLowerValueDoubleSpinBox.value(), self.dlg.scalingUpperValueDoubleSpinBox.value())
        self.scalingPairs.append(scalingPair)
        self.dlg.scalingList.addItem('Lower: ' + str(scalingPair[0]) + ', ' + 'Upper: ' + str(scalingPair[1]))

    def scalingDelete(self):
        selectedIndex = self.dlg.scalingList.currentRow()
        if selectedIndex >= 0:
            self.dlg.scalingList.takeItem(selectedIndex)
            del self.scalingPairs[selectedIndex]

    def featureImageAdd(self):
        featureImagePair = (self.dlg.featureReferenceImageQgsFileWidget.filePath(), self.dlg.featureWarpImageQgsFileWidget.filePath())
        self.featureImagePairs.append(featureImagePair)
        self.dlg.featureImageList.addItem('Reference: ' + str(featureImagePair[0]) + ', ' + 'Warp: ' + str(featureImagePair[1]))

    def featureImageDelete(self):
        selectedIndex = self.dlg.featureImageList.currentRow()
        if selectedIndex >= 0:
            self.dlg.featureImageList.takeItem(selectedIndex)
            del self.featureImagePairs[selectedIndex]

    def run(self):
        """Run method that performs all the real work"""

        # Create the dialog with elements (after translation) and keep reference
        # Only create GUI ONCE in callback, so that it will only load when the plugin is started
        if self.first_start == True:
            self.first_start = False
            self.dlg = ImageRegistrationDialog()
            self.dlg.previousButton.clicked.connect(lambda: self.pageChange(-1))
            self.dlg.nextButton.clicked.connect(lambda: self.pageChange(1))
            self.dlg.scalingAddButton.clicked.connect(self.scalingAdd)
            self.dlg.scalingDeleteButton.clicked.connect(self.scalingDelete)
            self.dlg.featureImageAddButton.clicked.connect(self.featureImageAdd)
            self.dlg.featureImageDeleteButton.clicked.connect(self.featureImageDelete)

        # Start the widget on the first page
        self.dlg.stackedWidget.setCurrentIndex(0)
        self.scalingPairs = []
        self.featureImagePairs = []
        self.dlg.scalingList.clear()
        self.dlg.featureImageList.clear()

        self.arguments = {}

        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            self.configContents = {}
            self.configContents["transformationType"] = self.dlg.transformationTypeComboBox.currentIndex()
            self.configContents["downsample"] = 1 if self.dlg.downsampleInputImageCheckBox.isChecked() else 0
            self.configContents["windowSize"] = int(self.dlg.windowSizeSpinBox.text())
            self.configContents["warpWindow"] = int(self.dlg.warpWindowQgsSpinBox.text())
            self.configContents["interpolationMethod"] = self.dlg.interpolationMethodComboBox.currentIndex()
            self.configContents["searchMethod"] = self.dlg.searchMethodComboBox.currentIndex()
            self.configContents["similarityMetrics"] = self.dlg.similarityMetricsComboBox.currentIndex()
            self.configContents["borderPaddingValue"] = float(self.dlg.borderPaddingValueDoubleSpinBox.text())
            self.configContents["scaleDelta"] = float(self.dlg.scaleIncrementValueQDoubleSpinBox.text())
            self.configContents["rotationDelta"] = float(self.dlg.rotationIncrementValueDoubleSpinBox.text())
            scaling = []
            for s in self.scalingPairs:
                scaleObj = {'scaleLowerValue': s[0], 'scaleUpperValue': s[1]}
                scaling.append(scaleObj)
            self.configContents['scaling'] = scaling
            self.configContents["rotationFactor"] = {"LowerRotationalBound":float(self.dlg.lowerRotationFactorBoundDoubleSpinBox.text()), 
                                                        "UpperRotationalBound":float(self.dlg.upperRotationFactorBoundDoubleSpinBox.text())}
            logFilePath = Path(self.dlg.logFileQgsFileWidget.filePath())
            self.configContents["log"] = {"logDirectory":str(logFilePath.parent), "logFilename":str(logFilePath.name)}
            featureImgs = []
            for f in self.featureImagePairs:
                featureObj = {'reference':f[0], 'warp':f[1]}
                featureImgs.append(featureObj)
            self.configContents["featureImage"] = featureImgs
            self.configContents["originalImage"] = {"reference":self.dlg.originalReferenceImageQgsFileWidget.filePath(), 
                                                    "warp":self.dlg.originalWarpImageQgsFileWidget.filePath()}
            self.configContents["outputImage"] = {
                "outputDirectory": self.dlg.outputDirectoryQgsFileWidget.filePath(),
                "referenceUnion": self.dlg.referenceUnionLineEdit.text(),
                "warpUnion": self.dlg.warpUnionLineEdit.text(),
                "warpIntersect": self.dlg.warpIntersectLineEdit.text(),
                "transMat": self.dlg.trasformationMatrixLineEdit.text(),
                "finalControlPoints": self.dlg.finalControlPointsLineEdit.text()
            }
            """
            self.arguments['-t'] = str(self.dlg.transformationTypeComboBox.currentIndex())
            self.arguments['-b'] = str(self.dlg.bandSpinBox.text())
            self.arguments['-d'] = self.dlg.downsampleInputImageCheckBox.isChecked()
            self.arguments['-k'] = str(self.dlg.windowSizeSpinBox.text())
            self.arguments['-r'] = str(self.dlg.interpolationMethodComboBox.currentIndex())
            self.arguments['-m'] = str(self.dlg.searchMethodComboBox.currentIndex())
            self.arguments['-n'] = str(self.dlg.similarityMetricsComboBox.currentIndex())
            self.arguments['-p'] = str(self.dlg.borderPaddingValueDoubleSpinBox.text())
            self.arguments['-c'] = str(self.dlg.scaleIncrementValueQDoubleSpinBox.text())
            self.arguments['-a'] = str(self.dlg.rotationIncrementValueDoubleSpinBox.text())
            self.arguments['-rf'] = str(self.dlg.lowerRotationFactorBoundDoubleSpinBox.text()) + ',' + str(self.dlg.upperRotationFactorBoundDoubleSpinBox.text())
            logFilePath = self.dlg.logFileQgsFileWidget.filePath()
            backslashPos = logFilePath.rfind('\\')
            self.arguments['-l'] = logFilePath[:backslashPos] + ',' + logFilePath[backslashPos + 1:]
            self.arguments['-i'] = self.dlg.originalReferenceImageQgsFileWidget.filePath() + ',' + self.dlg.originalWarpImageQgsFileWidget.filePath()


            outputFiles = self.dlg.outputDirectoryQgsFileWidget.filePath() + '\\'
            outputFiles += ',' + self.dlg.referenceUnionLineEdit.text()
            outputFiles += ',' + self.dlg.warpUnionLineEdit.text()
            outputFiles += ',' + self.dlg.warpIntersectLineEdit.text()
            outputFiles += ',' + self.dlg.trasformationMatrixLineEdit.text()
            outputFiles += ',' + self.dlg.finalControlPointsLineEdit.text()
            self.arguments['-o'] = outputFiles
            """

            args = []

            s = QSettings()
            path = s.value("qgis-exe/path")
            config_path = path + "/" + 'config-image-registration.toml'
            with open(config_path, 'w') as f:
                toml_string = toml.dump(self.configContents, f)
            args.append("-c")
            args.append(config_path)

            exeName = "Registration.exe"
            path = path + "/" + exeName
            args.insert(0, path)
            args_message = " ".join(arg for arg in args)

            popen = subprocess.Popen(args, stdout=subprocess.PIPE)
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
            output_dlg = self.output_dialog.exec_()
