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


from e3pipe.root.__ROOT__ import *



class E3Legend(ROOT.TLegend):
    """ Small wrapper around the ROOT.TLegend class.

    TODO: this might inherit from E3RootObject.
    """
    
    LINE_LENGTH = 0.250
    ROW_SPACING = 0.055

    def __init__(self, x = 0.16, y = 0.9, entries = []):
        """ Constructor. (x, y) are the coordinates of the top-left corner.
        """
        ROOT.TLegend.__init__(self, x, y, x + self.LINE_LENGTH, y)
        self.SetTextFont(TEXT_FONT)
        self.SetTextSize(LEGEND_TEXT_SIZE)
        self.SetFillStyle(0)
        for entry in entries:
            self.AddEntry(entry)

    def vstretch(self, factor):
        """ Stretch the legend vertically.
        """
        self.SetY1(self.GetY2() - factor*(self.GetY2() - self.GetY1()))

    def AddEntry(self, plot, label = None, options = 'lp'):
        """ Overload method for constant spacing between rows.
        """
        if plot is None:
            return
        if label is None:
            label = plot.GetTitle()
        ROOT.TLegend.AddEntry(self, plot, label, options)
        self.SetY1(self.GetY1() - self.ROW_SPACING)

    def AddEntries(self, plots, options = 'lp'):
        """ Add a list of plots to the captions.
        """
        for plot in plots:
            self.AddEntry(plot, None, options)
