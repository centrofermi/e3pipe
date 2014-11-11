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

from e3pipe.mc.E3Point import E3Point



class E3Vector(E3Point):

    """ Small class encapsulating a point in the three-dimensional space.
    """

    def mag2(self):
        """ Return the magnutude squared of the vector.
        """
        return self.x()**2 + self.y()**2 + self.z()**2

    def mag(self):
        """ Return the magnutude of the vector.
        """
        return math.sqrt(self.mag2())

    def theta(self):
        """ Return the theta angle corresponding to the vector.
        """
        return math.degrees(math.acos(self.z()/self.mag()))

    def phi(self):
        """ Return the phi angle corresponding to the vector.
        """
        return math.degrees(math.atan2(self.y(), self.x()))

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
