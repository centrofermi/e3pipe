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

from e3pipe.db.E3RunDbFileCrawlerBase import E3RunDbFileCrawlerBase
from e3pipe.config.__storage__ import binFilePath
from e3pipe.db.__select__ import selectRunsToBeProcessed



class E3RunDbRawFileCrawler(E3RunDbFileCrawlerBase):
    
    """ db-based crawler for the binary files.
    """

    def __init__(self, endDate = None, daysSpanned = 2, minSize = 0,
                 blackList = None, overwrite = False):
        """
        """
        endDate = endDate or datetime.date.today()
        startDate = endDate - datetime.timedelta(daysSpanned)
        E3RunDbFileCrawlerBase.__init__(self, [], startDate, endDate)
        self.__MinSize = minSize
        self.__BlackList = blackList or []
        runList = selectRunsToBeProcessed(startDate, endDate, minSize,
                                          overwrite)
        for station, date, runId in runList:
            if station not in self.__BlackList:
                filePath = binFilePath(station, date, runId)
                self.addFilePath(station, filePath)


def test():
    """ Test program.
    """
    crawler = E3RunDbRawFileCrawler(daysSpanned = 1, blackList = ['FRAS-03'])
    print crawler
  

  
if __name__ == '__main__':
    test()
