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


import math

from e3pipe.tracking.E3Point import E3Point



class E3Vector(E3Point):

    """ Small class encapsulating a point in the three-dimensional space.
    """

    def __mul__(self, scalar):
        """
        """
        return E3Vector(self.x()*scalar, self.y()*scalar, self.z()*scalar)

    def __div__(self, scalar):
        """ Overloaded division operator.
        """
        if scalar == 0:
            raise ZeroDivisionError
        return E3Vector(self.x()/scalar, self.y()/scalar, self.z()/scalar)

    def __add__(self, other):
        """ Overloaded sum operator.
        """
        return E3Vector(self.x() + other.x(),
                        self.y() + other.y(),
                        self.z() + other.z()) 

    def __sub__(self, other):
        """ Overloaded subtraction operator.
        """
        return E3Vector(self.x() - other.x(),
                        self.y() - other.y(),
                        self.z() - other.z())
    
    def unit(self):
        """ Return the normalized unit vector.
        """
        return self/self.mag()

    def mag2(self):
        """ Return the magnutude squared of the vector.
        """
        return self.x()**2 + self.y()**2 + self.z()**2

    def mag(self):
        """ Return the magnutude of the vector.
        """
        return math.sqrt(self.mag2())

    def dot(self, other):
        """ Return the scalar product with another vector.
        """
        return self.x()*other.x() + self.y()*other.y() + self.z()*other.z()

    def cross(self, other):
        """ Return the vector product with another vector.
        """
        _x = self.y()*other.z() - self.z()*other.y()
        _y = self.z()*other.x() - self.x()*other.z()
        _z = self.x()*other.y() - self.y()*other.x()
        return E3Vector(_x, _y, _z)

    def theta(self):
        """ Return the theta angle corresponding to the vector.
        """
        return math.degrees(math.acos(self.z()/self.mag()))

    def phi(self):
        """ Return the phi angle corresponding to the vector.
        """
        return math.degrees(math.atan2(self.y(), self.x()))

    def rotatez(self, phi, deg = False):
        """ Return a new vector rotated by an angle phi around the zaxis.
        """
        if deg:
            phi = math.radians(phi)
        _x = self.x()*math.cos(phi) - self.y()*math.sin(phi)
        _y = self.x()*math.sin(phi) + self.y()*math.cos(phi)
        _z = self.z()
        return E3Vector(_x, _y, _z)

    def __str__(self):
        """ String representation.
        """
        return 'V(%.3f, %.3f, %.3f)' % (self.x(), self.y(), self.z())
        


if __name__ == '__main__':
    v = E3Vector(2, 3, 4)
    print v
    print v.mag()
    print v.theta()
    print v.phi()
    print v.rotatez(0., deg = True)
    print v.rotatez(90., deg = True)
    v1 = v.rotatez(36., deg = True)
    v2 = v1.rotatez(-36., deg = True)
    print v, v1, v2
