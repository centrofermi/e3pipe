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
from e3pipe.misc.E3Chrono import E3Chrono


def data2hist(data, key, xmin = -0.5, xmax = 50.5, xbins = 51):
    """
    """
    name = 'h%s' % key
    title = key.replace('Mult', ' multiplicity ')
    logger.info('Filling histogram %s...' % name)
    h = ROOT.TH1I(name, title, xbins, xmin, xmax)
    h.SetXTitle(title)
    content = data[key]
    for value, weight in content.items():
        h.Fill(value, weight)
    return h


def e3dst(baseFilePath):
    """ Parse all the output text files from the analyzer and build the
    actual DST in ROOT format.
    """
    chrono = E3Chrono()
    logger.info('Collecting input files for the DST...')
    outFile = E3AnalyzerOutFile('%s.out' % baseFilePath)
    sumFile = E3AnalyzerSumFile('%s.sum' % baseFilePath)
    dstFilePath = '%s_dst.root' % baseFilePath
    logger.info('Opening output ROOT file %s...' % dstFilePath)
    rootFile = ROOT.TFile(dstFilePath, 'RECREATE')
    logger.info('Initializing event tree...')
    eventTree = E3DstEventTree()
    logger.info('Filling event tree...')
    for row in outFile:
        eventTree.fillRow(row)
    eventTree.Write()
    logger.info('Done, %d event(s) filled in.' % eventTree.GetEntries())
    if eventTree.GetEntries() == 0:
        abort('No events found (maybe an issue with eee_calib.txt?)')
    logger.info('Initializing header tree...')
    headerTree = E3DstHeaderTree()
    logger.info('Filling header tree...')
    data = sumFile.data()
    data['RunNumber'] = row['RunNumber']
    headerTree.fillRow(data)
    headerTree.Write()
    logger.info('Creating histograms...')
    for key in ['HitMultBot', 'HitMultMid', 'HitMultTop', 'HitMultTotal',
                'ClusterMultBot', 'ClusterMultMid', 'ClusterMultTop',
                'ClusterMultTotal']:
        h = data2hist(data, key)
        h.Write()
    logger.info('Closing files...')
    rootFile.Close()
    outFile.close()
    sumFile.close()
    logger.info('DST created in %.3f s.' % chrono.stop())
    return dstFilePath



if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser()
    (opts, args) = parser.parse_args()
    for arg in args:
        e3dst(arg)
