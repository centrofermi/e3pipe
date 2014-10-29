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


import ROOT

from e3pipe.__logging__ import logger
from e3pipe.dst.E3DstEventChain import E3DstEventChain


def e3eastwest(filePath, northAngle = 56.,
               baseCut = 'StatusCode == 0 && Theta > 30'):
    """
    """
    chain = E3DstEventChain(filePath)
    expr = 'Phi - %.3f + 360*(Phi - %.3f < -180) - 360*(Phi - %.3f > 180)' %\
           (northAngle, northAngle, northAngle)
    chain.SetAlias('PhiNorth', expr)
    h1 = ROOT.TH1F('h1', '#phi > 0 (East)', 200, 0, 180)
    h1.SetXTitle('abs(#phi) [#circ from North]')
    h1.SetLineColor(ROOT.kRed)
    h2 = ROOT.TH1F('h2', '#phi < 0 (West)', 200, 0, 180)
    h2.SetLineColor(ROOT.kBlue)
    cut1 = '%s && PhiNorth > 0' % baseCut
    chain.Project('h1', 'PhiNorth', cut1)
    cut2 = '%s && PhiNorth < 0' % baseCut
    chain.Project('h2', '-PhiNorth', cut2)
    hratio = h1.Clone('hratio')
    hratio.Divide(h2)
    return h1, h2, hratio
    


if __name__ == '__main__':
    from e3pipe.root.E3Canvas import E3Canvas
    from e3pipe.root.E3Legend import E3Legend
    from optparse import OptionParser
    parser = OptionParser()
    (opts, args) = parser.parse_args()
    h1, h2, hratio = e3eastwest(args[0])
    c1 = E3Canvas('c1')
    h1.Draw()
    h2.Draw('same')
    l = E3Legend(entries = [h1, h2])
    l.Draw()
    c1.Update()
    c2 = E3Canvas('c2')
    hratio.Draw()
    c2.Update()
