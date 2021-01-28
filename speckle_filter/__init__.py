# -*- coding: utf-8 -*-
"""
/***************************************************************************
 SpeckleFilter
                                 A QGIS plugin
 This plugin loads the speckle filter and sets parameters
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2020-07-16
        copyright            : (C) 2020 by tomas
        email                : tomas@augsignals.com
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
    """Load SpeckleFilter class from file SpeckleFilter.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .speckle_filter import SpeckleFilter
    return SpeckleFilter(iface)