# -*- coding: utf-8 -*-
"""
/***************************************************************************
 RangeDopplerTerrainCorrection
                                 A QGIS plugin
 This plugin performs a Range Doppler Terrain Correction
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2020-08-17
        copyright            : (C) 2020 by Tomas/AUG Signals
        email                : tomas@augsignals
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
    """Load RangeDopplerTerrainCorrection class from file RangeDopplerTerrainCorrection.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .range_doppler import RangeDopplerTerrainCorrection
    return RangeDopplerTerrainCorrection(iface)
