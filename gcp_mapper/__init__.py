# -*- coding: utf-8 -*-
"""
/***************************************************************************
 GCPMap
                                 A QGIS plugin
 This plugin matches control points and outputs a corresponding csv.
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2021-08-26
        copyright            : (C) 2021 by A.U.G Signals
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
    """Load GCPMap class from file GCPMap.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .gcp_mapper import GCPMap
    return GCPMap(iface)
