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



class E3DstHeaderChain(E3Chain, E3TreePlotter):

    """ Small wrapper around the TChain class specialized for the
    Trending DST tree.
    """

    TREE_NAME = 'Header'
    ALIAS_DICT = {'RunCenter': '0.5*(RunStart + RunStop)',
                  'AverageRate': 'NumEvents/RunDuration'}

    def __init__(self, *fileList):
        """ Constructor.
        """
        E3Chain.__init__(self, self.TREE_NAME, *fileList)
        E3TreePlotter.__init__(self)
        
    def stripChartTime(self):
        """ Return the center of the time bin for the current entry.
        """
        return self.formulaValue('RunCenter')

    def doSummaryPlots(self, xpad = 0.05):
        """ Create a set of summary plots.
        """
        self.hist1d('RunDuration', xpad = xpad,
                    XTitle = 'Run duration [s]')
        self.hist1d('NumEvents', xpad = xpad,
                    XTitle = 'Total number of events', Ndivisions = 508)
        self.stripChart('AverageRate', YTitle = 'Average rate of events [Hz]')
        self.hist1d('NumTrackEvents', xpad = xpad,
                    XTitle = 'Number of events with tracks', Ndivisions = 508)
        self.hist1d('NumMalformedEvents', xpad = xpad,
                    XTitle = 'Number of malformed events')
        self.hist1d('NumBackwardEvents', xpad = xpad,
                    XTitle = 'Number of non-time-ordered events')
        self.hist1d('NumNoHitsEvents', xpad = xpad,
                    XTitle = 'Number of "no hits" events')
        self.hist1d('NumNoHitEvents', xpad = xpad,
                    XTitle = 'Number of "no hit" events')



def test(*fileList):
    """ Test program.
    """
    t = E3DstHeaderChain(*fileList)
    t.doSummaryPlots()
    return t.plots()



if __name__ == '__main__':
    from e3pipe.root.E3Canvas import E3Canvas
    from optparse import OptionParser
    parser = OptionParser()
    (opts, args) = parser.parse_args()
    for i, h in enumerate(test(*args)):
        c = E3Canvas('c%d' % i)
        h.Draw()
        c.Update()
