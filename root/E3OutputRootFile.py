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
import time

from e3pipe.__logging__ import logger, abort
from e3pipe.__version__ import TAG
from e3pipe.root.E3RootFileBase import E3RootFileBase



def writeString(key, value):
    """ Write a string to the current ROOT file.

    The text can be retrieved from the file using the
    E3InputRootFile.readString() method.
    """
    string = ROOT.TNamed(key, str(value))
    logger.info('Writing %s (%s) to output file...' % (key, value))
    string.Write()
    return string



class E3OutputRootFile(ROOT.TFile):

    """ Small convenience base class for output ROOT files.

    Here we give a common interface to write "annotations" in the output
    file---most notably the version of the software that created it.
    """

    def __init__(self, filePath, creator = 'e3pipe', date = None,
                 station = None):
        """
        """
        if not filePath.endswith(E3RootFileBase.EXTENSION):
            abort('Please root the %s extension for ROOT files' %\
                  E3RootFileBase.EXTENSION)
        logger.info('Opening output file %s...' % filePath)
        ROOT.TFile.__init__(self, filePath, 'RECREATE')
        writeString(E3RootFileBase.CREATOR_KEY, creator)
        writeString(E3RootFileBase.VERSION_KEY, TAG)
        writeString(E3RootFileBase.CREATION_TIME_KEY, time.asctime())
        if date is not None:
            writeString(E3RootFileBase.DATE_KEY, date)
        if station is not None:
            writeString(E3RootFileBase.STATION_KEY, station)

    def Close(self):
        """
        """
        logger.info('Closing output file %s...' % self.GetName())
        ROOT.TFile.Close(self)

