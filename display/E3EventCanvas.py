#!/usr/bin/env python
# *********************************************************************
# * Copyright (C) 2014 Luca Baldini (luca.baldini@pi.infn.it)         *
# *                                                                   *
# * For the license terms see the file LICENCE, distributed           *
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


X_MIN = 0.
X_MAX = 158.0
NUM_STRIPS = 24
STRIP_PITCH = 3.2
Y_MIN = 0.5*STRIP_PITCH
Y_MAX = STRIP_PITCH*(NUM_STRIPS - 0.5)
DX = X_MAX - X_MIN
DY = Y_MAX - Y_MIN


from e3pipe.display.E3PhysicalCanvas import E3PhysicalCanvas
from e3pipe.display.__geometry2d__ import *



class E3EventCanvas(E3PhysicalCanvas):
    """
    """

    NAME = 'cdisplay'
    TITLE = 'EEE event display'
    WPX = 1200
    PLANE_THICKNESS = 2.

    def __init__(self, z = [0, 40, 80], padding = 30., **kwargs):
        """ Constructor.
        """
        self.__Z = z
        self.__Pad = padding
        dz = max(z) - min(z)
        self.__W = self.__Pad*4 + DX + DY
        self.__H = self.__Pad*2 + dz
        E3PhysicalCanvas.__init__(self, self.NAME, self.__W, self.__H,
                                  self.WPX,  title = self.TITLE, logo = False)
        self.drawTelescope()
        self.drawReference()

    def xz2canvas(self, x, z):
        """ Convert from physical units to canvas coordinates (x-z plane).
        """
        _x = x + self.__Pad - 0.5*self.__W
        _z = z + self.__Pad - 0.5*self.__H
        return (_x, _z)

    def yz2canvas(self, y, z):
        """ Convert from physical units to canvas coordinates (y-z plane).
        """
        _y = y + 3*self.__Pad + DX - 0.5*self.__W
        _z = z + self.__Pad - 0.5*self.__H
        return (_y, _z)

    def drawTelescope(self):
        """ Draw the three planes of the telescope.
        """
        for z in self.__Z:
            box(0.5*DX - 0.5*self.__W + self.__Pad,
                z - 0.5*self.__H + self.__Pad,
                DX, self.PLANE_THICKNESS)
            box(0.5*DY - 0.5*self.__W + DX + 3*self.__Pad,
                z - 0.5*self.__H + self.__Pad,
                DY, self.PLANE_THICKNESS)

    def drawReference(self):
        """ Draw the reference system.
        """
        _l = 0.4*self.__Pad
        _x, _z = self.xz2canvas(-0.5*self.__Pad, -0.5*self.__Pad)
        arrow(_x, _z, _x + _l, _z)
        annotate(_x + _l, _z, ' x', align = 13)
        arrow(_x, _z, _x, _z + _l)
        annotate(_x, _z + _l, 'z ', align = 31)
        _y, _z = self.yz2canvas(-0.5*self.__Pad, -0.5*self.__Pad)
        arrow(_y, _z, _y + _l, _z)
        annotate(_y + _l, _z, ' y', align = 13)
        arrow(_y, _z, _y, _z + _l)
        annotate(_y, _z + _l, 'z ', align = 31)

    def drawPoint(self, x, y, z):
        """ Draw a three-dimensional point.
        """
        _x, _z = self.xz2canvas(x, z)
        marker(_x, _z)
        _y, _z = self.yz2canvas(y, z)
        marker(_y, _z)
        self.Update()


if __name__ == '__main__':
    c = E3EventCanvas()
    c.Draw()
    c.drawPoint(100, 34, 40)
