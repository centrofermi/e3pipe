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


import datetime
import glob
import os

from e3pipe.config.__storage__ import E3RawDataInfo, rawDataFolders
from e3pipe.config.__stations__ import STATION_LIST
from e3pipe.__logging__ import logger, abort



class E3RawDataCrawler:

    """ Basic data crawler implementation.
    """

    def __init__(self, stationList = STATION_LIST,
                 endDate = datetime.date.today(), lookBack = 2):
        """ Constructor.
        """
        logger.info('Starting data crawler...')
        self.__RunList = []
        for station in stationList:
            logger.info('Searching for raw data from station %s...' % station)
            folders = rawDataFolders(station, endDate, lookBack)
            for folder in folders:
                if os.path.exists(folder):
                    logger.info('Crawling into %s...' % folder)
                    fileList = glob.glob(os.path.join(folder, '*.bin'))
                    for filePath in fileList:
                        runInfo = E3RawDataInfo(filePath)
                        if not runInfo.processed():
                            self.__RunList.append(runInfo)

    def runList(self):
        """ Return the list of runs.
        """
        return self.__RunList



def test():
    """ Test program.
    """
    crawler = E3RawDataCrawler()
    print crawler.runList()



if __name__ == '__main__':
    test()
