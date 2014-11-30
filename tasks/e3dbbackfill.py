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

from e3pipe.misc.E3RawFileCrawler import E3RawFileCrawler
from e3pipe.__logging__ import logger
from e3pipe.db.e3registerRun import e3registerRun
from e3pipe.db.E3RunDbInterface import E3RunDbInterface



class E3RawFileCrawlerSimple(E3RawFileCrawler):

    """
    """

    def __init__(self, stations = None, endDate = None, daysSpanned = 2,):
        """ Constructor.
        """
        E3RawFileCrawler.__init__(self, stations, endDate, daysSpanned)

    def crawlFolder(self, folderPath):
        """  Overloaded class method.
        """
        fileList = glob.glob(os.path.join(folderPath, '*.bin'))
        fileList.sort()
        return fileList


def e3dbbackfill(stations = None, endDate = None, daysSpanned = 2,
                 maxNumRuns = None):
    """ Crawl the raw data and process the files.
    """
    crawler = E3RawFileCrawlerSimple(stations, endDate, daysSpanned)
    logger.info(crawler)
    numFiles = maxNumRuns or len(crawler)
    curFile = 1
    db = E3RunDbInterface()
    for filePath in crawler:
        logger.info('Registering file %d/%d: %s' %\
                    (curFile, numFiles, filePath))
        e3registerRun(filePath, db)
        if maxNumRuns is not None and curFile >= maxNumRuns:
            break
        curFile += 1
    db.close()


