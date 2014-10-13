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

from e3pipe.dqm.E3Alarm import E3Alarm



class alarm_y_values(E3Alarm):

    """ Derived class for setting alarm on the average y-values of a
    histogram.
    """

    SUPPORTED_ROOT_TYPES = ['TH1I', 'TH1F', 'TH1D']
    SUPPORTED_PARAMETERS = []
    SUPPORTED_CONDITIONS = []
    OUTPUT_DESCRIPTION = 'the worst y value'

    def run(self):
        """ Overloaded method.
        """
        obj = self.rootObject()
        worstBadness = None
        for i in range(1, obj.GetNbinsX() + 1):
            value = obj.GetBinContent(i)
            error = obj.GetBinError(i)
            badness = self.valueBadness(value, error)
            if worstBadness is None or badness > worstBadness:
                worstBadness = badness
                (worstBin, worstValue, worstError) = (i, value, error)
        self.setValue(worstValue, worstError, worstBadness)
        self.setInfo('worst_bin', worstBin)
        self.setInfo('worst_value', worstValue)
        self.setInfo('worst_error', worstError)

    def draw(self):
        """ Overloaded method.
        """
        import ROOT
        from e3pipe.root.E3Line import E3Line, E3YellowLine, E3RedLine
        ROOT.gPad.Update()
        ymin = self.errorMin()
        ymax = self.errorMax()
        self.rootObject().GetYaxis().SetRangeUser(ymin, ymax)
        xmin = ROOT.gPad.GetUxmin()
        xmax = ROOT.gPad.GetUxmax()
        if ROOT.gPad.GetLogx():
            xmin = 10**xmin
            xmax = 10**xmax
        for y in [self.warningMin(), self.warningMax()]:
            l = E3YellowLine(xmin, y, xmax, y)
            l.Draw()
        for y in [self.errorMin(), self.errorMax()]:
            l = E3RedLine(xmin, y, xmax, y)
            l.Draw()



def test():
    """ Test program.
    """
    import ROOT
    h = ROOT.TH1F('h', 'h', 100, 0, 1)
    h.FillRandom('pol0', 10000)
    a = alarm_y_values(h, 10, 90, 110, 150)
    a.run()
    print a


if __name__ == '__main__':
    test()

