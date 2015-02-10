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
from e3pipe.dst.E3DstHeaderChain import E3DstHeaderChain
from e3pipe.dst.__runid__ import uniqueRunId
from e3pipe.root.E3InputRootFile import E3InputRootFile
from e3pipe.tasks.__exitcodes__ import E3PIPE_EXIT_CODE_SUCCESS,\
    E3PIPE_EXIT_CODE_UNKNOWN


def _register(runInfo, db = None, **kwargs):
    """ Base function.
    """
    station = info['Station']
    date = info['DateString']
    runId = info['RunNumber']
    kwargs['unique_run_id'] = uniqueRunId(station, date, runId)
    dstFilePath = info['DstFilePath']
    if os.path.exists(dstFilePath):
        dstLastModTime = time.gmtime(os.path.getmtime(dstFilePath))
        dstLastModDatetime = time.strftime('%Y-%m-%d %H:%M:%S', dstLastModTime)
        kwargs['last_processing'] = dstLastModDatetime
    kwargs['last_update'] = 'NOW()'
    _closeOnExit = False
    if db is None:
        db = E3RunDbInterface()
        _closeOnExit = True
    query = 'UPDATE runs SET '
    for key, value in kwargs.items():
        query += '%s = %s, ' % (key, value)
    query = query.strip(' ,')
    query += ' WHERE station_name = "%s" AND run_date = "%s" AND run_id = %d' %\
             (station, date, runId)
    db.execute(query, commit = True)
    if _closeOnExit:
        db.close()

def registerSuccess(runInfo, db = None):
    """ Register a success.
    """
    dstFilePath = info['DstFilePath']
    dstFile = E3InputRootFile(dstFilePath)
    header = dstFile.Get('Header')
    header.GetEntry(0)
    kwargs = {
        'run_start'             : header.RunStart,
        'run_stop'              : header.RunStop,
        'num_events'            : header.NumEvents,
        'num_hit_events'        : header.NumHitEvents,
        'num_track_events'      : header.NumTrackEvents,
        'num_no_hit_events'     : header.NumNoHitEvents,
        'num_no_hits_events'    : header.NumNoHitsEvent,
        'num_malformed_events'  : header.NumMalformedEvents,
        'num_backward_events'   : header.NumBackwardEvent,
        'processing_status_code': E3PIPE_EXIT_CODE_SUCCESS,
        'e3pipe_version'        : dstFile.version()
    }
    dstFile.Close()
    _register(runInfo, db, **kwargs)

def registerFailure(runInfo, exitCode, db = None):
    """ Registed a failure.
    """
    kwargs = {
        'processing_status_code': E3PIPE_EXIT_CODE_SUCCESS,
        'e3pipe_version'        : dstFile.version()
    }
    _register(runInfo, db, **kwargs)
    



def e3registerSuccess(uniqueId, dstFilePath, db):
    """ Register into the database a run successfully processed.
    """
    _runStation = runStation(uniqueId)
    _runDate = '%s' % runDate(uniqueId)
    _runId = runId(uniqueId)
    dstLastModTime = time.gmtime(os.path.getmtime(dstFilePath))
    dstLastModDatetime = time.strftime('%Y-%m-%d %H:%M:%S', dstLastModTime)
    dstFile = E3InputRootFile(dstFilePath)
    header = dstFile.Get('Header')
    header.GetEntry(0)
    query = 'UPDATE runs SET unique_run_id = %d, run_start = %f, run_stop = %f, num_events = %d, num_hit_events = %d, num_track_events = %d, num_no_hit_events = %d, num_no_hits_events = %d, num_malformed_events = %d, num_backward_events = %d, processing_status_code = %d, e3pipe_version = "%s", last_processing = "%s", last_update = NOW() WHERE station_name = "%s" AND run_date = "%s" AND run_id = %d' %\
        (uniqueId, header.RunStart, header.RunStop, header.NumEvents,
         header.NumHitEvents, header.NumTrackEvents,
         header.NumNoHitEvents, header.NumNoHitsEvents,
         header.NumMalformedEvents, header.NumBackwardEvents,
         E3PIPE_EXIT_CODE_SUCCESS, dstFile.version(), dstLastModDatetime,
         _runStation, _runDate, _runId)
    db.execute(query, commit = True)
    dstFile.Close()


def e3registerFailure(uniqueId, lockFilePath, db):
    """ Register into the run database a run that we failed to process.
    """
    _runStation = runStation(uniqueId)
    _runDate = '%s' % runDate(uniqueId)
    _runId = runId(uniqueId)
    try:
        lockLastModTime = time.gmtime(os.path.getmtime(lockFilePath))
        lockLastModDatetime = time.strftime('%Y-%m-%d %H:%M:%S',
                                            lockLastModTime)
        statusCode = open(lockFilePath).readline().strip('\n')
        statusCode = int(statusCode.split()[2])
        query = 'UPDATE runs SET unique_run_id = %d, processing_status_code = %d, last_processing = "%s", last_update = NOW() WHERE station_name = "%s" AND run_date = "%s" AND run_id = %d' %\
            (uniqueId, statusCode, lockLastModDatetime, _runStation, _runDate,
             _runId)
    except Exception, e:
        logger.info(e)
        query = 'UPDATE runs SET unique_run_id = %d, processing_status_code = %d, last_update = NOW() WHERE station_name = "%s" AND run_date = "%s" AND run_id = %d' %\
            (uniqueId, E3PIPE_EXIT_CODE_UNKNOWN, _runStation, _runDate, _runId)
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

    



