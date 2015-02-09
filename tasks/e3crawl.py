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
from e3pipe.config.__stations__ import E3_ACTIVE_STATIONS
from e3pipe.__logging__ import logger, abort, E3FileHandler
from e3pipe.misc.E3Chrono import E3Chrono
from e3pipe.config.__storage__ import E3PIPE_LOG_BASE, E3RawDataInfo
from e3pipe.dst.__time__ import date2str
from e3pipe.tasks.__exitcodes__ import lockFileMessage
from e3pipe.db.e3registerRun import e3registerRun
from e3pipe.db.E3RunDbInterface import E3RunDbInterface



def e3crawl(endDate = None, daysSpanned = 2, minSize = 0,
            blackList = [], overwrite = False, maxNumRuns = None,
            dryRun = False, register = False):
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
        chrono = E3Chrono()
        _cmd = 'e3recon.py %s' % filePath
        exitCode = __utils__.cmd(_cmd)
        if exitCode:
            runInfo = E3RawDataInfo(filePath)
            lockFilePath = runInfo.LockFilePath
            __utils__.createFolder(os.path.dirname(lockFilePath))
            logger.info('Writing lock file %s...' % lockFilePath)
            msg = lockFileMessage(exitCode, logFilePath)
            open(lockFilePath, 'w').write(msg)
            logger.info('Done.')
            logger.error('Processing terminated after %.3f s.' % chrono.stop())
        else:
            logger.info('Run processed in %.3f s.' % chrono.stop())
        if register:
            db = E3RunDbInterface()
            e3registerRun(filePath, db)
            db.close()
        if maxNumRuns is not None and curFile >= maxNumRuns:
            break
        curFile += 1
    logFileHandler.close()

