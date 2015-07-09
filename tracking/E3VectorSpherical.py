#!/usr/bin/env python
# *********************************************************************
# * Copyright (C) 2015 Luca Baldini (luca.baldini@pi.infn.it)         *
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

from e3pipe.tracking.E3Vector import E3Vector



class E3VectorSpherical(E3Vector):

    """ Small inherited class for initializing a vector from the
    two spherical angles theta and phi.

    Note that by default theta and phi are both given in radians---you should
    set the argument deg to True if you want to pass values in degrees.
    """

    def __init__(self, theta, phi, deg = False):
        """ Constructor.
        """
        if deg:
            theta = math.radians(theta)
            phi = math.radians(phi)
        xdir = math.cos(phi)*math.sin(theta)
        ydir = math.sin(phi)*math.sin(theta)
        zdir = math.cos(theta)
        E3Vector.__init__(self, xdir, ydir, zdir)




if __name__ == '__main__':
    v = E3VectorSpherical(math.pi/3., math.pi/4.)
    print v
    print v.mag()
    print v.theta()
    print v.phi()
    v = E3VectorSpherical(60., 45., True)
    print v
    print v.mag()
    print v.theta()
    print v.phi()
