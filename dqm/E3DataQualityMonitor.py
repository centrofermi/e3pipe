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
from e3pipe.config.__dqm__ import DQM_BASELINE_PLOT_LIST,\
    DQM_BASELINE_ALARM_LIST
from e3pipe.__utils__ import createFolder, cp
from e3pipe.__package__ import E3PIPE_DQM



class E3DataQualityMonitor:

    """ Basic DQM class.
    """

    def __init__(self, filePath, outputFolder = None):
        """ Constructor.
        """
        self.__InputFile = E3InputRootFile(filePath)
        self.__Label = os.path.basename(filePath).replace('_dst.root', '')
        self.__OutputFolder = outputFolder
        self.__AlarmList = []

    def alarms(self):
        """ Return the list of active alarms.
        """
        return self.__AlarmList

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
            plot.GetXaxis().SetNdivisions(507)
            plot.GetXaxis().SetLabelOffset(0.04)
            plot.GetXaxis().SetTimeFormat('#splitline{%d/%m/%y}{%H:%M:%S}')

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
        self.__AlarmList.append(_alarm)
        logger.info(_alarm)

    def run(self):
        """ Run the data quality monitoring on a DST file.
        """
        if self.__OutputFolder is not None:
            createFolder(self.__OutputFolder)
        for plotName, kwargs in DQM_BASELINE_PLOT_LIST:
            self.draw(plotName, **kwargs)
        for objName, alarmName, errMin, warnMin, warnMax, errMax, kwargs in \
            DQM_BASELINE_ALARM_LIST:
            self.alarm(objName, alarmName, errMin, warnMin, warnMax, errMax,
                       **kwargs)
        self.createReport()
        self.createSummary()

    def createSummary(self):
        """ Create the alarm summary.
        """
        summary = E3AlarmSummary()
        for alarm in self.__AlarmList:
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
        img = '%s.png' % self.canvasName('RateTrackEvents', 'y_values')
        outputFile.image(img, width = '49%')
        img = '%s.png' % self.canvasName('ChiSquare', 'x_average')
        outputFile.image(img, width = '49%')
        outputFile.section('Run summary')
        header = self.__InputFile.Get('Header')
        header.GetEntry(0)
        outputFile.write('<p></p>\n')
        outputFile.write('<ul>\n')
        outputFile.li('DST file path: %s' % self.__InputFile.GetName())
        outputFile.li('Run duration: %.3f s' % header.RunDuration)
        outputFile.li('Number of events: %s' % header.NumEvents)
        outputFile.li('Number of events with track(s): %s' %\
                      header.NumTrackEvents)
        outputFile.li('Number of GPS events: %s' % header.NumGpsEvents)
        outputFile.write('</ul>\n')
        outputFile.section('Alarm summary')
        outputFile.write('\n<table width=100%>\n')
        outputFile.write('%s\n' % E3Alarm.HTML_TABLE_HEADER)
        for i, alarm in enumerate(self.__AlarmList):
            outputFile.write('%s\n' % alarm.htmlTableRow(True, i))
        outputFile.write('</table>\n<p></p>\n')
        outputFile.close()
        logger.info('Done.')
        



def test(filePath):
    """ Test function.
    """
    monitor = E3DataQualityMonitor(filePath, None)
    monitor.run()



if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser()
    (opts, args) = parser.parse_args()
    test(args[0])
