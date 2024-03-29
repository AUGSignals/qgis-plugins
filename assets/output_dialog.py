# -*- coding: utf-8 -*-
import os

from qgis.PyQt import uic
from qgis.PyQt import QtWidgets

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'output_dialog.ui'))


class OutputDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        super(OutputDialog, self).__init__(parent)
        self.setupUi(self)