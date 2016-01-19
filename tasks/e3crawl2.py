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
import datetime

import e3pipe.__utils__ as __utils__

from e3pipe.db.E3RunDbRawFileCrawler import E3RunDbRawFileCrawler
from e3pipe.__logging__ import logger, abort, E3FileHandler
from e3pipe.config.__storage__ import E3PIPE_LOG_BASE
from e3pipe.dst.__time__ import date2str


def e3crawl2(endDate = None, daysSpanned = 2, minSize = 0,
            blackList = [], overwrite = False, maxNumRuns = None,
            dryRun = False):
    """ Crawl the raw data and process the files.
    """
    logDate = datetime.datetime.today()
    datestr = date2str(logDate)
    timestr = logDate.strftime('%Y-%m-%d-%H-%M-%S-%f')
    logFilePath = os.path.join(E3PIPE_LOG_BASE, datestr, '%s.log' % timestr)
    logFolder = os.path.dirname(logFilePath)
    __utils__.createFolder(logFolder)
    logFileHandler = E3FileHandler(logFilePath)
    crawler = E3RunDbRawFileCrawler(endDate, daysSpanned, minSize,
                                    blackList, overwrite)
    logger.info(crawler)
    if dryRun:
        logger.info('Just kidding, dry run :-)')
        return
    numFiles = maxNumRuns or len(crawler)
    curFile = 1
    for filePath in crawler:
        logger.info('Processing file %d/%d: %s' % (curFile, numFiles, filePath))
        _cmd = 'e3process2.py %s' % filePath
        exitCode = __utils__.cmd(_cmd)
        if maxNumRuns is not None and curFile >= maxNumRuns:
            break
        curFile += 1
    logFileHandler.close()
