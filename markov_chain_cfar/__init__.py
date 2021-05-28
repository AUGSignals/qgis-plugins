# -*- coding: utf-8 -*-
"""
/***************************************************************************
 MarkovChainCFAR
                                 A QGIS plugin
 This plugin launches a process of a markov chain CFAR.
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2021-04-08
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
    """Load MarkovChainCFAR class from file MarkovChainCFAR.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .markov_chain_cfar import MarkovChainCFAR
    return MarkovChainCFAR(iface)