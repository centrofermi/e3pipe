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


class E3EventChain(E3Chain):

    """ Small wrapper around the TChain class.
    """

    TREE_NAME = 'Events'
    ALIAS_DICT = {'Timestamp': 'Seconds + 1.0e-9*Nanoseconds'}

    def __init__(self, filePath):
        """ Constructor.
        """
        E3Chain.__init__(self, filePath, self.TREE_NAME)
        self.StartTime = self.value('Timestamp', 0)
        self.StopTime = self.value('Timestamp', self.GetEntries() - 1)
        self.Duration = self.StopTime - self.StartTime
        logger.info('Time range: %.3f--%.3f (%.3f) s' %\
                    (self.StartTime, self.StopTime, self.Duration))



def test(filePath):
    """ Test program.
    """
    t = E3EventChain(filePath)
    h = t.trendingHist('Seconds > 0')
    return h



if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser()
    (opts, args) = parser.parse_args()
    for filePath in args:
        h = test(filePath)
        h.Draw()
