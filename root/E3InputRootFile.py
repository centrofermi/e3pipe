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
from e3pipe.root.E3RootFileBase import E3RootFileBase



class E3InputRootFile(ROOT.TFile):

    """ Small convenience base class for input ROOT files.

    This will essentially check that a file exists and, possibly, that
    it has the right extension.
    """

    def __init__(self, filePath):
        """
        """
        if not os.path.exists(filePath):
            abort('Could not find input file %s' % filePath)
        if not filePath.endswith(E3RootFileBase.EXTENSION):
            abort('Wrong file extension for input file %s (%s expected)' %\
                  (filePath, E3RootFileBase.EXTENSION))
        logger.info('Opening input file %s...' % filePath)
        ROOT.TFile.__init__(self, filePath)
        logger.info('Creator: %s' % self.creator())
        logger.info('Version: %s' % self.version())
        logger.info('Creation time: %s' % self.creationTime())
        logger.info('Date: %s' % self.date())
        logger.info('Station: %s' % self.station())

    def readString(self, key):
        """ Read a piece of text from the ROOT file.
        """
        try:
            return self.Get(key).GetTitle()
        except ReferenceError:
            return 'N/A'

    def creator(self):
        """
        """
        return self.readString(E3RootFileBase.CREATOR_KEY)

    def version(self):
        """
        """
        return self.readString(E3RootFileBase.VERSION_KEY)

    def creationTime(self):
        """
        """
        return self.readString(E3RootFileBase.CREATION_TIME_KEY)

    def date(self):
        """
        """
        return self.readString(E3RootFileBase.DATE_KEY)

    def station(self):
        """
        """
        return self.readString(E3RootFileBase.STATION_KEY)

    def canvasLabel(self):
        """
        """
        return '%s %s' % (self.station(), self.date())

    def filter(self, *args, **kwargs):
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
                    if not kwargs.get('strict') or rootObject.__class__ == arg:
                        outputList.append(rootObject)
                    break
        return outputList

    def __str__(self):
        """ Terminal formatting.
        """

        def _format(obj):
            """ Nested function for basic formatting.
            """
            return '* [ROOT.%s] %s (%s)\n' %\
                (obj.__class__.__name__, obj.GetName(), obj.GetTitle())

        text = ''
        text += '\n### Annotation(s)\n'
        for label in self.filter(ROOT.TNamed, strict = True):
            text += _format(label)
        text += '\n### Tree(s)\n'
        for tree in self.filter(ROOT.TTree):
            text += _format(tree)
            for branch in tree.GetListOfBranches():
                text += '    * %s\n' % branch.GetTitle()
        text += '\n### Histogram(s)\n'
        for hist in self.filter(ROOT.TH1):
            text += _format(hist)
        return text



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
