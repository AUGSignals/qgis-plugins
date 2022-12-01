# -*- coding: utf-8 -*-
"""
/***************************************************************************
 MultiCFAR
                                 A QGIS plugin
 This plugin launches a multi CFAR process.
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2021-01-29
        copyright            : (C) 2021 by AUG Signals
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
    """Load MultiCFAR class from file MultiCFAR.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .multi_cfar import MultiCFAR
    return MultiCFAR(iface)