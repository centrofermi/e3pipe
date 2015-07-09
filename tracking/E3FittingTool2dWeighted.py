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


from e3pipe.tracking.E3FittingTool2d import E3FittingTool2d
from e3pipe.tracking.E3Point import E3Point



class E3FittingTool2dWeighted(E3FittingTool2d):

    """ Simple two-dimensional track-fitting tool.
    """

    def __init__(self):
        """ Constructor.
        """
        E3FittingTool2d.__init__(self, weighted = True)



def test():
    """
    """
    fitTool = E3FittingTool2dWeighted()
    # Real event from FRAS-02-2014-10-30-00018_dst.root (11878)
    # Processed with e3pipe 2.1.0 gives:
    # root [4] Events.Scan("XDir:YDir:ZDir:ChiSquare", "EventNumber==11878")
    # ************************************************************
    # *    Row   *      XDir *      YDir *      ZDir * ChiSquare *
    # ************************************************************
    # *    11878 * -0.050563 * 0.1976770 * 0.9789620 * 1.6044100 *
    # ************************************************************
    hits = [E3Point(79.229, 38.400, 0.000),
            E3Point(82.742, 32.000, 40.000),
            E3Point(83.922, 22.400, 80.000)
            ]
    fitTool.run(hits)
    print fitTool.track()
    


if __name__ == '__main__':
    test()       
