# -*- coding: utf-8 -*-
"""
/***************************************************************************
 FrenchAddress
                                 A QGIS plugin
 Recherche et localisation d'adresse française.
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2020-04-20
        copyright            : (C) 2020 by Guillaume DELPLANQUE
        email                : delpro.guillaume@gmail.com
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
    """Load FrenchAddress class from file FrenchAddress.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .french_address import FrenchAddress
    return FrenchAddress(iface)
