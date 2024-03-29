# -*- coding: utf-8 -*-
"""
/***************************************************************************
 FourierTransform
                                 A QGIS plugin
 This process performs a fourier transform on the selected image.
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
    """Load FourierTransform class from file FourierTransform.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .fourier_transform import FourierTransform
    return FourierTransform(iface)
