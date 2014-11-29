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
from e3pipe.__logging__ import logger
from e3pipe.config.__storage__ import E3RawDataInfo
from e3pipe.dst.__runid__ import uniqueRunIdFromFilePath
from e3pipe.dst.E3DstHeaderChain import E3DstHeaderChain
from e3pipi.tasks.____exitcodes__ import E3PIPE_EXIT_CODE_SUCCESS
from e3pipe.__version__ import TAG


"""
  `unique_run_id` bigint(20) unsigned NOT NULL,
  `run_start` double DEFAULT NULL,
  `run_stop` double DEFAULT NULL,
  `run_tag` tinyint(3) unsigned DEFAULT NULL,
  `run_comment` text,
  `num_events` int(10) unsigned DEFAULT NULL,
  `num_hit_events` int(10) unsigned DEFAULT NULL,
  `num_track_events` int(10) unsigned DEFAULT NULL,
  `num_no_hit_events` int(10) unsigned DEFAULT NULL,
  `num_no_hits_events` int(10) unsigned DEFAULT NULL,
  `num_malformed_events` int(10) unsigned DEFAULT NULL,
  `num_backward_events` int(10) unsigned DEFAULT NULL,
  `processing_status_code` tinyint(3) unsigned DEFAULT NULL,
  `e3pipe_version` char(10) DEFAULT NULL,
  `last_processing` datetime DEFAULT NULL,
  `last_update` datetime DEFAULT NULL,
"""


def e3registerSuccess(uniqueId, dstFilePath, db):
    """
    """
    header = E3DstHeaderChain(dstFilePath)
    query = """INSERT INTO run_table
    (unique_run_id, run_start, run_stop, num_events, num_hit_events,
    num_track_events, num_no_hit_events, num_no_hits_events,
    num_malformed_events, num_backward_events, processing_status_code,
    e3pipe_version, last_processing, last_update)
    VALUES(%d, %f, %f, %d, %d, %d, %d, %d, %d, %d, %d, "%s", NOW(), NOW())""" %\
        (uniqueId, header.RunStart, header.RunStop, header.NumEvents,
         header.NumNoHitEvents, header.NumNoHitsEvents,
         header.NumMalformedEvents, header.NumBackwardEvents,
         E3PIPE_EXIT_CODE_SUCCESS, TAG)
    print query


def e3registerFailure(uniqueId, lockFilePath, db):
    """
    """
    query = """INSERT INTO run_table
    (unique_run_id, processing_status_code, e3pipe_version, last_processing,
    last_update)
    VALUES(%d, %d, "%s", NOW(), NOW())""" %\
        (uniqueId, 1, TAG)
    print query


def e3registerRun(rawFilePath, db):
    """ Register a previously processed run into the run database.
    """
    info = E3RawDataInfo(rawFilePath)
    uniqueId = uniqueRunIdFromFilePath(rawFilePath)
    if os.path.exists(dstFilePath):
        e3registerSuccess(uniqueId, info['DstFilePath'])
    else:
        e3registerFailure(uniqueId, info['LockFilePath'])

    



if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser()
    (opts, args) = parser.parse_args()
    db = E3RunDbInterface()
    for arg in args:
        e3registerRun(arg, db)
