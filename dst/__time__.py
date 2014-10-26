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


import ROOT
import time
import datetime

E3_DATE_OFFSET = ROOT.TDatime(2007,01,01,00,00,00)
E3_TIME_OFFSET = E3_DATE_OFFSET.Convert(True)


""" The format string for the dates used throughout.
"""
DATE_FMT_STRING = '%Y-%m-%d'

E3_DATE_REFERENCE = datetime.date(2007, 1, 1)
E3_DATETIME_REFERENCE = datetime.datetime(2007, 1, 1, 0, 0)


def date2str(date):
    """ Convert a date to string.
    """
    return date.strftime(DATE_FMT_STRING)


def str2date(string):
    """ Convert a string to date.
    """
    return datetime.datetime.strptime(string, DATE_FMT_STRING).date()

def isDST(dt):
    """ Return whether the daylight saving flag is on for a given
    datetime object.
    
    Mind this relies on the timezone of the computer the code is run on!
    """
    t = time.mktime(datetime.datetime.timetuple(dt))
    return time.localtime(t).tm_isdst 


if __name__ == '__main__':
    import time

    dt1 = datetime.datetime(2014, 10, 26, 1, 0)
    dt2 = datetime.datetime(2014, 10, 26, 3, 0)
    print dt1, isDST(dt1)
    print dt2, isDST(dt2)
