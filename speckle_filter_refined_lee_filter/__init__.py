# -*- coding: utf-8 -*-
"""
/***************************************************************************
 RefinedLeeFilter
                                 A QGIS plugin
 This plugin launches the refined lee filter algorithm.
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2020-07-22
        copyright            : (C) 2020 by Tomas
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
    """Load RefinedLeeFilter class from file RefinedLeeFilter.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .refined_lee_filter import RefinedLeeFilter
    return RefinedLeeFilter(iface)
