# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ClassifierTrainer
                                 A QGIS plugin
 This plugin launches the Classification Training Process
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2021-03-04
        copyright            : (C) 2021 by AUG Signals
        email                : tomas@augsignal.coms
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load ClassifierTrainer class from file ClassifierTrainer.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .classifier_trainer import ClassifierTrainer
    return ClassifierTrainer(iface)
