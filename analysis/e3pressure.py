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


_usage = 'usage: %prog [options] filePath'
_synopsis = 'Calculate the pressure correction to the event rate'

# Set up the command-line switches.
from e3pipe.misc.E3OptionParser import E3OptionParser

parser = E3OptionParser(_usage, _synopsis)
parser.add_option('-o', '--output-folder', type = str, default = None,
                  dest = 'output_folder',
                  help = 'the output folder for the DQM products')
parser.add_option('-m', '--min-rate', type = float, default = 0.,
                  dest = 'min_rate',
                  help = 'the minimum event rate for the analysis')
parser.add_option('-M', '--max-rate', type = float, default = 100.,
                  dest = 'max_rate',
                  help = 'the maximum event rate for the analysis')
parser.add_option('-i', '--interactive', action = 'store_true',
                  default = False, dest = 'interactive',
                  help = 'run interactively (show the plots)')
(opts, args) = parser.parse_args()

# Make sure we are passing some argument.
if len(args) != 1:
    parser.print_help()
    parser.error('Please provide a single input file.')

filePath = args[0]

STD_PRESSURE = 1013.25
RATE_EXPR = 'RateTrackEvents'
RATE_ERR_EXPR = '%sErr' % RATE_EXPR


import os

from e3pipe.root.__ROOT__ import *
from e3pipe.root.E3Canvas import E3Canvas
from e3pipe.root.E3H1D import E3H1D
from e3pipe.root.E3H2D import E3H2D
from e3pipe.dst.E3DstHeaderChain import E3DstHeaderChain
from e3pipe.dst.E3DstTrendingChain import E3DstTrendingChain
from e3pipe.dst.E3DstWeatherChain import E3DstWeatherChain


trendingChain = E3DstTrendingChain(filePath)
trendingChain.setupArrays()
trendingChain.setupTreeFormulae()
weatherChain = E3DstWeatherChain(filePath)
station = os.path.basename(filePath)[:7]

logger.info('Peeking at input data....')
minRate = trendingChain.GetMinimum(RATE_EXPR)
maxRate = trendingChain.GetMaximum(RATE_EXPR)
logger.info('Rate: %.3f--%.3f Hz' % (minRate, maxRate))
minPres = weatherChain.GetMinimum('Pressure')
maxPres = weatherChain.GetMaximum('Pressure')
logger.info('Pressure: %d--%d hPa' % (minPres, maxPres))

rmin = max(minRate - 0.1*(maxRate - minRate), opts.min_rate)
rmax = min(maxRate + 0.1*(maxRate - minRate), opts.max_rate)
rbins = 100
pmin = minPres - 0.5
pmax = maxPres + 0.5
pbins = int(maxPres - minPres + 1.5)


c1 = E3Canvas('%s_raw_rate' % station)
h1 = E3H1D('hrawrate', 'Raw rate', rbins, rmin, rmax,
           XTitle = 'Raw rate of tracks [Hz]')
trendingChain.Project(h1.GetName(), RATE_EXPR)
h1.Draw()
c1.annotate(0.1, 0.94, station)
c1.Update()
if opts.output_folder:
    c1.save(opts.output_folder)


c2 = E3Canvas('%s_raw_rate_vs_pres' % station, RightMargin = 0.16)
h2 = E3H2D('hrawratepres', 'Raw rate vs. pressure', pbins, pmin, pmax,
           rbins, rmin, rmax, XTitle = 'Pressure [hPa]',
           YTitle = 'Raw rate of tracks [Hz]', Stats = False)
for i in xrange(trendingChain.GetEntries()):
    trendingChain.GetEntry(i)
    t = trendingChain.stripChartTime()
    p = weatherChain.interpolatePressure(t)
    r = trendingChain.arrayValue(RATE_EXPR)
    h2.Fill(p, r)
h2.Draw('colz')
prof = h2.ProfileX()
prof.SetLineColor(ROOT.kWhite)
prof.SetMarkerStyle(20)
prof.SetMarkerColor(ROOT.kWhite)
prof.Draw('same')
func = ROOT.TF1('line', '[0] + [1]*(x - %f)' % STD_PRESSURE, pmin, pmax)
func.SetLineColor(ROOT.kRed)
prof.Fit(func, 'N')
func.Draw('same')
c2.annotate(0.1, 0.94, station)
c2.annotate(0.4, 0.85, 'p0 = %.2f Hz @ %.2f hPa' %\
            (func.GetParameter(0), STD_PRESSURE))
slope = func.GetParameter(1)/func.GetParameter(0)*100.
c2.annotate(0.4, 0.80, 'p1 = %.2f %% per hPa' % slope)
m = ROOT.TMarker(STD_PRESSURE, func.Eval(STD_PRESSURE), 20)
m.SetMarkerColor(ROOT.kRed)
m.SetMarkerSize(2)
m.Draw()
c2.Update()
if opts.output_folder:
    c2.save(opts.output_folder)


c3 = E3Canvas('%s_corr_rate' % station)
h3 = E3H1D('hcorrrate', 'Corrected rate', rbins, rmin, rmax,
           XTitle = 'Corrected rate of tracks [Hz]')
h4 = E3H1D('hpull', 'Pulls', rbins, -5, 5,
           XTitle = 'Pulls')
graw = ROOT.TGraph()
graw.SetLineColor(ROOT.kRed)
gcor = ROOT.TGraph()
gcor.SetLineColor(ROOT.kBlue)
r0 = func.Eval(STD_PRESSURE)
for i in xrange(trendingChain.GetEntries()):
    trendingChain.GetEntry(i)
    t = trendingChain.stripChartTime()
    p = weatherChain.interpolatePressure(t)
    r = trendingChain.arrayValue(RATE_EXPR)
    rerr = trendingChain.arrayValue(RATE_ERR_EXPR)
    corr = r0/func.Eval(p)
    rcor = r*corr
    rerrcor = rerr*corr
    h3.Fill(rcor)
    h4.Fill((rcor - r0)/rerrcor)
    graw.SetPoint(i, t, r)
    gcor.SetPoint(i, t, rcor)
h3.Draw()
c3.annotate(0.1, 0.94, station)
exp = (func.Eval(STD_PRESSURE)/60)**0.5
c3.annotate(0.65, 0.6, 'Exp. RMS = %.3f' % exp)
c3.Update()
if opts.output_folder:
    c3.save(opts.output_folder)


c4 = E3Canvas('%s_pulls' % station, Logy = True)
h4.Draw()
fgaus = ROOT.TF1('fgaus', 'gaus')
fgaus.SetLineColor(ROOT.kRed)
h4.Fit('fgaus')
c4.annotate(0.1, 0.94, station)
c4.annotate(0.5, 0.5, '#mu = %.3f' % fgaus.GetParameter(1))
c4.annotate(0.5, 0.45, '#sigma = %.3f' % fgaus.GetParameter(2))
c4.Update()
if opts.output_folder:
    c4.save(opts.output_folder)


#c5 = E3Canvas('%s_stripchart' % station)
#graw.Draw('al')
#gcor.Draw('lsame')
#c5.annotate(0.1, 0.94, station)
#c5.Update()


if opts.interactive:
    os.environ['PYTHONINSPECT'] = 'True'
