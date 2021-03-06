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


class E3DstWeatherTree(E3Tree):
    
    """ Class describing the ROOT tree containing the run-by-run header
    information.
    """

    NAME = 'Weather'
    BRANCHES = [E3BranchDescriptor('Seconds', 'i'),
                E3BranchDescriptor('IndoorTemperature', 'F'),
                E3BranchDescriptor('OutdoorTemperature', 'F'),
                E3BranchDescriptor('Pressure', 'F')
            ]

    def __init__(self):
        """ Constructor.
        """
        E3Tree.__init__(self, 'Weather tree')



def test():
    """
    """
    tree = E3DstWeatherTree()



if __name__ == '__main__':
    test()
