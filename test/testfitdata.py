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


""" Synopsis: this is reading a ROOT DST file, extracting the hit positions
and re-running the stripped down version of the track fitting in the EEE
Analyzer to check for consistency.
"""


from e3pipe.display.E3EventDisplay import E3EventDisplay
from e3pipe.tracking.E3FittingToolAnalyzer import E3FittingToolAnalyzer
from e3pipe.tracking.E3FittingTool2d import E3FittingTool2d



def test(filePath):
    """
    """
    fitter1 = E3FittingToolAnalyzer()
    fitter2 = E3FittingTool2d()
    display = E3EventDisplay(filePath)
    for i in range(display.GetEntries()):
        display.readEvent(i)
        hits = display.currentHits()
        print 'Rerunning the stripped-down Analyzer fitter...'
        fitter1.run(hits)
        print fitter1
        print 'Running the 2d fitter...'
        fitter2.run(hits)
        print fitter2
        raw_input()




if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser()
    (opts, args) = parser.parse_args()
    for arg in args:
        test(arg)
