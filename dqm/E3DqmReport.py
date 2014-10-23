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

import e3pipe.__utils__ as __utils__

from e3pipe.__logging__ import logger, abort
from e3pipe.root.E3InputRootFile import E3InputRootFile
from e3pipe.root.E3Canvas import E3Canvas
from e3pipe.dqm.E3HtmlOutputFile import E3HtmlOutputFile
from e3pipe.__utils__ import createFolder, cp
from e3pipe.dst.E3DstHeaderChain import E3DstHeaderChain
from e3pipe.dst.E3DstTrendingChain import E3DstTrendingChain
from e3pipe.__package__ import E3PIPE_DQM
from e3pipe.dqm.E3HtmlOutputFile import htmlTableHeader


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
        """ Get the canvas name for a given plot.
        """
        return 'c%s' % objName

    def fill(self):
        """ Fill the report.
        """
        if self.__OutputFolder is not None:
            __utils__.createFolder(self.__OutputFolder)
        header = E3DstHeaderChain(self.__InputFilePath)
        header.doSummaryPlots()
        for _plot in header.plots():
            _canvas = E3Canvas(self.canvasName(_plot.GetName()))
            _plot.Draw()
            _canvas.annotate(0.1, 0.94, self.__Label)
            _canvas.Update()
            if self.__OutputFolder is not None:
                _canvas.save(self.__OutputFolder)
            self.__ObjectList.append(_plot.GetName())
        self.__ObjectList.append(None)
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
            self.__ObjectList.append(_plot.GetName())
        self.createReport()

    def createReport(self):
        """ Create the html report.

        TODO: this is ugly. We should refector the code so that objects
        encpsulating specific parts of the report (e.g., the Header TTree)
        are self-aware and can format themselves for html.

        TODO: we should be able to configure which plots end up on the top
        of the page.
        """
        if self.__OutputFolder is None:
            logger.info('No DQM output folder set, skipping report...')
            return
        cp(os.path.join(E3PIPE_DQM, 'e3pipe.css'), self.__OutputFolder)
        logger.info('Writing DQM report...')
        filePath = os.path.join(self.__OutputFolder, 'index.html')
        outputFile = E3HtmlOutputFile(filePath,
                                      header = 'EEE DQM summary report')
        outputFile.write('<p></p>\n')
        for objName in ['gRateTrackEvents', 'gFractionTrackEvents']:
            img = '%s.png' % self.canvasName(objName)
            outputFile.image(img, width = '49%')
        outputFile.section('Summary')
        outputFile.write('<ul>\n')
        outputFile.li('Station: ---')
        outputFile.li('Time period: ---')
        outputFile.li('Number of runs transferred to CNAF: --- ')
        outputFile.li('Number of runs processed: --- ')
        outputFile.li('Number of runs failed: --- ')
        outputFile.li('Data files: root, csv (header), csv (events)')
        outputFile.write('</ul>\n')
        outputFile.section('Summary plots')
        outputFile.write('\n<table width=100%>\n')
        outputFile.write('%s\n' % htmlTableHeader('ROOT object'))
        def _htmlTableRow(objName, linkPlot = True, index = None):
            """ Embedded function to make a table row on the fly.
            """
            if index is not None:
                if index % 2:
                    row = '<tr class="even">'
                else:
                    row = '<tr class="odd">'
            else:
                row = '<tr>'
            if linkPlot:
                plotName = 'c%s.png' % objName
                row += '<td><a href="%s">%s</a></td>' % (plotName, objName)
            else:
                row += '<td>%s</td>' % objName
            row += '</tr>'
            return row

        for i, item in enumerate(self.__ObjectList):
            if item is None:
                outputFile.write('%s\n' % _htmlTableRow('', False, i))
            else:
                outputFile.write('%s\n' % _htmlTableRow(item, True, i))
        outputFile.write('</table>\n<p></p>\n')
        outputFile.close()
        logger.info('Done.')



def test(filePath, outputFolder):
    """ Test function.
    """
    report = E3DqmReport(filePath, outputFolder)
    report.fill()



if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option('-o', '--output-folder', type = str,
                      default = None, dest = 'out',
                      help = 'path to the output folder')
    (opts, args) = parser.parse_args()
    
    test(args[0], opts.out)
