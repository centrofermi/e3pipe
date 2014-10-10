#!/usr/bin/env python
# *********************************************************************
# * Copyright (C) 2014 Luca Baldini (luca.baldini@pi.infn.it)         *
# *                                                                   *
# * For the license terms see the file LICENCE, distributed           *
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


from e3pipe.root.E3Tree import E3Tree
from e3pipe.root.E3BranchDescriptor import E3BranchDescriptor


class E3DstEventTree(E3Tree):
    
    """ Class describing the ROOT tree containing all the event-by-event
    information.
    """

    NAME = 'Events'
    BRANCHES = [E3BranchDescriptor('RunNumber', 'i'),
                E3BranchDescriptor('EventNumber', 'i'),
                E3BranchDescriptor('Seconds', 'i'),
                E3BranchDescriptor('Nanoseconds', 'i'),
                E3BranchDescriptor('XDir', 'F'),
                E3BranchDescriptor('YDir', 'F'),
                E3BranchDescriptor('ZDir', 'F'),
                E3BranchDescriptor('ChiSquare', 'F'),
                E3BranchDescriptor('TimeOfFlight', 'F'),
                E3BranchDescriptor('TrackLength', 'F'),
                E3BranchDescriptor('DeltaTime', 'F')
            ]
    ALIAS_DICT = {'Timestamp': 'Seconds + 1.e-9*Nanoseconds',
                  'Theta'    : '57.29577951308232*acos(ZDir)',
                  'Phi'      : '57.29577951308232*atan2(YDir, XDir)'}
    TRACK_CUT = 'ChiSquare >= 0'

    def __init__(self):
        """ Constructor.
        """
        E3Tree.__init__(self, 'Event tree')

    def runDuration(self):
        """ Return the run duration.
        """
        self.GetEntry(0)
        start = self.Seconds + 1.e-9*self.Nanoseconds
        self.GetEntry(self.GetEntries() - 1)
        stop = self.Seconds + 1.e-9*self.Nanoseconds
        return stop - start

    def numTrackEvents(self):
        """ Return the number of events with tracks.
        """
        return self.GetEntries(self.TRACK_CUT)

    def createMonitoringPlots(self):
        """ Create the standard set of monitoring plots.

        TODO: this should properly configured via a configuration file.
        """
        self.hist1d('Theta', self.TRACK_CUT,
                    xmin = 0., xmax = 70., xbins = 50,
                    XTitle = '#theta [#circ]')
        self.hist1d('Phi', self.TRACK_CUT,
                    xmin = -180., xmax = 180., xbins = 50,
                    XTitle = '#phi [#circ]', Minimum = 0.)
        self.hist1d('DeltaTime', xmin = -1, xmax = 1,
                    XTitle = 'Time difference [s]')
        self.hist1d('ChiSquare', self.TRACK_CUT,
                    xmin = 0, xmax = 50, xbins = 100,
                    XTitle = '#chi^{2}')
        self.hist1d('TimeOfFlight', self.TRACK_CUT,
                    xmin = -10, xmax = 20, xbins = 100,
                    XTitle = 'Time of flight [ns]')
        self.hist1d('TrackLength', self.TRACK_CUT,
                    xmin = 0, xmax = 300., xbins = 100,
                    XTitle = 'Track length [cm]')



def test():
    """
    """
    tree = E3DstEventTree()



if __name__ == '__main__':
    test()
