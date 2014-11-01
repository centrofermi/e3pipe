#!/usr/bin/env python
# *********************************************************************
# * Copyright (C) 2014 Luca Baldini (luca.baldini@pi.infn.it)         *
# *                                                                   *
# * For the license terms see the file LICENSE, distributed           *
# * along with this software.                                         *
# *********************************************************************
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.



class E3GpsRecord:

    """ Utility class encapsulating a GPS record.

    The documentation is coming from the GPS 2092 data sheet, particularly:

    10 (pos1): 0-6  : 7 bits of Latitude degrees
               7-12 : 6 bits of Latitude minutes
               13-15: Low 3 bits of fraction of a minute of Latitude.
    11 (pos2): 0-6  : High 7 bits of fraction of a minute of Latitude
                      (thousandths).
               7    : North/South flag bit (1 = North).
               8-15 : 8 bits of Longitude in degrees.
    12 (pos3): 0-5  : 6 bits of Longitude minutes,
               6-15 : 10 bits of fraction of a minute of Longitude
                      (thousandths).
    13 (pos4): 0    : One bit East/West flag (1 = East).
               1-12 : 12 bits of Altitude in m.
               13   : One bit flag for above/below sea level (1 = above).

    Note we only parse a few fields, for the time being.
    """
    
    def __init__(self, *args):
        """ Constructor.
        """
        pos1 = args[9]
        pos2 = args[10]
        pos3 = args[11]
        pos4 = args[12]
        latDeg = pos1 & 0x7F
        latMin = (pos1 >> 7) & 0x3F
        latMinFrac = ((pos1 >> 13) & 0x7) + ((pos2 & 0x7F) << 3)
        north = (pos2 >> 7) & 0x1
        lonDeg = (pos2 >> 8) & 0xFF
        lonMin = pos3 & 0x3F
        lonMinFrac = (pos3 >> 6) & 0x3FF
        east = pos4 & 0x1
        alt = (pos4 >> 1) & 0xFFF
        asl = (pos4 >> 13) & 0x1
        self.__Latitude = latDeg + (latMin + 0.001*latMinFrac)/60.
        if not north:
            self.__Latitude *= -1.
        self.__Longitude = lonDeg + (lonMin + 0.001*lonMinFrac)/60.
        if not east:
            self.__Longitude *= -1.
        self.__Altitude = alt
        if not asl:
            self.__Altitude *= -1.

    def latitude(self):
        """ Return the latitude.
        """
        return self.__Latitude

    def longitude(self):
        """ Return the longitude.
        """
        return self.__Longitude

    def altitude(self):
        """ Return the altitude,
        """
        return self.__Altitude
        
    def __str__(self):
        """ String formatting.
        """
        return 'Latitude %.12f deg, Longitude %.12f deg, altitude %d m' %\
            (self.latitude(), self.longitude(), self.altitude())
