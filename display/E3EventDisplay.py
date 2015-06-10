#!/usr/bin/env python
# *********************************************************************
# * Copyright (C) 2015 Luca Baldini (luca.baldini@pi.infn.it)         *
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


from e3pipe.root.__ROOT__ import *
from e3pipe.dst.E3DstEventChain import E3DstEventChain
from e3pipe.config.__stations__ import geometry
from e3pipe.root.E3InputRootFile import E3InputRootFile
from e3pipe.display.E3EventCanvas import E3EventCanvas
from e3pipe.__logging__ import logger
from e3pipe.mc.E3FittingTool import E3FittingTool
from e3pipe.mc.E3Point import E3Point

import os


class E3EventDisplay(E3DstEventChain):
    """ Class encapsulating an event display.
    """

    def __init__(self, *fileList):
        """
        """
        station = E3InputRootFile(fileList[0]).station()
        self.__FileName = os.path.basename(fileList[0])
        logger.info('Parsing telescope geometry for %s...' % station)
        phiNorth, d12, d23 = geometry(station)
        self.__Z = [0, d12, d12 + d23]
        logger.info('Plane z values: %s' % self.__Z)
        E3DstEventChain.__init__(self, *fileList)
        self.setupArrays()
        self.__FittingTool = E3FittingTool()
        self.__Canvas = E3EventCanvas(self.__Z)
        self.__Canvas.Show()

    def display(self, event, color = ROOT.kBlue, refit = False):
        """ Display a single event.
        """
        self.__Canvas.setup()
        self.overlay(event, color, refit)

    def overlay(self, event, color, refit = False):
        """ Convenience method for displaying without erasing.
        """
        self.GetEntry(event)
        self.__printEventInfo(event)
        self.displayHits(color)
        self.displayTrack(color, refit)
        self.displayEventInfo()

    def __printEventInfo(self, event):
        """ Print event information.
        """
        print '*** Information for event %d ***' % event
        print 'Top hit: (%.2f, %.2f, %.2f) cm' %\
            (self.value('PosXTop'), self.value('PosYTop'), self.__Z[2])
        print 'Mid hit: (%.2f, %.2f, %.2f) cm' %\
            (self.value('PosXMid'), self.value('PosYMid'), self.__Z[1])
        print 'Bot hit: (%.2f, %.2f, %.2f) cm' %\
            (self.value('PosXBot'), self.value('PosYBot'), self.__Z[0])
        print 'Track direction: (%.2f, %.2f, %.2f)' %\
            (self.value('XDir'), self.value('YDir'), self.value('ZDir'))
        print 'Track intersection: (%.2f, %.2f, %.2f) **z is wrong **' %\
            (self.value('IntersectXMid'), self.value('IntersectYMid'),
             self.value('IntersectZMid'))
        print 'Track chisquare: %.3f' % (self.value('ChiSquare'))

    def displayHits(self, color):
        """ Display the hits.
        """
        x = self.value('PosXBot')
        y = self.value('PosYBot')
        z = self.__Z[0]
        self.__Canvas.drawMarker(x, y, z, MarkerColor = color)
        x = self.value('PosXMid')
        y = self.value('PosYMid')
        z = self.__Z[1]
        self.__Canvas.drawMarker(x, y, z, MarkerColor = color)
        x = self.value('PosXTop')
        y = self.value('PosYTop')
        z = self.__Z[2]
        self.__Canvas.drawMarker(x, y, z, MarkerColor = color)

    def refitTrack(self):
        """ Refit the track points.
        """
        logger.info('Refitting track points...')
        p1 = E3Point(self.value('PosXBot'), self.value('PosYBot'), self.__Z[0])
        p2 = E3Point(self.value('PosXMid'), self.value('PosYMid'), self.__Z[1])
        p3 = E3Point(self.value('PosXTop'), self.value('PosYTop'), self.__Z[2])
        self.__FittingTool.run([p1, p2, p3])
        print self.__FittingTool.track()
        return self.__FittingTool.track()

    def displayTrack(self, color, refit = False):
        """ Display the first track.
        """
        if refit:
            t = self.refitTrack()
            x0 = t.x0()
            y0 = t.y0()
            z0 = t.z0()
            xdir = -t.xdir()
            ydir = -t.ydir()
            zdir = t.zdir()
        else:
            x0 = self.value('IntersectXMid')
            y0 = self.value('IntersectYMid')
            # Note there is apparently a bug where IntersectZMid is always
            # 80 and cannot be used here.
            z0 = self.__Z[1]
            xdir = self.value('XDir')
            ydir = self.value('YDir')
            zdir = self.value('ZDir')
        self.__Canvas.drawLine(x0, y0, z0, xdir, ydir, zdir, bot = 1000,
                               top = 1000, LineColor = color, LineWidth = 1,
                               LineStyle = 7)

    def displayEventInfo(self):
        """ Display the event information.
        """
        evt = self.value('EventNumber')
        run = self.value('UniqueRunId')
        self.__Canvas.drawEventInfo(self.__FileName, run, evt)

        

def test(*fileList):
    """ Test code.
    """
    c = E3EventDisplay(*fileList)
    c.display(0, refit = True)
    


if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser()
    (opts, args) = parser.parse_args()
    test(*args)
