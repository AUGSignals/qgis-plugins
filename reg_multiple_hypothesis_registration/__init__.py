# -*- coding: utf-8 -*-
"""
/***************************************************************************
 MultiHypothesis
                                 A QGIS plugin
 This plugin runs the Multiple Hypothesis Sequential Scene Matching program.
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2020-12-15
        copyright            : (C) 2020 by Chris
        email                : chris@augsignals.com
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
    """Load MultiHypothesis class from file MultiHypothesis.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .multihypothesis import MultiHypothesis
    return MultiHypothesis(iface)