# -*- coding: utf-8 -*-
"""
/***************************************************************************
 HuMoments
                                 A QGIS plugin
 This plugin launches a Hu Moments process
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2020-07-27
        copyright            : (C) 2020 by Tomas/AUG Signals
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
    """Load HuMoments class from file HuMoments.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .hu_moment import HuMoments
    return HuMoments(iface)
