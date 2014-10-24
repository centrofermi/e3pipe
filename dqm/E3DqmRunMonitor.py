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
from e3pipe.dqm.E3Alarm import E3Alarm
from e3pipe.dqm.E3AlarmSummary import E3AlarmSummary
from e3pipe.dqm.E3HtmlOutputFile import E3HtmlOutputFile
from e3pipe.config.__dqm__ import DQM_BASELINE_LIST, TOP_IMAGES, dqmPreformat
from e3pipe.__utils__ import createFolder, cp
from e3pipe.__package__ import E3PIPE_DQM
from e3pipe.root.__ROOT__ import setupTimeDisplay



class E3DqmRunMonitor:

    """ Basic DQM class.
    """

    def __init__(self, filePath, outputFolder = None):
        """ Constructor.
        """
        self.__InputFile = E3InputRootFile(filePath)
        self.__Label = os.path.basename(filePath).replace('_dst.root', '')
        self.__OutputFolder = outputFolder
        self.__ObjectList = []
        dqmPreformat(self.__InputFile)

    def objects(self):
        """ Return the list of active alarms.
        """
        return self.__ObjectList

    def canvasName(self, objName, alarmName = None):
        """
        """
        name = 'c%s' % objName
        if alarmName is not None:
            name += '_%s' % alarmName
        return name

    def setupTimeDisplay(self, plot):
        """ Setup the x-axis labels for strip charts.
        """
        if plot.GetXaxis().GetTimeDisplay():
            setupTimeDisplay(plot, Ndivisions = 504, LabelOffset = 0.04)

    def draw(self, objName, **kwargs):
        """ Draw a plot from the DST.
        """
        _canvas = E3Canvas(self.canvasName(objName), **kwargs)
        _rootObject = self.__InputFile.Get(objName)
        self.setupTimeDisplay(_rootObject)
        _rootObject.Draw()
        _canvas.annotate(0.1, 0.94, self.__Label)
        _canvas.Update()
        if self.__OutputFolder is not None:
            _canvas.save(self.__OutputFolder)
        self.__ObjectList.append(objName)

    def alarm(self, objName, alarmName, errMin, warnMin, warnMax, errMax,
              **kwargs):
        """ Apply an alarm on a ROOT object from the DST.
        """
        exec('from e3pipe.dqm.alarm_%s import alarm_%s as alarmClass' %\
             (alarmName, alarmName))
        _canvas = E3Canvas(self.canvasName(objName, alarmName), **kwargs)
        _rootObject = self.__InputFile.Get(objName)
        self.setupTimeDisplay(_rootObject)
        _rootObject.Draw()
        _canvas.annotate(0.1, 0.94, self.__Label)
        _alarm = alarmClass(_rootObject, errMin, warnMin, warnMax, errMax)
        _alarm.run()
        _alarm.draw()
        _canvas.Update()
        if self.__OutputFolder is not None:
            _canvas.save(self.__OutputFolder)
        self.__ObjectList.append(_alarm)
        logger.info(_alarm)

    def run(self):
        """ Run the data quality monitoring on a DST file.

        TODO: the way we distinguish between plots and alarms is actually ugly,
        we need to find a better way to handle this.
        """
        if self.__OutputFolder is not None:
            createFolder(self.__OutputFolder)
        for item in DQM_BASELINE_LIST:
            if item is None:
                self.__ObjectList.append(item)
            elif len(item) == 2:
                plotName, kwargs = item
                self.draw(plotName, **kwargs)
            elif len(item) == 7:
                objName, alarmName, errMin, warnMin, warnMax, errMax,\
                    kwargs = item
                self.alarm(objName, alarmName, errMin, warnMin, warnMax, errMax,
                           **kwargs)
        self.createReport()
        self.createSummary()

    def createSummary(self):
        """ Create the alarm summary.
        """
        summary = E3AlarmSummary()
        for alarm in self.__ObjectList:
            if isinstance(alarm, E3Alarm):
                summary.fill(alarm)
        logger.info(summary)
        if self.__OutputFolder is not None:
            filePath = os.path.join(self.__OutputFolder, '.summary')
            summary.write(filePath)

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
        outputFile = E3HtmlOutputFile(filePath)
        outputFile.write('<p></p>\n')
        for objName, alarmName in TOP_IMAGES:
            img = '%s.png' % self.canvasName(objName, alarmName)
            outputFile.image(img, width = '49%')
        outputFile.section('Run summary')
        header = self.__InputFile.Get('Header')
        header.GetEntry(0)
        outputFile.write('<p></p>\n')
        outputFile.write('<ul>\n')
        outputFile.li('DST file path: %s' % self.__InputFile.GetName())
        outputFile.li('Unique run identifier: %s' %\
                      header.UniqueRunId)
        outputFile.li('Smallest event timestamp: %.3f s UTC' % header.RunStart)
        outputFile.li('Largest event timestamp: %.3f s UTC' % header.RunStop)
        outputFile.li('Run duration (largest - smallest timestamp): %.3f s' %\
                      header.RunDuration)
        outputFile.li('Total number of events: %s' %\
                      header.NumEvents)
        outputFile.li('Number of events with hits: %s' %\
                      header.NumHitsEvents)
        outputFile.li('Number of events with a track: %s' %\
                      header.NumTrackEvents)
        outputFile.li('Number of GPS events: %s' %\
                      header.NumGpsEvents)
        outputFile.li('Number of events with no hits: %s' %\
                      header.NumNoHitsEvents)
        outputFile.li('Number of malformed events: %s'% \
                      header.NumMalformedEvents)
        outputFile.li('Number of events out of order: %s'% \
                      header.NumBackwardEvents)
        outputFile.write('</ul>\n')
        outputFile.section('Weather station')
        outputFile.write('<p></p>\n')
        outputFile.write('<ul>\n')
        weather = self.__InputFile.Get('Weather')
        if weather.GetEntries():
            weather.GetEntry(0)
            delta = weather.Seconds - header.RunStart
            if delta < 0:
                text = '(%.3f s before the start of the run)' % abs(delta)
            else:
                text = '(%.3f s after (!!) the start of the run)' % abs(delta)
            outputFile.li('Readout at %.3f s UTC %s' % (weather.Seconds, text))
            outputFile.li('Outdoor temperature: %.2f deg C' %\
                          weather.OutdoorTemperature)
            outputFile.li('Indoor temperature: %.2f deg C' %\
                          weather.IndoorTemperature)
            outputFile.li('Pressure: %d hPa' % weather.Pressure)
        else:
            outputFile.li('Weather station data not found.')
        outputFile.write('</ul>\n')
        outputFile.section('Alarm summary')
        outputFile.write('\n<table width=100%>\n')
        outputFile.write('%s\n' % E3Alarm.HTML_TABLE_HEADER)

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
            row += ('<td></td>' * 4)
            row += '</tr>'
            return row

        for i, item in enumerate(self.__ObjectList):
            if item is None:
                outputFile.write('%s\n' % _htmlTableRow('', False, i))
            if isinstance(item, E3Alarm):
                outputFile.write('%s\n' % item.htmlTableRow(True, i))
            elif isinstance(item, str):
                outputFile.write('%s\n' % _htmlTableRow(item, True, i))
        outputFile.write('</table>\n<p></p>\n')
        outputFile.close()
        logger.info('Done.')
        



def test(filePath):
    """ Test function.
    """
    monitor = E3DqmRunMonitor(filePath, None)
    monitor.run()



if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser()
    (opts, args) = parser.parse_args()
    test(args[0])
