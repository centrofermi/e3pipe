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
import time

from e3pipe.db.E3RunDbInterface import E3RunDbInterface
from e3pipe.__logging__ import logger
from e3pipe.config.__storage__ import E3RawDataInfo
from e3pipe.dst.__runid__ import uniqueRunIdFromFilePath
from e3pipe.dst.E3DstHeaderChain import E3DstHeaderChain
from e3pipe.root.E3InputRootFile import E3InputRootFile
from e3pipe.tasks.__exitcodes__ import E3PIPE_EXIT_CODE_SUCCESS,\
    E3PIPE_EXIT_CODE_UNKNOWN



def e3registerSuccess(uniqueId, dstFilePath, db):
    """ Register into the database a run successfully processed.
    """
    dstLastModTime = time.gmtime(os.path.getmtime(dstFilePath))
    dstLastModDatetime = time.strftime('%Y-%m-%d %H:%M:%S', dstLastModTime)
    dstFile = E3InputRootFile(dstFilePath)
    header = dstFile.Get('Header')
    header.GetEntry(0)
    query = 'INSERT INTO run_table (unique_run_id, run_start, run_stop, num_events, num_hit_events, num_track_events, num_no_hit_events, num_no_hits_events, num_malformed_events, num_backward_events, processing_status_code, e3pipe_version, last_processing, last_update) VALUES(%d, %f, %f, %d, %d, %d, %d, %d, %d, %d, %d, "%s", "%s", NOW())' %\
        (uniqueId, header.RunStart, header.RunStop, header.NumEvents,
         header.NumHitEvents, header.NumTrackEvents,
         header.NumNoHitEvents, header.NumNoHitsEvents,
         header.NumMalformedEvents, header.NumBackwardEvents,
         E3PIPE_EXIT_CODE_SUCCESS, dstFile.version(), dstLastModDatetime)
    db.execute(query, commit = True)


def e3registerFailure(uniqueId, lockFilePath, db):
    """ Register into the run database a run that we failed to process.
    """
    try:
        lockLastModTime = time.gmtime(os.path.getmtime(lockFilePath))
        lockLastModDatetime = time.strftime('%Y-%m-%d %H:%M:%S',
                                            lockLastModTime)
        statusCode = open(lockFilePath).readline().strip('\n')
        statusCode = int(statusCode.split()[2])
        query = 'INSERT INTO run_table (unique_run_id, processing_status_code, last_processing, last_update) VALUES(%d, %d, "%s", NOW())' %\
            (uniqueId, statusCode, lockLastModDatetime)
    except Exception, e:
        logger.info(e)
        query = 'INSERT INTO run_table (unique_run_id, processing_status_code, last_update) VALUES(%d, %d, NOW())' %\
            (uniqueId, E3PIPE_EXIT_CODE_UNKNOWN)
    db.execute(query, commit = True)


def e3registerRun(rawFilePath, db):
    """ Register a previously processed run into the run database.
    """
    info = E3RawDataInfo(rawFilePath)
    uniqueId = uniqueRunIdFromFilePath(rawFilePath)
    if os.path.exists(info['DstFilePath']):
        e3registerSuccess(uniqueId, info['DstFilePath'], db)
    else:
        e3registerFailure(uniqueId, info['LockFilePath'], db)

    



if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser()
    (opts, args) = parser.parse_args()
    db = E3RunDbInterface()
    for arg in args:
        e3registerRun(arg, db)
