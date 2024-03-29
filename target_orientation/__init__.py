# -*- coding: utf-8 -*-
"""
/***************************************************************************
 TargetOrientation
                                 A QGIS plugin
 This plugin finds the orientation of a target in an image
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2021-01-28
        copyright            : (C) 2021 by Terry/AUG Signals
        email                : terry@augsignals.com
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
    """Load TargetOrientation class from file TargetOrientation.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .target_orientation import TargetOrientation
    return TargetOrientation(iface)
