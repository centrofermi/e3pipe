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
import sys


from e3pipe.__logging__ import logger
from e3pipe.dst.E3DstEventChain import E3DstEventChain
from e3pipe.misc.E3Chrono import E3Chrono
from e3pipe.analysis.E3Event import E3Event



class E3ChainRow:
    
    """ Minimal event structure that we use to sort events in a chain.
    """

    def __init__(self, index, timestamp):
        """ Constructor.
        """
        self.__Index = index
        self.__Timestamp = float(timestamp)

    def index(self):
        """
        """
        return self.__Index

    def timestamp(self):
        """
        """
        return self.__Timestamp

    def __cmp__(self, other):
        """ Comparison operator (for sorting).
        """
        if self.timestamp() > other.timestamp():
            return 1
        elif self.timestamp() < other.timestamp():
            return -1
        else:
            return 0      
    



def e3reduce(*fileList, **kwargs):
    """
    """
    selectionCut = kwargs.get('selectionCut', 'StatusCode == 0')
    outputFilePath = kwargs.get('outputFilePath', None)
    windowWidth = kwargs.get('windowWidth', 3e-6)
    maxEvents = kwargs.get('maxEvents', None)
    eventList = []
    chrono = E3Chrono()
    logger.info('Populating events list...')
    chain = E3DstEventChain(*fileList)
    chain.GetEntry(0)
    chain.setupArrays()
    chain.setupTreeFormulae()
    selectionFormula = ROOT.TTreeFormula('cut', selectionCut, chain)
    numEvents = chain.GetEntries()
    #if maxEvents is not None:
    #    numEvents = min(numEvents, maxEvents)
    for i in xrange(numEvents):
        chain.ResetBranchAddresses()
        chain.GetEntry(i)
        #if selectionFormula.EvalInstance():
        print i
        row = E3ChainRow(i, chain.formulaValue('Timestamp'))
        eventList.append(row)
    logger.info('Input files processed in %.3f s.' % chrono.stop())
    logger.info('Event list ready, %d event(s) in.' % len(eventList))
    #logger.info('Sorting event list...')
    #chrono = E3Chrono()
    #eventList.sort()
    #logger.info('List sorted in %.3f s.' % chrono.stop())
    #for i in xrange(1, len(eventList)):
    #    _evt1 = eventList[i - 1]
    #    _evt2 = eventList[i]
    #    if abs(_evt1.timestamp() - _evt2.timestamp()) <= windowWidth:
    #        _sta1 = _evt1.stationId()
    #        _sta2 = _evt2.stationId()
    #        if _sta1 != _sta2:
    #            if _sta1 > _sta2:
    #                _evt1, _evt2 = _evt2, _evt1
    #            print _evt1
    #            print _evt2
    #            print
        



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
    h = e3reduce(*args, maxEvents = 10000)
    #h.Draw()
