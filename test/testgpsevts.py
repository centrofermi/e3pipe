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

from e3pipe.dst.E3AnalyzerOutFile import E3AnalyzerOutFile
from e3pipe.dst.E3AnalyzerSumFile import E3AnalyzerSumFile
from e3pipe.__logging__ import logger


def test(filePath):
    """ Print out some debug information about the "GPS" events.
    """
    outFile = E3AnalyzerOutFile(filePath)
    numEvents = 0
    numEmptyEvents = 0
    emptyEventsMult = {}
    isolatedEmptyEvents = []
    _acc = 0
    for event in outFile:
        numEvents += 1
        if event['ChiSquare'] < 0:
            _acc += 1
            numEmptyEvents += 1
        else:
            if _acc > 0:
                if _acc == 1:
                    isolatedEmptyEvents.append(event['EventNumber'] - 1)
                try:
                    emptyEventsMult[_acc] += 1
                except KeyError:
                    emptyEventsMult[_acc] = 1
            _acc = 0
    logger.info('Number of events: %d' % numEvents)
    logger.info('Number of empty events: %d' % numEmptyEvents)
    logger.info('Empty event multiplicity: %s' % emptyEventsMult)
    multSum = 0
    for key, value in emptyEventsMult.items():
        multSum += key*value
    logger.info('Sum of multiplicities (for cross check): %d' % multSum)
    logger.info('Isolated empy events: %s' % isolatedEmptyEvents)
    sumFilePath = filePath.replace('.out', '.sum')
    if os.path.exists(sumFilePath):
        sumFile = E3AnalyzerSumFile(sumFilePath)
        logger.info('Number of events according to the sum file: %d' %\
                    sumFile.get('NumEvents'))
        logger.info('Number of GPS events according to the sum file: %d' %\
                    sumFile.get('NumGpsEvents'))
            
    

if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser()
    (opts, args) = parser.parse_args()
    for arg in args:
        test(arg)
