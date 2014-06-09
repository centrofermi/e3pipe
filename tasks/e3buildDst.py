#!/usr/bin/env python
# *********************************************************************
# * Copyright (C) 2014 Luca Baldini (luca.baldini@pi.infn.it)         *
# *                                                                   *
# * For the license terms see the file LICENCE, distributed           *
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
import e3pipe.__utils__

from e3pipe.__logging__ import logger, startmsg, abort
from e3pipe.dst.E3AnalyzerOutFile import E3AnalyzerOutFile
from e3pipe.dst.E3AnalyzerSumFile import E3AnalyzerSumFile
from e3pipe.dst.E3DstEventTree import E3DstEventTree
from e3pipe.dst.E3DstHeaderTree import E3DstHeaderTree


def e3buildDst(baseFilePath):
    """ Parse all the output text files from the analyzer and build the
    actual DST in ROOT format.
    """
    logger.info('Collecting input files for the DST...')
    outFile = E3AnalyzerOutFile('%s.out' % baseFilePath)
    sumFile = E3AnalyzerSumFile('%s.sum' % baseFilePath)
    rootFilePath = '%s_dst.root' % baseFilePath
    logger.info('Opening output ROOT file %s...' % rootFilePath)
    rootFile = ROOT.TFile(rootFilePath, 'RECREATE')
    logger.info('Initializing event tree...')
    eventTree = E3DstEventTree()
    logger.info('Filling event tree...')
    for row in outFile:
        eventTree.fillRow(row)
    eventTree.Write()

    logger.info('Initializing header tree...')
    headerTree = E3DstHeaderTree()
    logger.info('Filling header tree...')
    data = sumFile.data()
    data['RunNumber'] = row['RunNumber']
    headerTree.fillRow(data)
    headerTree.Write()

    logger.info('Closing files...')
    rootFile.Close()
    outFile.close()
    sumFile.close()



if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser()
    (opts, args) = parser.parse_args()
    for arg in args:
        e3buildDst(arg)
