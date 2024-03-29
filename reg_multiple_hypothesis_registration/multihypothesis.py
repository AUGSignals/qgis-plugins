# -*- coding: utf-8 -*-
"""
/***************************************************************************
 MultiHypothesis
                                 A QGIS plugin
 This plugin runs the Multiple Hypothesis Sequential Scene Matching program.
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2020-12-15
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
from qgis.PyQt.QtWidgets import QAction, QWidget, QMenu, QMessageBox
from qgis.core import QgsMessageLog, Qgis, QgsProject, QgsRasterLayer, QgsMapLayer


# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .multihypothesis_dialog import MultiHypothesisDialog
from .output_dialog import OutputDialog
import os.path


class MultiHypothesis:
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
        self.output_dialog = OutputDialog()
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'MultiHypothesis_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Multiple Hypothesis Scene Matching')

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
        return QCoreApplication.translate('MultiHypothesis', message)


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
        self.menu = self.iface.mainWindow().findChild(QMenu, '&Image Registration')
        if not self.menu:
            self.menu = QMenu(self.iface.mainWindow())
            self.menu.setObjectName('&Image Registration')
            self.menu.setTitle('&Image Registration')
        self.action = QAction(QIcon(":/plugins/lee_sigma_filter/icon.png"),
                                    "Multiple Hypothesis Scene Matching",
                                    self.iface.mainWindow())
        self.action.setObjectName("testAction")
        self.action.setWhatsThis("Configuration for test plugin")
        self.action.setStatusTip("This is status tip")
        self.action.triggered.connect(self.run)

        self.menu.addAction(self.action)

        menuBar = self.iface.mainWindow().menuBar()
        menuBar.insertMenu(self.iface.firstRightStandardMenu().menuAction(),
                       self.menu)


    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""
        self.addToCustomMenu()
        """

        icon_path = ':/plugins/contour_detection/icon.png'
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
                self.tr(u'&Multiple Hypothesis Sequential Scene Matching'),
                action)
            self.iface.removeToolBarIcon(action)


    def pageChange(self, pagesToChange):
        curIndex = self.dlg.stackedWidget.currentIndex()
        if (curIndex == 2 and pagesToChange == 1 and not self.featureImagePairs):
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText("Reference and Warp Feature Images Required")
            msgBox.setWindowTitle("Missing Entries")
            msgBox.setStandardButtons(QMessageBox.Ok)

            returnValue = msgBox.exec()
            if returnValue == QMessageBox.Ok:
                return
        elif (curIndex == 3 and pagesToChange == 1 and not self.originalImagePairs):
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText("Reference and Warp Original Image Pair Required")
            msgBox.setWindowTitle("Missing Entries")
            msgBox.setStandardButtons(QMessageBox.Ok)

            returnValue = msgBox.exec()
            if returnValue == QMessageBox.Ok:
                return
        curIndex += pagesToChange
        if curIndex < 0 or curIndex == 0:
            curIndex = 0
            self.dlg.previousButton.setEnabled(False)
        else:
            self.dlg.previousButton.setEnabled(True)
        if curIndex >= self.dlg.stackedWidget.count() or curIndex == self.dlg.stackedWidget.count() - 1:
            curIndex = self.dlg.stackedWidget.count() - 1
            self.dlg.nextButton.setEnabled(False)
        else:
            self.dlg.nextButton.setEnabled(True)
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
        featureImagePair = (self.dlg.referenceTopLeftLineEdit.text(), self.dlg.displacementLineEdit.text(), self.dlg.featureReferenceImageQgsFileWidget.filePath(), self.dlg.featureWarpImageQgsFileWidget.filePath())
        self.featureImagePairs.append(featureImagePair)
        self.dlg.featureImageList.addItem('Top Left: ' + str(featureImagePair[0]) + ', ' + 'Displacement: ' + str(featureImagePair[1]) + ', ' + 'Reference: ' + str(featureImagePair[2]) + ', ' + 'Warp: ' + str(featureImagePair[3]))

    def featureImageDelete(self):
        selectedIndex = self.dlg.featureImageList.currentRow()
        if selectedIndex >= 0:
            self.dlg.featureImageList.takeItem(selectedIndex)
            del self.featureImagePairs[selectedIndex]

    def originalImageAdd(self):
        originalImage = self.dlg.originalWarpImageQgsFileWidget.filePath()
        if originalImage and len(self.originalImagePairs) <= len(self.featureImagePairs):
            self.originalImagePairs.append(originalImage)
            self.dlg.originalImageList.addItem(originalImage)

    def originalImageDelete(self):
        selectedIndex = self.dlg.originalImageList.currentRow()
        if selectedIndex >= 0:
            self.dlg.originalImageList.takeItem(selectedIndex)
            del self.originalImagePairs[selectedIndex]

    def run(self):
        """Run method that performs all the real work"""

        # Create the dialog with elements (after translation) and keep reference
        # Only create GUI ONCE in callback, so that it will only load when the plugin is started
        self.featureImagePairs = []
        self.originalImagePairs = []
        if self.first_start == True:
            self.first_start = False
            self.dlg = MultiHypothesisDialog()
            self.dlg.previousButton.setEnabled(False)
            self.dlg.previousButton.clicked.connect(lambda: self.pageChange(-1))
            self.dlg.nextButton.clicked.connect(lambda: self.pageChange(1))
            self.dlg.scalingAddButton.clicked.connect(self.scalingAdd)
            self.dlg.scalingDeleteButton.clicked.connect(self.scalingDelete)
            self.dlg.featureImageAddButton.clicked.connect(self.featureImageAdd)
            self.dlg.featureImageDeleteButton.clicked.connect(self.featureImageDelete)
            self.dlg.originalImageAddButton.clicked.connect(self.originalImageAdd)
            self.dlg.originalImageDeleteButton.clicked.connect(self.originalImageDelete)

        # Start the widget on the first page
        self.dlg.stackedWidget.setCurrentIndex(0)
        self.scalingPairs = []

        self.dlg.scalingList.clear()
        self.dlg.featureImageList.clear()
        self.dlg.originalImageList.clear()

        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            self.configContents = {}
            self.configContents['numTests'] = self.dlg.numberOfTestsSpinBox.value()
            self.configContents['transformationType'] = self.dlg.transformationTypeComboBox.currentIndex()
            self.configContents['downsample'] = int(self.dlg.downsampleQgsSpinBox.text())
            self.configContents['windowSize'] = int(self.dlg.windowSizeSpinBox.text())
            self.configContents["warpWindow"] = int(self.dlg.warpWindowQgsSpinBox.text())
            self.configContents['interpolationMethod'] = self.dlg.interpolationMethodComboBox.currentIndex()
            self.configContents['searchMethod'] = self.dlg.searchMethodComboBox.currentIndex()
            self.configContents['similarityMetrics'] = self.dlg.similarityMetricsComboBox.currentIndex()
            self.configContents['padding'] = int(self.dlg.paddingSpinBox.text())
            self.configContents['borderPaddingValue'] = float(self.dlg.borderPaddingValueDoubleSpinBox.text())
            self.configContents['scaleDelta'] = float(self.dlg.scaleIncrementValueQDoubleSpinBox.text())
            self.configContents['rotationDelta'] = float(self.dlg.rotationIncrementValueDoubleSpinBox.text())
            scaling = []
            for s in self.scalingPairs:
                scaleObj = {'scaleLowerValue': s[0], 'scaleUpperValue': s[1]}
                scaling.append(scaleObj)
            self.configContents['scaling'] = scaling
            self.configContents['rotationFactor'] = {'LowerRotationalBound': float(self.dlg.lowerRotationFactorBoundDoubleSpinBox.text()), 'UpperRotationalBound': float(self.dlg.upperRotationFactorBoundDoubleSpinBox.text())}
            logFilePath = Path(self.dlg.logFileQgsFileWidget.filePath())
            self.configContents["log"] = {"logDirectory":os.path.join(str(logFilePath.parent), ''), "logFilename":str(logFilePath.name)}

            featImages = []
            for featureImage in self.featureImagePairs:
                def parseArray(a):
                    b = a.replace('[', '').replace(']', '').split(",")
                    c = []
                    for elem in b:
                        c.append(int(elem))
                    return c
                refTopLeft = parseArray(featureImage[0])
                displacement = parseArray(featureImage[1])
                f = {'refTopLeft': refTopLeft, 'displacement': displacement, 'layer': [{'refFilename': featureImage[2], 'warpFilename': featureImage[3]}]}
                featImages.append(f)
            self.configContents['featImages'] = featImages
            self.configContents['origReference'] = {'filename': self.dlg.originalReferenceImageQgsFileWidget.filePath()}
            self.configContents['origWarp'] = [{'filename':item} for item in self.originalImagePairs]
            self.configContents['outputImage'] = {
                'outputDirectory': str(self.dlg.outputDirectoryQgsFileWidget.filePath()) + "\\",
                'referenceUnion': self.dlg.referenceUnionLineEdit.text(),
                'warpUnion': self.dlg.warpUnionLineEdit.text(),
                'warpIntersect': self.dlg.warpIntersectLineEdit.text(),
                'transMat': self.dlg.trasformationMatrixLineEdit.text(),
                'finalControlPoints': self.dlg.finalControlPointsLineEdit.text()
            }
            args = []

            s = QSettings()
            path = s.value("qgis-exe/path")
            config_path = path + "/" + 'config-multihypothesis.toml'
            with open(config_path, 'w') as f:
                toml_string = toml.dump(self.configContents, f)
            args.append("-c")
            args.append(config_path)

            exeName = "mulhypseqsm.exe"
            path = path + "/" + exeName
            args.insert(0, path)
            args_message = " ".join(arg for arg in args)

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
            self.output_dialog.outputText.setText("The output flow log is stored in {}".format(logFilePath))
            output_dlg = self.output_dialog.exec_()
            