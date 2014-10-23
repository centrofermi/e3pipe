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
from e3pipe.root.E3RootObject import E3RootObject
from e3pipe.dst.__time__ import E3_TIME_OFFSET


class E3H1D(ROOT.TH1D, E3RootObject):

    """ Wrapper around the ROOT.TLatex object.
    """

    def __init__(self, name, title, xbins, xmin, xmax, **kwargs):
        """ Constructor.
        """
        ROOT.TH1D.__init__(self, name, title, xbins, xmin, xmax)
        E3RootObject.init(self, **kwargs)

    def Draw(self, opts = '', **kwargs):
        """
        """
        ROOT.TH1D.Draw(self, opts)
        self.setupStatBox(**kwargs)

    def SetTimeDisplay(self):
        """ TODO: this is redundant with the function in root.__ROOT__.py
        """
        self.GetXaxis().SetTitle('')
        self.GetXaxis().SetTimeDisplay(True)
        self.GetXaxis().SetTimeOffset(E3_TIME_OFFSET)

    def setupStatBox(self, **kwargs):
        """ Set the stat box color, options and position.
        
        From http://root.cern.ch/root/html/THistPainter.html:
        In a script file the painting should be forced using gPad->Update()
        in order to make sure the statistics box is created:
        > h->Draw();
        > gPad->Update();
        > TPaveStats *st = (TPaveStats*)h->FindObject("stats");
        Without gPad->Update() the line h->FindObject("stats") returns
        a null pointer. 
        """
        ROOT.gPad.Update()
        statBox = self.FindObject('stats')
        # Make sure we really grabbed the stat box; if that fails we end up
        # here with a ROOT.TObject instance instead of a ROOT.TPaveStats
        # instance.
        if not isinstance(statBox, ROOT.TPaveStats):
            return
        statRow = kwargs.get('statrow' , 0)
        statCol = kwargs.get('statcol' , 0)
        statMode = kwargs.get('statmode', 111110)        
        textSize = kwargs.get('textsize', SMALLER_TEXT_SIZE)
        x1 = kwargs.get('statx1', 0.76)
        y1 = kwargs.get('staty1', 0.70)
        x2 = kwargs.get('statx2', 0.94)
        y2 = kwargs.get('staty2', 0.90)
        statBox.SetTextColor(self.GetLineColor())
        statBox.SetOptStat(statMode)
        width  = x2 - x1
        height = y2 - y1
        dx = 1.05*statCol*width
        dy = 1.05*statRow*height
        statBox.SetX1NDC(x1 + dx)
        statBox.SetX2NDC(x2 + dx)
        statBox.SetY1NDC(y1 + dy)
        statBox.SetY2NDC(y2 + dy)
        statBox.SetTextSize(textSize)
        ROOT.gPad.Modified()
        ROOT.gPad.Update()



def test():
    l = E3H1D('htest', 'htest', 100, 0, 1, XTitle = 'x [a.u.]')
    l.Draw()
    ROOT.gPad.Update()


if __name__ == '__main__':
    test()
