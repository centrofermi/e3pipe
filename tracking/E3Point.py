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



class E3Point:

    """ Small class encapsulating a point in the three-dimensional space.
    """

    def __init__(self, x, y, z):
        """ Constructor.
        """
        self.__X = float(x)
        self.__Y = float(y)
        self.__Z = float(z)

    def x(self):
        """ Return the x coordinate.
        """
        return self.__X

    def y(self):
        """ Return the y coordinate.
        """
        return self.__Y

    def z(self):
        """ Return the z coordinate.
        """
        return self.__Z

    def __add__(self, other):
        """
        """
        return E3Point(self.x() + other.x(),
                       self.y() + other.y(),
                       self.z() + other.z()) 

    def __sub__(self, other):
        """
        """
        return E3Point(self.x() - other.x(),
                       self.y() - other.y(),
                       self.z() - other.z())

    def __str__(self):
        """ String representation.
        """
        return 'P(%.3f, %.3f, %.3f)' % (self.x(), self.y(), self.z())
        


if __name__ == '__main__':
    p = E3Point(2, 3, 4)
    print p
