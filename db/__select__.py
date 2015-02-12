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

from e3pipe.db.E3RunDbInterface import E3RunDbInterface



def _select(startDate, endDate, selection = None, db = None):
    """ Base function.
    """
    _closeOnExit = False
    if db is None:
        db = E3RunDbInterface()
        _closeOnExit = True
    query = 'SELECT station_name, run_date, run_id from runs WHERE '
    query += 'run_date BETWEEN "%s" AND "%s"' % (startDate, endDate)
    if selection:
        query += ' AND %s' % selection
    query += ';'
    db.execute(query, commit = False)
    runList = [(station, str(date), runId) for \
                   (station, date, runId) in db.fetchall()]
    if _closeOnExit:
        db.close()
    return runList


def selectRunsToBeProcessed(startDate, endDate, minSize = 0, overwrite = False,
                            db = None):
    """
    """
    selection = 'bin_file_size > %d' % minSize
    if not overwrite:
        selection += ' AND processing_status_code IS NULL'
    return _select(startDate, endDate, selection, db)


def selectProcessedRuns(startDate, endDate, selection):
    """
    """
    pass


def test():
    """ Test program.
    """
    endDate = datetime.date.today()
    startDate = endDate - datetime.timedelta(1)
    for run in selectRunsToBeProcessed(startDate, endDate):
        print run

  


if __name__ == '__main__':
    test()
