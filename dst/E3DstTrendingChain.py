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
from e3pipe.config.__dst__ import MAX_GOOD_CHISQUARE



class E3DstTrendingChain(E3Chain, E3TreePlotter):

    """ Small wrapper around the TChain class specialized for the
    Trending DST tree.
    """

    TREE_NAME = 'Trending'
    ALIAS_DICT = {'BinCenter': '0.5*(BinStart + BinEnd)'}

    def __init__(self, *fileList):
        """ Constructor.
        """
        E3Chain.__init__(self, self.TREE_NAME, *fileList)
        E3TreePlotter.__init__(self)

    def binCenter(self):
        """ Return the center of the time bin for the current entry.
        """
        return self.formulaValue('BinCenter')

    def doSummaryPlots(self):
        """ Create the summary plots.
        """
        _ytitle = 'Rate of non-GPS events [Hz]'
        self.stripChart('RateNonGpsEvents', ytitle = _ytitle)
        _ytitle = 'Rate of tracks with #chi^{2} < %.1f [Hz]' %\
                  MAX_GOOD_CHISQUARE
        self.stripChart('RateTrackEvents', ytitle = _ytitle)
        _ytitle = 'Fraction of tracks with #chi^{2} < %.1f' %\
                  MAX_GOOD_CHISQUARE
        self.stripChart('FractionTrackEvents', ytitle = _ytitle)



def test(*fileList):
    """ Test program.
    """
    t = E3DstTrendingChain(*fileList)
    t.setupArrays()
    t.setupTreeFormulae()
    t.doSummaryPlots()
    return t.plots()
    



if __name__ == '__main__':
    from e3pipe.root.E3Canvas import E3Canvas
    from optparse import OptionParser
    parser = OptionParser()
    (opts, args) = parser.parse_args()
    for i, g in enumerate(test(*args)):
        c = E3Canvas('c%d' % i)
        g.Draw('al')
        c.Update()
    
