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


from e3pipe.db.E3RunDbInterface import E3RunDbInterface
from e3pipe.tasks.__exitcodes__ import *
from e3pipe.config.__storage__ import binFilePath
from e3pipe.__logging__ import logger

import os




def e3failureStats(exitCode):
    """
    """
    db = E3RunDbInterface()
    query = 'SELECT station_name, run_date, run_id from runs WHERE processing_status_code = %d' % exitCode
    db.execute(query, commit = False)
    outputFilePath = 'failures_%d.dat' % exitCode
    logger.info('Opening output file %s...' % outputFilePath)
    outputFile = open(outputFilePath, 'w')
    n = 0
    for station, date, runId in db.fetchall():
        filePath = binFilePath(station, date, runId)
        if os.path.exists(filePath):
            outputFile.write('%s\t%d\n' %\
                                 (filePath, os.stat(filePath).st_size))
            n += 1
        else:
            logger.error('Could not find %s!' % filePath)
    outputFile.close()
    logger.info('Done, %d rows written.' % n)
    db.close()



if __name__ == '__main__':
    e3failureStats(E3PIPE_EXIT_CODE_ANALYZER_SEGFAULT)
    e3failureStats(E3PIPE_EXIT_CODE_ANALYZER_KILLED)
    e3failureStats(E3PIPE_EXIT_CODE_NO_HITS_EVENTS)
