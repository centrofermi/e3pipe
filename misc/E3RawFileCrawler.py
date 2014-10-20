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


import glob
import os


from e3pipe.misc.E3FileCrawlerBase import E3FileCrawlerBase
from e3pipe.config.__storage__ import E3PIPE_RAW_BASE
from e3pipe.config.__storage__ import date2str
from e3pipe.__logging__ import logger



class E3RawFileCrawler(E3FileCrawlerBase):

    """ Overloaded crawler class for the raw data.
    """
    
    ROOT_FOLDER = E3PIPE_RAW_BASE

    def __init__(self, stations = None, endDate = None, daysSpanned = 2,
                 minHoursSinceSynch = 2., overwrite = False):
        """ Constructor.
        """
        E3FileCrawlerBase.__init__(self, stations, endDate, daysSpanned)
        self.__MinHoursSinceSynch = minHoursSinceSynch
        self.__Overwrite = overwrite

    def folderPath(self, station, date):
        """ Overloaded class method.
        """
        return os.path.join(self.ROOT_FOLDER, station, 'data', date2str(date))

    def crawlFolder(self, folderPath):
        """  Overloaded class method.
        """
        runList = []
        numNew = 0
        numProcessed = 0
        numReady = 0
        for filePath in glob.glob(os.path.join(folderPath, '*.bin')):
            runInfo = E3RawDataInfo(filePath)
            _new = runInfo.hoursSinceSynch() < self.__MinHoursSinceSynch
            _processed = runInfo.processed()
            if _new:
                numNew += 1
            elif _processed:
                numProcessed += 1
            else:
                numReady += 1
            if (not _processed() or self.__Overwrite) and not new:
                runList.append(runInfo)
        logger.info('%d file(s) ready, %d processed, %d new.' %\
                    (numReady, numProcessed, numNew))
        return runList


    
def test():
    """ Test program.
    """
    crawler = E3RawFileCrawler()
    print crawler


if __name__ == '__main__':
    test()
