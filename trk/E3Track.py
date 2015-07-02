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


from e3pipe.trk.E3Point import E3Point
from e3pipe.trk.E3Vector import E3Vector


class E3Track:

    """ Class representing a track.
    """
    
    def __init__(self, origin, direction, chi2 = -1.):
        """ Constructor.
        """
        self.__Origin = origin
        self.__Direction = direction
        self.__Chi2 = chi2

    def setChi2(self, chi2):
        """ Set the track chisquare.
        """
        self.__Chi2 = chi2

    def origin(self):
        """ Return the starting point of the track.
        """
        return self.__Origin

    def direction(self):
        """ Return the track direction.
        """
        return self.__Direction

    def chi2(self):
        """ Return the track chisquare.
        """
        return self.__Chi2
    
    def x0(self):
        """ Return the x-coordinate of the starting point of the track.
        """
        return self.__Origin.x()
        
    def y0(self):
        """ Return the y-coordinate of the starting point of the track.
        """
        return self.__Origin.y()

    def z0(self):
        """ Return the z-coordinate of the starting point of the track.
        """
        return self.__Origin.z()

    def xdir(self):
        """ Return the x cosine director of the track direction.
        """
        return self.__Direction.x()

    def ydir(self):
        """ Return the y cosine director of the track direction.
        """
        return self.__Direction.y()

    def zdir(self):
        """ Return the z cosine director of the track direction.
        """
        return self.__Direction.z()

    def theta(self):
        """
        """
        return self.__Direction.theta()

    def phi(self):
        """
        """
        return self.__Direction.phi()

    def extrapolate(self, z):
        """
        """
        x = self.x0() + (z - self.z0())*self.xdir()/self.zdir()
        y = self.y0() + (z - self.z0())*self.ydir()/self.zdir()
        return E3Point(x, y, z)

    def __str__(self):
        """ String formatting
        """
        return '%s -> %s (chi2 = %.3f)' %\
            (self.origin(), self.direction(), self.chi2())



if __name__ == '__main__':
    p = E3Point(50., 50., 100)
    v = E3Vector(0, 0, 1)
    t = E3Track(p, v)
    print t
    print t.phi(), t.theta()
    print t.extrapolate(0)

