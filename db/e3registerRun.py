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
from e3pipe.__version__ import TAG
from e3pipe.dst.E3DstHeaderChain import E3DstHeaderChain
from e3pipe.dst.__runid__ import uniqueRunId
from e3pipe.root.E3InputRootFile import E3InputRootFile
from e3pipe.tasks.__exitcodes__ import E3PIPE_EXIT_CODE_SUCCESS,\
    E3PIPE_EXIT_CODE_UNKNOWN


def _register(runInfo, db = None, **kwargs):
    """ Base function.
    """
    station = runInfo['Station']
    date = runInfo['Date']
    datestr = runInfo['DateString']
    runId = runInfo['RunNumber']
    kwargs['unique_run_id'] = uniqueRunId(station, date, runId)
    dstFilePath = runInfo['DstFilePath']
    if os.path.exists(dstFilePath):
        dstLastModTime = time.gmtime(os.path.getmtime(dstFilePath))
        dstLastModDatetime = time.strftime('%Y-%m-%d %H:%M:%S', dstLastModTime)
        kwargs['last_processing'] = '"%s"' % dstLastModDatetime
    kwargs['last_update'] = 'NOW()'
    kwargs['e3pipe_version'] = '"%s"' % TAG
    _closeOnExit = False
    if db is None:
        db = E3RunDbInterface()
        _closeOnExit = True
    query = 'UPDATE runs SET '
    for key, value in kwargs.items():
        query += '%s = %s, ' % (key, value)
    query = query.strip(' ,')
    query += ' WHERE station_name = "%s" AND run_date = "%s" AND run_id = %d' %\
             (station, datestr, runId)
    db.execute(query, commit = True)
    if _closeOnExit:
        db.close()

def registerSuccess(runInfo, db = None):
    """ Register a success.
    """
    dstFilePath = runInfo['DstFilePath']
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
        'num_no_hits_events'    : header.NumNoHitsEvents,
        'num_malformed_events'  : header.NumMalformedEvents,
        'num_backward_events'   : header.NumBackwardEvents,
        'processing_status_code': E3PIPE_EXIT_CODE_SUCCESS
    }
    dstFile.Close()
    _register(runInfo, db, **kwargs)

def registerFailure(runInfo, exitCode, db = None):
    """ Registed a failure.
    """
    kwargs = {
        'processing_status_code': exitCode
    }
    _register(runInfo, db, **kwargs)

def registerRun(runInfo, exitCode, db = None):
    """
    """
    if exitCode == E3PIPE_EXIT_CODE_SUCCESS:
        registerSuccess(runInfo, db)
    else:
        registerFailure(runInfo, exitCode, db)
