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
from dst.__runid__ import runStation, runDate, runId
from e3pipe.__logging__ import logger


def e3backfillRunInfo():
    """
    """
    db = E3RunDbInterface()
    query = 'SELECT * from run_table WHERE station_name is NULL;'
    db.execute(query)
    i = 0
    for row in db.fetchall():
        logger.info('Processing row %d' % i)
        uniqueId = row[4]
        _runStation = runStation(uniqueId)
        _runDate = '%s' % runDate(uniqueId)
        _runId = runId(uniqueId)
        query = 'UPDATE run_table SET station_name = "%s", run_date = "%s", run_id = %d WHERE unique_run_id = %d' %\
            (_runStation, _runDate, _runId, uniqueId)
        db.execute(query, commit = True)
        i += 1
    db.close()



if __name__ == '__main__':
    e3backfillRunInfo()
