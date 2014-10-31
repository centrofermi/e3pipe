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



class E3GeometryRecord:

    """ Utility class encapsulating a geometry record.

    Note we only parse a few fields, for the time being.
    """
    
    def __init__(self, *args):
        """
        """
        self.__Angle = args[0]/100.
        self.__Dist12 = float(args[1])
        self.__Dist23 = float(args[2])

    def angle(self):
        """
        """
        return self.__Angle

    def d12(self):
        """
        """
        return self.__Dist12

    def d23(self):
        """
        """
        return self.__Dist23

    def __str__(self):
        """ String formatting
        """
        return 'Angle to north: %.1f deg, d12 = %.1f cm, d23 = %.1f cm.' %\
            (self.angle(), self.d12(), self.d23())
    
