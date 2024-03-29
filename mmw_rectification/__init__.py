# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Rectification
                                 A QGIS plugin
 This plugin performs geo-rectification on MMW imagery 
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2022-10-11
        copyright            : (C) 2022 by Nusaibah Alhadhrami
        email                : nusaibah.alhadhrami@bayanat.ai
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
    """Load Rectification class from file rectification.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .rectification import Rectification
    return Rectification(iface)
