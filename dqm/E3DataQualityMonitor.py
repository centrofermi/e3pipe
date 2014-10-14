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
from e3pipe.dqm.E3HtmlOutputFile import E3HtmlOutputFile
from e3pipe.__utils__ import createFolder



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
        _canvas = E3Canvas('c%s' % objName, **kwargs)
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
        _canvas = E3Canvas('c%s_%s' % (objName, alarmName), **kwargs)
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

        TODO: this should be fully configurable from a file---possibly
        on a telescope-by-telescope basis.
        """
        if self.__OutputFolder is not None:
            createFolder(self.__OutputFolder)
        self.draw('Phi')
        self.draw('Theta')
        self.alarm('ChiSquare', 'x_average', 1, 2, 6, 10, Logy = True)
        self.alarm('DeltaTime', 'exp_fit_lambda', 5, 10, 50, 75, Logy = True)
        self.draw('TimeOfFlight')
        self.draw('TrackLength')
        self.alarm('RateTrackEvents', 'y_values', 5, 10, 50, 75)
        self.alarm('HitMultTop', 'x_average', 0.5, 0.75, 2, 3, Logy = True)
        self.alarm('HitMultMid', 'x_average', 0.5, 0.75, 2, 3, Logy = True)
        self.alarm('HitMultBot', 'x_average', 0.5, 0.75, 2, 3, Logy = True)
        self.alarm('HitMultTotal', 'x_average', 1.5, 2.5, 6, 9, Logy = True)
        self.alarm('ClusterMultTop', 'x_average', 0.5, 0.75, 2, 3, Logy = True)
        self.alarm('ClusterMultMid', 'x_average', 0.5, 0.75, 2, 3, Logy = True)
        self.alarm('ClusterMultBot', 'x_average', 0.5, 0.75, 2, 3, Logy = True)
        self.alarm('ClusterMultTotal', 'x_average', 1.5, 2.5, 6, 9, Logy = True)
        self.createReport()

    def createReport(self):
        """ Create the html report.
        """
        if self.__OutputFolder is None:
            logger.info('No DQM output folder set, skipping report...')
            return
        logger.info('Writing DQM report...')
        filePath = os.path.join(self.__OutputFolder, 'dqmreport.html')
        outputFile = E3HtmlOutputFile(filePath)
        outputFile.write('<table>\n')
        outputFile.write('%s\n' % E3Alarm.HTML_TABLE_HEADER)
        for alarm in self.__AlarmList:
            outputFile.write('%s\n' % alarm.htmlTableRow())
        outputFile.write('</table>\n')
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
