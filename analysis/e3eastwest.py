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


_usage = 'usage: %prog [options] dataFilePath mcFilePath'
_synopsis = 'Macro to search for the east-west effect'

# Set up the command-line switches.
from e3pipe.misc.E3OptionParser import E3OptionParser

parser = E3OptionParser(_usage, _synopsis)
parser.add_option('-o', '--output-dir', type = str, default = None,
                  dest = 'outputDir',
                  help = 'path to the output folder for the plots')
parser.add_option('-i', '--interactive', action = 'store_true',
                  default = False, dest = 'interactive',
                  help = 'run interactively (show the plots)')
(opts, args) = parser.parse_args()

if len(args) != 2:
    parser.error('Please pass the data and MC file paths')

from e3pipe.__logging__ import logger
from e3pipe.root.__ROOT__ import *
from e3pipe.root.E3H1D import E3H1D
from e3pipe.root.E3Canvas import E3Canvas
from e3pipe.dst.E3DstEventChain import E3DstEventChain
from e3pipe.mc.E3McEventChain import E3McEventChain
from e3pipe.root.E3Legend import E3Legend
from e3pipe.config.__storage__ import splitFilePath


THETA_CUT = 'Theta > 0'

dataFilePath, mcFilePath = args
station = splitFilePath(dataFilePath)[0]
dataChain = E3DstEventChain(dataFilePath)
mcChain = E3McEventChain(mcFilePath)

htheta = E3H1D('htheta', 'Theta', 75, 0, 90, Minimum = 0,
               XTitle = '#theta [#circ]')
hphi = E3H1D('hphi', 'Phi', 75, -180, 180, Minimum = 0,
             XTitle = '#phi [#circ]')

hthetadata = htheta.Clone('hthetadata')
hthetadata.SetLineColor(ROOT.kRed)
hthetadata.SetTitle('Data')
hphidata = hphi.Clone('hphidata')
hphidata.SetTitle('Data')
hphidata.SetLineColor(ROOT.kRed)
dataCut = '%s && StatusCode == 0 && ChiSquare < 10' % THETA_CUT
dataChain.Project('hthetadata', 'Theta', dataCut)
dataChain.Project('hphidata', 'Phi', dataCut)
hthetadata.Scale(1./hthetadata.GetSumOfWeights())
hphidata.Scale(1./hphidata.GetSumOfWeights())
hthetadata.SetMinimum(0)
hphidata.SetMinimum(0)


hthetamc = htheta.Clone('hthetamc')
hthetamc.SetTitle('Monte Carlo')
hthetamc.SetLineColor(ROOT.kBlue)
hphimc = hphi.Clone('hphimc')
hphimc.SetTitle('Monte Carlo')
hphimc.SetLineColor(ROOT.kBlue)
mcCut = '%s && Trigger == 1' % THETA_CUT
mcChain.Project('hthetamc', 'Theta', mcCut)
mcChain.Project('hphimc', 'Phi', mcCut)
hthetamc.Scale(1./hthetamc.GetSumOfWeights())
hphimc.Scale(1./hphimc.GetSumOfWeights())
hthetamc.SetMinimum(0)
hphimc.SetMinimum(0)

c1 = E3Canvas('%s_theta_datamc' % station)
hthetadata.Draw()
hthetamc.Draw('same')
l1 = E3Legend(0.6, 0.6, entries = [hthetadata, hthetamc])
l1.Draw()
c1.annotate(0.1, 0.94, station)
c1.Update()
if opts.outputDir is not None:
    c1.save(opts.outputDir)


c2 = E3Canvas('%s_phi_datamc' % station)
hphidata.Draw()
hphimc.Draw('same')
l2 = E3Legend(0.4, 0.8, entries = [hphidata, hphimc])
l2.Draw()
c2.annotate(0.1, 0.94, station)
c2.Update()
if opts.outputDir is not None:
    c2.save(opts.outputDir)


c3 = E3Canvas('%s_phi_modulation' % station)
hphiratio = hphidata.Clone('hphiratio')
hphiratio.Divide(hphimc)
hphiratio.SetLineColor(ROOT.kBlack)
hphiratio.SetMinimum(0.75)
hphiratio.SetMaximum(1.25)
hphiratio.SetYTitle('Data/MC ratio')
hphiratio.Draw()

def vline(x):
    y0 = hphiratio.GetMinimum()
    y1 = hphiratio.GetMaximum()
    l = ROOT.TLine(x, y0, x, y1)
    l.SetLineStyle(7)
    l.Draw()
    store(l)

for x in [-135, -45, 45, 135]:
    vline(x)

c3.annotate(0, 0.8, 'North', ndc = False, align = 21)
c3.annotate(90, 0.8, 'East', ndc = False, align = 21)
c3.annotate(-90, 0.8, 'West', ndc = False, align = 21)
c3.annotate(0.1, 0.94, station)
c3.Update()
if opts.outputDir is not None:
    c3.save(opts.outputDir)
