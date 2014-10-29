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
from e3pipe.dst.E3Timestamp import E3Timestamp
from e3pipe.misc.E3Chrono import E3Chrono



class E3DumbTimestamp:

    def __init__(self, timestamp, station):
        """
        """
        self.Timestamp = timestamp
        self.Station = station

    def __cmp__(self, other):
        """
        """
        if self.Timestamp > other.Timestamp:
            return 1
        else:
            return -1

    def __sub__(self, other):
        """
        """
        return self.Timestamp - other.Timestamp
        


def e3coincidences(*fileList, **kwargs):
    """ Search for coincidences in a series of data stream.
    """
    tlist = []
    logger.info('Populating timestamp list')
    for i, filePath in enumerate(fileList):
        logger.info('Processing file %s...' % filePath)
        chrono = E3Chrono()
        chain = E3DstEventChain(filePath)
        chain.SetBranchStatus('*', 0)
        chain.SetBranchStatus('Seconds', 1)
        chain.SetBranchStatus('Nanoseconds', 1)
        chain.SetBranchStatus('StatusCode', 1)
        chain.setupArrays()
        chain.setupTreeFormulae()
        for i in xrange(chain.GetEntries()):
            chain.GetEntry(i)
            if chain.arrayValue('StatusCode') == 0:
                #t = E3Timestamp(chain.arrayValue('Seconds'),
                #                chain.arrayValue('Nanoseconds'))
                tlist.append(E3DumbTimestamp(i,
                                             chain.formulaValue('Timestamp')))
        logger.info('File processed in %.3f s.' % chrono.stop())
    logger.info('Done.')
    logger.info('Sorting timestamp list...')
    chrono = E3Chrono()
    tlist.sort()
    logger.info('List sorted in %.3f s.' % chrono.stop())
    logger.info('Filling histogram...')
    chrono = E3Chrono()
    h = ROOT.TH1F('h', 'h', 200, -10000, 10000)
    for i in xrange(1, len(tlist)):
        delta = 1e9*(tlist[i] - tlist[i-1])
        if tlist[i].Station > tlist[i-1].Station:
            delta *= -1.
        h.Fill(delta)
    logger.info('Histogram filled in %.3f s.' % chrono.stop())
    logger.info('Done.')
    return h



if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser()
    (opts, args) = parser.parse_args()
    h = e3coincidences(*args)
    h.Draw()
