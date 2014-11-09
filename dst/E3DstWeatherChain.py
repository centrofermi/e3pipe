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
import ROOT

from e3pipe.__logging__ import logger, abort
from e3pipe.root.E3Chain import E3Chain
from e3pipe.root.E3TreePlotter import E3TreePlotter



class E3DstWeatherChain(E3Chain, E3TreePlotter):

    """ Small wrapper around the TChain class specialized for the
    Weather DST tree.
    """

    TREE_NAME = 'Weather'
    ALIAS_DICT = {}

    def __init__(self, *fileList):
        """ Constructor.
        """
        E3Chain.__init__(self, self.TREE_NAME, *fileList)
        E3TreePlotter.__init__(self)
        self.__fillGraphs()

    def __fillGraphs(self):
        """ Setup the internal TGraph objects to perform the linear 
        interpolation of the environmental quantities.
        """
        self.setupArrays()
        logger.info('Setting up graphs for environmental quantities...')
        self.__IndoorTemperature = ROOT.TGraph()
        self.__OutdoorTemperature = ROOT.TGraph()
        self.__Pressure = ROOT.TGraph()
        for i in xrange(self.GetEntries()):
            self.GetEntry(i)
            t = self.arrayValue('Seconds')
            Tin = self.arrayValue('IndoorTemperature')
            Tout = self.arrayValue('OutdoorTemperature')
            p = self.arrayValue('Pressure')
            self.__IndoorTemperature.SetPoint(i, t, Tin)
            self.__OutdoorTemperature.SetPoint(i, t, Tout)
            self.__Pressure.SetPoint(i, t, p)
        logger.info('Done.')

    def indoorTemperature(self):
        """ Return the underlying TGraph for the indoor temperature.
        """
        return self.__IndoorTemperature

    def interpolateIndoorTemperature(self, t):
        """ Interpolate the indoor temperature at a given time.
        """
        return self.__IndoorTemperature.Eval(t)

    def outdoorTemperature(self):
        """ Return the underlying TGraph for the outdoor temperature.
        """
        return self.__OutdoorTemperature

    def interpolateOutdoorTemperature(self, t):
        """ Interpolate the outdoor temperature at a given time.
        """
        return self.__OutdoorTemperature.Eval(t)

    def pressure(self):
        """ Return the underlying TGraph for the indoor pressure.
        """
        return self.__Pressure

    def interpolatePressure(self, t):
        """ Interpolate the pressure at a given time.
        """
        return self.__Pressure.Eval(t)

    def stripChartTime(self):
        """ Return the center of the time bin for the current entry.
        """
        return self.arrayValue('Seconds')

    def doSummaryPlots(self):
        """ Create the summary plots.
        """
        pass
  



if __name__ == '__main__':
    from e3pipe.root.E3Canvas import E3Canvas
    from optparse import OptionParser
    parser = OptionParser()
    (opts, args) = parser.parse_args()
    t = E3DstWeatherChain(*args)
    print t.interpolateIndoorTemperature(247e6)
    print t.interpolateOutdoorTemperature(247e6)
    print t.interpolatePressure(247e6)
    glist = [t.indoorTemperature(), t.outdoorTemperature(), t.pressure()]
    for i, g in enumerate(glist):
        c = E3Canvas('c%d' % i)
        g.Draw('al')
        c.Update()
    
