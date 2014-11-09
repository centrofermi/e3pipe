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


import array
import ROOT


class E3ColorPalette:

    """ Set a color palette from a given RGB list.
    stops, red, green and blue should all be lists of the same length
    from http://ultrahigh.org/2007/08/20/making-pretty-root-color-palettes/
    """
   
    def __init__(self, name, stops, red, green, blue):
        """
        """
        self.Name = name
        self.Stops = array.array('d', stops)
        self.Red = array.array('d', red)
        self.Green = array.array('d', green)
        self.Blue = array.array('d', blue)

    def __len__(self):
        """
        """
        return len(self.Stops)

    def createGradientColorTable(self, rootStyle, contours = 250):
        """
        """
        ROOT.TColor.CreateGradientColorTable(len(self), self.Stops, self.Red,
                                             self.Green, self.Blue, contours)
        rootStyle.SetNumberContours(contours)



DEFAULT_COLOR_PALETTE = E3ColorPalette('Default',
                                       [0.00, 0.34, 0.61, 0.84, 1.00],
                                       [0.00, 0.00, 0.87, 1.00, 0.51],
                                       [0.00, 0.81, 1.00, 0.20, 0.00],
                                       [0.51, 1.00, 0.12, 0.00, 0.00])



if __name__ == '__main__':
    DEFAULT_COLOR_PALETTE.createGradientColorTable(ROOT.gStyle)
