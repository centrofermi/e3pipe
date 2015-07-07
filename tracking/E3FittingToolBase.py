#!/usr/bin/env python
# *********************************************************************
# * Copyright (C) 2015 Luca Baldini (luca.baldini@pi.infn.it)         *
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


import math

from e3pipe.tracking.E3Point import E3Point
from e3pipe.tracking.E3Vector import E3Vector
from e3pipe.tracking.E3Track import E3Track


class E3FittingToolBase:

    DEFAULT_TRACK = E3Track(E3Point(-1., -1., -1), E3Vector(-1., -1., -1.), -1.)

    """ Base class for track fitting.
    """

    def __init__(self):
        """ Constructor.
        """
        self.clear()

    def track(self):
        """ Return the best-fit track.
        """
        return self.__Track

    def setTrack(self, track):
        """ Set the best-fit track.
        """
        self.__Track = track

    def clear(self):
        """ Reset the best-fit track.
        """
        self.setTrack(self.DEFAULT_TRACK)

    def __str__(self):
        """ String formatting.
        """
        return '%s' % self.__Track

    def fitTrack(self, hits):
        """ Do-nothing hook.
        The actual fitting code is implemented in the actual sub-classes.
        """
        return self.DEFAULT_TRACK

    def run(self, hits):
        """ Run the fit.
        """
        self.clear()
        if len(hits) < 2:
            return
        self.setTrack(self.fitTrack(hits))



def test():
    """ Test function
    """
    fitTool = E3FittingToolBase()
    hits = [E3Point(20.00, -53.28, 142.00),
            E3Point(35.00, -37.05, 97.00),
            E3Point(55.00, -21.60, 53.00)
    ]
    fitTool.run(hits)
    print fitTool.track()



if __name__ == '__main__':
    test()
