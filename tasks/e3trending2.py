#!/usr/bin/env python
# *********************************************************************
# * Copyright (C) 2015 Luca Baldini (luca.baldini@pi.infn.it)         *
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
import sys
import ROOT
import datetime
import e3pipe.__utils__ as __utils__

from e3pipe.__logging__ import logger, startmsg, abort
#from e3pipe.dst.E3BinFile import E3BinFile
from e3pipe.dst.E3DstEventTree import E3DstEventTree
from e3pipe.dst.E3DstHeaderTree import E3DstHeaderTree
from e3pipe.dst.E3DstWeatherTree import E3DstWeatherTree
from e3pipe.dst.__runid__ import uniqueRunIdFromFilePath
from e3pipe.root.E3OutputRootFile import E3OutputRootFile
from e3pipe.misc.E3Chrono import E3Chrono
from e3pipe.config.__storage__ import listTemp, splitFilePath
from e3pipe.config.__dqm__ import TRENDING_TIME_BIN
from e3pipe.config.__dst__ import MAX_RUN_DURATION
from e3pipe.dst.__time__ import date2str



def e3trending2(dstFilePath):
    """ Parse a DST root file produced by the new analyzer and add the bits that
    are missing for the DQM (e.g., the trending).
    """
    chrono = E3Chrono()
    #uniqueId = uniqueRunIdFromFilePath(baseFilePath)
    #station, year, month, day, runId = splitFilePath(baseFilePath)
    #date = datetime.date(int(year), int(month), int(day))
    #logger.info('Unique run ID is %s.' % uniqueId)
    logger.info('Opening output ROOT file %s...' % dstFilePath)
    rootFile = E3OutputRootFile(dstFilePath, 'e3dst', date2str(date), station)
    logger.info('Initializing event tree...')
    eventTree = E3DstEventTree()
    #eventTree.setUniqueRunId(uniqueId)
    #logger.info('Filling event tree...')
    #for row in outFile:
    #    eventTree.fillRow(row)
    #eventStat = outFile.eventStat()
    #tmin = outFile.minTimestamp()
    #tmax = outFile.maxTimestamp()
    # If we have less than two good events there is nothing we could
    # possibly do, here.
    # Close all files and remove the output dst ROOT file so that
    # we know the run has not been processed.
    #if eventStat['hits'] < 2:
    #    logger.info('Closing all files...')
    #    rootFile.Close()
    #    outFile.close()
    #    sumFile.close()
    #    __utils__.rm(dstFilePath)
    #    logger.info('No events with hits, processing terminated after %.3f s.' %\
    #                chrono.stop())
    #    sys.exit(E3PIPE_EXIT_CODE_NO_HITS_EVENTS)
    #logger.info('Event stats: %s' % eventStat)
    #logger.info('Range of timestamps in the output files: %.3f--%.3f' %\
    #            (tmin, tmax))
    #duration = tmax - tmin
    #logger.info('Corresponding run duration: %.3f s' % duration)
    #if duration > MAX_RUN_DURATION:
    #    logger.error('Run looks way too long, something must be wrong.')
    #    sys.exit(E3PIPE_EXIT_CODE_RUN_TOO_LONG)
    #eventTree.Write()
    logger.info('Done, %d event(s) filled in.' % eventTree.GetEntries())
    if eventTree.GetEntries() == 0:
        abort('No events found (maybe an issue with eee_calib.txt?)')
    logger.info('Creating monitoring plots...')
    #eventTree.doMonitoring()
    #logger.info('Initializing weather tree...')
    #weatherTree = E3DstWeatherTree()
    #weatherTree.setUniqueRunId(uniqueId)
    #binFile = E3BinFile('%s.bin' % baseFilePath)
    #weatherRecord = binFile.weatherStationRecord()
    #if weatherRecord is not None:
    #    logger.info('Filling weather tree...')
    #    weatherTree.fillRow(weatherRecord.data())
    #weatherTree.Write()
    #logger.info('Creating trending data products...')
    #trendingTree = eventTree.doTrending(TRENDING_TIME_BIN, tmin, tmax,
    #                                    weatherRecord)
    #logger.info('Writing trending tree...')
    #trendingTree.Write()
    #logger.info('Writing monitoring/trending plots...')
    #for plot in eventTree.plots():
    #    plot.Write()
    #logger.info('Initializing header tree...')
    #headerTree = E3DstHeaderTree()
    #headerTree.setUniqueRunId(uniqueId)
    #logger.info('Filling header tree...')
    #data = sumFile.data()
    # Mind we need to add a few things "by hand", here, as not all the
    # information that we want in the header is really coming from the
    # sum file.
    #data['RunNumber'] = row['RunNumber']
    #data['RunStart'] = tmin
    #data['RunStop'] = tmax
    #data['RunDuration'] = tmax - tmin
    #data['NumHitEvents'] = eventStat['hits']
    #data['NumTrackEvents'] = eventStat['track']
    #data['NumNoHitsEvents'] = eventStat['no_hits']
    #data['NumNoHitEvents'] = eventStat['no_hit']
    #data['NumMalformedEvents'] = eventStat['malformed']
    #data['NumBackwardEvents'] = eventStat['backward']
    #headerTree.fillRow(data)
    #headerTree.Write()
    #logger.info('Creating histograms...')
    #for key in ['HitMultBot', 'HitMultMid', 'HitMultTop',
    #            'ClusterMultBot', 'ClusterMultMid', 'ClusterMultTop']:
    #    h = data2hist(data, key, xmax = 15.5)
    #    h.Write()
    #for key in ['HitMultTotal', 'ClusterMultTotal']:
    #    h = data2hist(data, key, xmax = 35.5)
    #    h.Write()
    #logger.info('Closing all files...')
    #rootFile.Close()
    #outFile.close()
    #sumFile.close()
    logger.info('DST created in %.3f s.' % chrono.stop())
    listTemp()
    logger.info('Returning DST path: %s...' % dstFilePath)
    return dstFilePath



if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser()
    (opts, args) = parser.parse_args()
    for arg in args:
        e3trending2(arg)
