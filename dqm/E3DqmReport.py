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

from e3pipe.__logging__ import logger, abort
from e3pipe.root.E3InputRootFile import E3InputRootFile
from e3pipe.root.E3Canvas import E3Canvas
from e3pipe.dqm.E3HtmlOutputFile import E3HtmlOutputFile
from e3pipe.__utils__ import createFolder, cp
from e3pipe.dst.E3DstHeaderChain import E3DstHeaderChain
from e3pipe.dst.E3DstTrendingChain import E3DstTrendingChain



class E3DqmReport:

    """ Basic DQM report class.
    """

    def __init__(self, filePath, outputFolder = None):
        """ Constructor.
        """
        self.__InputFilePath = filePath
        self.__Label = os.path.basename(filePath).replace('.root', '')
        self.__OutputFolder = outputFolder
        self.__ObjectList = []

    def canvasName(self, objName):
        """
        """
        return 'c%s' % objName

    def fill(self):
        """
        """
        header = E3DstHeaderChain(self.__InputFilePath)
        header.doSummaryPlots()
        for _plot in header.plots():
            _canvas = E3Canvas(self.canvasName(_plot.GetName()))
            _plot.Draw()
            _canvas.annotate(0.1, 0.94, self.__Label)
            _canvas.Update()
            if self.__OutputFolder is not None:
                _canvas.save(self.__OutputFolder)
        self.__ObjectList.append(_canvas.GetName())
        trending = E3DstTrendingChain(self.__InputFilePath)
        trending.setupArrays()
        trending.setupTreeFormulae()
        trending.doSummaryPlots()
        for _plot in trending.plots():
            _canvas = E3Canvas(self.canvasName(_plot.GetName()))
            _plot.Draw('al')
            _canvas.annotate(0.1, 0.94, self.__Label)
            _canvas.Update()
            if self.__OutputFolder is not None:
                _canvas.save(self.__OutputFolder)
        self.__ObjectList.append(_canvas.GetName())



def test(filePath):
    """ Test function.
    """
    report = E3DqmReport(filePath, None)
    report.fill()



if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser()
    (opts, args) = parser.parse_args()
    test(args[0])

