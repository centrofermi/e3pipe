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

    Note we only parse a few fields, for the time being.
    """
    
    def __init__(self, *args):
        """
        """
        pos1 = args[9]
        pos2 = args[10]
        pos3 = args[11]
        pos4 = args[12]
        self.__LatitudeDegrees = pos1 & 0x7F
        self.__LatitudeMinutes = (pos1 >> 7) & 0x3F

        
    def __str__(self):
        """
        """
        return 'Latitude: %d deg %d.0\'' %\
            (self.__LatitudeDegrees, self.__LatitudeMinutes)
