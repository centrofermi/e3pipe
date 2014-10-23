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
import os

from e3pipe.__logging__ import logger, startmsg, abort
from e3pipe.dqm.E3DqmReport import E3DqmReport
from e3pipe.tasks.e3merge import e3mergeTimeSpan
from e3pipe.config.__storage__ import E3PIPE_REPORTS_BASE
from e3pipe.dst.__time__ import date2str



def e3report(station, endDate = None, daysSpanned = 2, outputFolder = None,
             **kwargs):
    """ Read the DST and run the data quality monitoring.
    """
    endDate = endDate or datetime.date.today()
    startDate = endDate - datetime.timedelta(daysSpanned - 1)
    if outputFolder is None:
        outputFolder = os.path.join(E3PIPE_REPORTS_BASE, station,
                                    date2str(endDate))
    mergedFileName = '%s_%s_%s.root' % (station, startDate, endDate)
    mergedFilePath = os.path.join(outputFolder, mergedFileName)
    e3mergeTimeSpan(mergedFilePath, station, endDate, daysSpanned,
                    mergeEvents = False)
    report = E3DqmReport(mergedFilePath, outputFolder)
    report.fill(station, startDate, endDate)



if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser()
    (opts, args) = parser.parse_args()
    e3report(args[0])
