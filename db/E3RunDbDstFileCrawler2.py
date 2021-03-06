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


import datetime

from e3pipe.db.E3RunDbFileCrawlerBase import E3RunDbFileCrawlerBase
from e3pipe.config.__storage2__ import dstFilePath
from e3pipe.db.__select2__ import selectProcessedRuns



class E3RunDbDstFileCrawler2(E3RunDbFileCrawlerBase):
    
    """ db-based crawler for the binary files.
    """

    def __init__(self, station, endDate = None, daysSpanned = 1):
        """
        """
        endDate = endDate or datetime.date.today()
        startDate = endDate - datetime.timedelta(daysSpanned - 1)
        E3RunDbFileCrawlerBase.__init__(self, [station], startDate, endDate)
        selection = 'station_name = "%s"' % station
        runList = selectProcessedRuns(startDate, endDate, selection)
        for station, date, runId in runList:
            filePath = dstFilePath(station, date, runId)
            self.addFilePath(station, filePath)


def test():
    """ Test program.
    """
    crawler = E3RunDbDstFileCrawler2('BOLO-03')
    print crawler
    for filePath in crawler:
        print filePath
  

  
if __name__ == '__main__':
    test()
