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


from e3pipe.root.E3Canvas import *



class E3PhysicalCanvas(E3Canvas, E3RootObject):

    """ A canvas to drow stuff in physical units.

    From the ROOT docs.
    c->SetWindowSize(w + (w - c->GetWw()), h + (h - c->GetWh()));
    """

    def __init__(self, name, width, height, wpx = None, title = None, **kwargs):
        """ Conctructor.
        """
        E3Canvas.__init__(self, name, title, **kwargs)
        wpx = wpx or self.GetWindowWidth()
        hpx = int(wpx*height/float(width) + 0.5) +\
              (self.GetWindowHeight() - self.GetWh()) -\
              (self.GetWindowWidth() - self.GetWw())
        self.SetWindowSize(wpx, hpx)
        self.SetBottomMargin(0.)
        self.SetTopMargin(0.)
        self.SetLeftMargin(0.)
        self.SetRightMargin(0.)
        self.Range(-0.5*width, -0.5*height, 0.5*width, 0.5*height)



if __name__ == '__main__':
    c = E3PhysicalCanvas('ctest', 300, 300)
    l = ROOT.TLine(0, 0, 100, 100)
    l.Draw()
    c.Update()
