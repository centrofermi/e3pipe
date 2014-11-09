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


filePath = '/data/work/EEE/data/SAVO-02-2014-10-27-2014-11-06-merged.root'

inputFile = ROOT.TFile(filePath)
weatherTree = inputFile.Get('Weather')
pressure = ROOT.TGraph()
for i in xrange(weatherTree.GetEntries()):
    weatherTree.GetEntry(i)
    pressure.SetPoint(i, weatherTree.Seconds, weatherTree.Pressure)
#pressure.Draw('alp')

headerTree = inputFile.Get('Header')
scatter = ROOT.TGraph()
for i in xrange(headerTree.GetEntries()):
    headerTree.GetEntry(i)
    t = 0.5*(headerTree.RunStart + headerTree.RunStop)
    p = pressure.Eval(t)
    r = headerTree.NumEvents/headerTree.RunDuration
    scatter.SetPoint(i, p, r)
scatter.Draw('ap')



