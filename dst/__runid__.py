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


""" We do reset the run ID at the beginning of each day, but sometimes it is
handy to have a unique run ID, so that we can unambigously identify an event
by a pair of numbers: its run ID and event ID.

This small utility module handles the conversions between the two schemes.
"""


import datetime

from e3pipe.config.__stations__ import E3_STATION_DICT, E3_STATION_ID_DICT
from e3pipe.config.__storage__ import splitFilePath
from e3pipe.dst.__time__ import E3_DATE_REFERENCE
from e3pipe.__logging__ import logger, abort


DATE_MULTIPLIER = 100000
STATION_MULTIPLIER = 10000*DATE_MULTIPLIER


def uniqueRunId(station, date, runId):
    """ Turn a triplet (station, date, runId) into a unique ID.
    """
    try:
        stationId = E3_STATION_DICT[station]
    except KeyError:
        abort('Unknown station: %s' % station)
    dateId = (date - E3_DATE_REFERENCE).days
    return stationId*STATION_MULTIPLIER + dateId*DATE_MULTIPLIER + runId
    
def uniqueRunIdFromFilePath(filePath):
    """ Return the unique run ID corresponding to a given file path.
    """
    station, year, month, day, runId = splitFilePath(filePath)
    date = datetime.date(int(year), int(month), int(day))
    return uniqueRunId(station, date, int(runId))

def runStation(uniqueId):
    """ Return the run station corresponding to a unique ID.
    """
    stationId = int(uniqueId/STATION_MULTIPLIER)
    return E3_STATION_ID_DICT[stationId]

def runDate(uniqueId):
    """ Return the run date corresponding to a unique ID.
    """
    stationId = int(uniqueId/STATION_MULTIPLIER)
    days = int((uniqueId - stationId*STATION_MULTIPLIER)/DATE_MULTIPLIER)
    return E3_DATE_REFERENCE + datetime.timedelta(days)

def runId(uniqueId):
    """ Return the run ID corresponding to a unique ID.
    """
    stationId = int(uniqueId/STATION_MULTIPLIER)
    days = int((uniqueId - stationId*STATION_MULTIPLIER)/DATE_MULTIPLIER)
    return int(uniqueId - stationId*STATION_MULTIPLIER - days*DATE_MULTIPLIER)

def runInfo(uniqueId):
    """ 
    """
    return runStation(uniqueId), runDate(uniqueId), runId(uniqueId)




if __name__ == '__main__':
    filePath = '/data/CATA-02/data/2014-10-21/CATA-02-2014-10-21-00019.bin'
    uniqueId = uniqueRunIdFromFilePath(filePath)
    print filePath
    print uniqueId
    print runStation(uniqueId)
    print runDate(uniqueId)
    print runId(uniqueId)
    print runInfo(uniqueId)
