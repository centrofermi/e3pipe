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


import os

from e3pipe.root.__ROOT__ import *
from e3pipe.root.E3Canvas import E3Canvas
from e3pipe.root.E3H1D import E3H1D
from e3pipe.root.E3H2D import E3H2D
from e3pipe.dst.E3DstHeaderChain import E3DstHeaderChain
from e3pipe.dst.E3DstTrendingChain import E3DstTrendingChain
from e3pipe.dst.E3DstWeatherChain import E3DstWeatherChain


STATION = 'SAVO-02'
RATE_EXPR = 'RateTrackEvents'
MIN_RATE = 20.
MAX_RATE = 50.
FOLDER_PATH = '/data/work/EEE/data/trending/'

fileName = '%s-2014-10-27-2014-11-09-trending-merged.root' % STATION
filePath = os.path.join(FOLDER_PATH, fileName)

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

rmin = max(minRate - 0.1*(maxRate - minRate), MIN_RATE)
rmax = min(maxRate + 0.1*(maxRate - minRate), MAX_RATE)
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
func = ROOT.TF1('line', '[0] + [1]*(x - 1013.25)', pmin, pmax)
func.SetLineColor(ROOT.kRed)
prof.Fit(func, 'N')
func.Draw('same')
c2.annotate(0.1, 0.94, station)
c2.annotate(0.5, 0.8, 'p0 = %.2f Hz' % func.GetParameter(0))
c2.annotate(0.5, 0.75, 'p1 = %.3f Hz/hPa' % func.GetParameter(1))
c2.Update()


c3 = E3Canvas('%s_corr_rate' % station)
h3 = E3H1D('hcorrrate', 'Corrected rate', rbins, rmin, rmax,
           XTitle = 'Corrected rate of tracks [Hz]')
for i in xrange(trendingChain.GetEntries()):
    trendingChain.GetEntry(i)
    t = trendingChain.stripChartTime()
    p = weatherChain.interpolatePressure(t)
    r = trendingChain.arrayValue(RATE_EXPR)
    corr = func.Eval(1013.25)/func.Eval(p)
    h3.Fill(r*corr)
h3.Draw()
c3.annotate(0.1, 0.94, station)
exp = (func.Eval(1013.25)/60)**0.5
c3.annotate(0.65, 0.6, 'Exp. RMS = %.3f' % exp)
c3.Update()
