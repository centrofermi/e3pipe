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


from e3pipe.dst.__runid__ import runStationId


class E3Event:

    """ Small container class serving the basic purpose of being able to
    sort events while searching for coincidences.
    """

    def __init__(self, runId, evtId, seconds, nanoseconds, theta, phi,
                 chisquare):
        """ Constructor.
        """
        self.UniqueRunId = runId
        self.EventId = evtId
        self.Seconds = seconds
        self.Nanoseconds = nanoseconds
        self.Theta = theta
        self.Phi = phi
        self.Chisquare = chisquare

    def timestamp(self):
        """ Return the timestamp of the event.
        """
        return self.Seconds + 1.e-9*self.Nanoseconds

    def stationId(self):
        """ Return the station ID encoded in the unique run ID.
        """
        return runStationId(self.UniqueRunId)

    def __cmp__(self, other):
        """ Comparison operator (for sorting).
        """
        if self.timestamp() > other.timestamp():
            return 1
        elif self.timestamp() < other.timestamp():
            return -1
        else:
            return 0
