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


from e3pipe.root.E3Tree import E3Tree
from e3pipe.root.E3BranchDescriptor import E3BranchDescriptor
from e3pipe.root.E3H1D import E3H1D



class E3McEventTree(E3Tree):
    
    """ Class describing the ROOT tree containing all the event-by-event
    information for the Monte Carlo sim.
    """

    NAME = 'McEvents'
    BRANCHES = [E3BranchDescriptor('EventNumber', 'i'),
                E3BranchDescriptor('Trigger', 'i'),
                E3BranchDescriptor('XDir', 'F'),
                E3BranchDescriptor('YDir', 'F'),
                E3BranchDescriptor('ZDir', 'F'),
            ]
    ALIAS_DICT = {'Theta'    : '57.29577951308232*acos(ZDir)',
                  'Phi'      : '57.29577951308232*atan2(YDir, XDir)'}

    def __init__(self):
        """ Constructor.
        """
        E3Tree.__init__(self, 'Monte Carlo Event tree')

    def doMonitoring(self):
        """ Create the standard set of monitoring plots.
        """
        self.hist1d('Theta', cut = CUT_GOOD_TRACK,
                    xmin = 0., xmax = 70., xbins = 50,
                    XTitle = '#theta [#circ]')
        self.hist1d('Phi', cut = CUT_GOOD_TRACK,
                    xmin = -180., xmax = 180., xbins = 50,
                    XTitle = '#phi [#circ]', Minimum = 0.)

def test():
    """
    """
    tree = E3McEventTree()



if __name__ == '__main__':
    test()
