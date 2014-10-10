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


class E3InputRootFile(ROOT.TFile):

    """ Small convenience base class for input ROOT files.

    This will essentially check that a file exists and, possibly, that
    it has the right extension.
    """

    EXTENSION = '.root'

    def __init__(self, filePath):
        """
        """
        if not os.path.exists(filePath):
            abort('Could not find input file %s' % filePath)
        if not filePath.endswith(self.EXTENSION):
            abort('Wrong file extension for input file %s (%s expected)' %\
                  (filePath, self.EXTENSION))
        logger.info('Opening input file %s...' % filePath)
        ROOT.TFile.__init__(self, filePath)

    def readString(self, key):
        """ Read a piece of text from the ROOT file.
        """
        try:
            return self.Get(key).GetTitle()
        except ReferenceError:
            logger.error('Could not find key "%s" in the ROOT file.' % key)
            return None

    def filter(self, *args):
        """ Filter the objects in the file based on their class.

        This involves looping over the list of keys in the file,
        retrieving the corresponding objects and returning a list of
        objects matching the types specified in the arguments passed 
        to the function.
        """
        outputList = []
        for key in self.GetListOfKeys():
            rootObject = self.Get(key.GetName())
            for arg in args:
                if isinstance(rootObject, arg):
                    outputList.append(rootObject)
                    break
        return outputList    



def test(filePath):
    """ Test program.
    """
    f = E3InputRootFile(filePath)
    print f



if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser()
    (opts, args) = parser.parse_args()
    for filePath in args:
        test(filePath)
