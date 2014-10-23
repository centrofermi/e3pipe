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

from e3pipe.__logging__ import logger, startmsg, abort
from e3pipe.dst.E3DstHeaderChain import E3DstHeaderChain
from e3pipe.dst.E3DstEventChain import E3DstEventChain
from e3pipe.dst.E3DstTrendingChain import E3DstTrendingChain
from e3pipe.root.E3OutputRootFile import E3OutputRootFile
from e3pipe.misc.E3DstFileCrawler import E3DstFileCrawler



def e3mergeFiles(outputFilePath, *fileList, **kwargs):
    """ Merge a series of DST ROOT files.
    """
    if kwargs.get('sort', True):
        logger.info('Sorting file list...')
        fileList = list(fileList)
        fileList.sort()
        logger.info('Done.')
    outputFile = E3OutputRootFile(outputFilePath, 'e3merge')
    if kwargs.get('mergeHeader', True):
        header = E3DstHeaderChain(*fileList)
        header.Write()
    if kwargs.get('mergeEvents', True):
        events = E3DstEventChain(*fileList)
        events.Write()
    if kwargs.get('mergeTrending', True):
        trending = E3DstTrendingChain(*fileList)
        trending.Write()
    outputFile.Close()
    


def e3mergeTimeSpan(outputFilePath, station, endDate = None, daysSpanned = 1,
                    **kwargs):
    """ Merge the DST ROOT files for a given station in a given time
    span.

    Note that we are not offering a sub-daily granularity at this point.
    That might come in the future if needed.
    """
    crawler = E3DstFileCrawler(station, endDate, daysSpanned)
    fileList = crawler.fileList()
    # The crawler return an ordered file list, so no need for an extra sort.
    kwargs['sort'] = False
    e3mergeFiles(outputFilePath, *fileList, **kwargs)



if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser()
    (opts, args) = parser.parse_args()
    e3mergeFiles('testmerge.root', *args, mergeEvents = False, sort = False)
