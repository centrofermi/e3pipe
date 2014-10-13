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


import os
import ROOT

from e3pipe.__logging__ import logger, abort
from e3pipe.root.E3InputRootFile import E3InputRootFile
from e3pipe.root.E3H1D import E3H1D


class E3Chain(ROOT.TChain):

    """ Small wrapper around the TChain class.

    TODO: we probably want to move all the plotting stuff to a base
    class so that we can use it both when while writing and while
    reading trees.
    """

    EXTENSION = E3InputRootFile.EXTENSION
    ALIAS_DICT = {}

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
        self.__TreeFormulaDict = {}
        for key, value in self.ALIAS_DICT.items():
            logger.info('Setting alias "%s" -> "%s"...' % (key, value))
            self.SetAlias(key, value)
            self.__TreeFormulaDict[key] = ROOT.TTreeFormula(key, value, self)

    def value(self, key, entry = None):
        """
        """
        if entry is not None:
            self.GetEntry(entry)
        return self.__TreeFormulaDict[key].EvalInstance()



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
