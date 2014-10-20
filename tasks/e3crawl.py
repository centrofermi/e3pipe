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

import e3pipe.__utils__ as __utils__

from e3pipe.misc.E3RawFileCrawler import E3RawFileCrawler
from e3pipe.config.__stations__ import E3_ACTIVE_STATIONS
from e3pipe.__logging__ import logger, abort
from e3pipe.misc.E3Chrono import E3Chrono



def e3crawl(stations = None, endDate = None, daysSpanned = 2,
            minHoursSinceSynch = 2., overwrite = False, dryRun = False):
    """ Crawl the raw data and process the files.
    """
    crawler = E3RawFileCrawler(stations, endDate, daysSpanned,
                               minHoursSinceSynch, overwrite)
    logger.info(crawler)
    if dryRun:
        logger.info('Just kidding, dry run :-)')
        return 
    for filePath in crawler.fileList():
        chrono = E3Chrono()
        _cmd = 'e3recon.py %s' % filePath
        __utils__.cmd(_cmd)
        logger.info('Run processed in %.3f s.' % chrono.stop())


