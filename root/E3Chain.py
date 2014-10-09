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


import os
import ROOT

from e3pipe.__logging__ import logger, abort
from e3pipe.root.E3InputRootFile import E3InputRootFile


class E3Chain(ROOT.TChain):

    """ Small wrapper around the TChain class.
    """

    EXTENSION = E3InputRootFile.EXTENSION

    def __init__(self, filePath, treeName):
        """ Constructor.
        """
        if not os.path.exists(filePath):
            abort('Could not find input file %s' % filePath)
        if not filePath.endswith(self.EXTENSION):
            abort('Wrong file extension for input file %s (%s expected)' %\
                  (filePath, self.EXTENSION))
        logger.info('Initializing TChain %s...' % treeName)
        ROOT.TChain.__init__(self, treeName)
        self.Add(filePath)
        logger.info('Done, %d entries found.' % self.GetEntries())

    def hist1d(self, expression, cut = '', **kwargs):
        """ Create a 1 dimensional histogram.
        """
        pass

    def hist2d(self, expression, cut = '', **kwargs):
        """ Create a 1 dimensional histogram.
        """
        pass



def test(filePath, treeName):
    """ Test program.
    """
    t = E3Chain(filePath, treeName)
    print t



if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser()
    (opts, args) = parser.parse_args()
    for filePath in args:
        test(filePath, 'Events')
