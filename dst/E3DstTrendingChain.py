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



class E3DstTrendingChain(E3Chain):

    """ Small wrapper around the TChain class specialized for the
    Trending DST tree.
    """

    TREE_NAME = 'Trending'
    ALIAS_DICT = {'BinCenter': '0.5*(BinStart + BinEnd)'}

    def __init__(self, *fileList):
        """ Constructor.
        """
        E3Chain.__init__(self, self.TREE_NAME, *fileList)

    def binCenter(self):
        """ Return the center of the time bin for the current entry.
        """
        return self.formulaValue('BinCenter')

    def stripChart(self, branchName, errors = False, ytitle = None,
                   **kwargs):
        """ Create a strip chart.
        
        TODO: the core of this should be moved to a base class, as presumably
        we'll want to reuse this functionality.
        """
        from e3pipe.root.__ROOT__ import setupTimeDisplay
        from e3pipe.root.E3Graph import E3Graph
        ytitle = ytitle or branchName
        g = E3Graph('g%s' % branchName, ytitle)
        for i in xrange(self.GetEntries()):
            self.GetEntry(i)
            x = self.binCenter()
            y = self.arrayValue(branchName)
            if errors:
                dy = self.arrayValue('%sErr' % branchName)
            else:
                dy = 0
            g.SetNextPoint(x, y, dy)
        setupTimeDisplay(g)
        g.GetYaxis().SetTitle(ytitle)
        return g



def test(*fileList):
    """ Test program.
    """
    t = E3DstTrendingChain(*fileList)
    t.setupArrays()
    t.setupTreeFormulae()
    g = t.stripChart('RateTrackEvents')
    return g
    



if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser()
    (opts, args) = parser.parse_args()
    g = test(*args)
    from e3pipe.root.E3Canvas import E3Canvas
    c = E3Canvas('c')
    g.Draw('alp')
    c.Update()
    
