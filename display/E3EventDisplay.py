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
from e3pipe.tracking.E3FittingTool2d import E3FittingTool2d
from e3pipe.tracking.E3Point import E3Point
from e3pipe.tracking.E3Vector import E3Vector
from e3pipe.tracking.E3Track import E3Track

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
        self.__FittingTool = E3FittingTool2d()
        self.__Canvas = E3EventCanvas(self.__Z)
        self.__Canvas.Show()
        self.__CurrentHits = []
        self.__CurrentTrack = None

    def canvas(self):
        """ Return thr underlying canvas.
        """
        return self.__Canvas

    def z(self, i):
        """ Return the z-coordinate of the i-th plane.
        
        (0 is bottom and 2 is top.)
        """
        return self.__Z[i]

    def currentHits(self):
        """
        """
        return self.__CurrentHits
    
    def currentTrack(self):
        """
        """
        return self.__CurrentTrack

    def readEvent(self, event, refit = False, verbose = True):
        """ Read all the event information and store it in memory.
        """
        self.__CurrentHits = []
        self.__CurrentTrack = None
        self.GetEntry(event)
        x = self.value('PosXBot')
        y = self.value('PosYBot')
        z = self.__Z[0]
        self.__CurrentHits.append(E3Point(x, y, z))
        x = self.value('PosXMid')
        y = self.value('PosYMid')
        z = self.__Z[1]
        self.__CurrentHits.append(E3Point(x, y, z))
        x = self.value('PosXTop')
        y = self.value('PosYTop')
        z = self.__Z[2]
        self.__CurrentHits.append(E3Point(x, y, z))
        if refit:
            self.__CurrentTrack = self.refitTrack(verbose)
        else:
            x0 = self.value('IntersectXMid')
            y0 = self.value('IntersectYMid')
            # Note there is apparently a bug where IntersectZMid is always
            # 80 and cannot be used here.
            z0 = self.__Z[1]
            origin = E3Point(x0, y0, z0)
            # Also, it looks like we need a couple of extra minus sign here.
            # We should agree on the reference system.
            xdir = -self.value('XDir')
            ydir = -self.value('YDir')
            zdir = self.value('ZDir')
            direction = E3Vector(xdir, ydir, zdir)
            self.__CurrentTrack = E3Track(origin, direction)
            chi2 = self.value('ChiSquare')
            self.__CurrentTrack.setChi2(chi2)
        if verbose:
            self.__printEventInfo(event)

    def __printEventInfo(self, event):
        """ Print event information.
        """
        print '*** Information for event %d ***' % event
        for hit in self.__CurrentHits:
            print hit
        print self.__CurrentTrack

    def display(self, event, color = ROOT.kBlue, refit = False):
        """ Display a single event.
        """
        self.__Canvas.setup()
        self.overlay(event, color, refit)
        self.displayEventInfo()

    def overlay(self, event, color, refit = False):
        """ Convenience method for displaying without erasing.
        """
        self.readEvent(event, refit)
        self.displayHits(color)
        self.displayTrack(color, refit)
        self.displayResiduals(color)

    def displayHits(self, color):
        """ Display the hits.
        
        Note that we keep track of the 
        """
        for hit in self.__CurrentHits:
            self.__Canvas.drawMarker(hit.x(), hit.y(), hit.z(),
                                     MarkerColor = color)

    def refitTrack(self, verbose = True):
        """ Refit the track points.
        """
        logger.info('Refitting track points...')
        self.__FittingTool.run(self.__CurrentHits)
        if verbose:
            print self.__FittingTool
        return self.__FittingTool.track()

    def displayTrack(self, color, refit):
        """ Display the first track.
        """
        x0 = self.__CurrentTrack.x0()
        y0 = self.__CurrentTrack.y0()
        z0 = self.__CurrentTrack.z0()
        xdir = self.__CurrentTrack.xdir()
        ydir = self.__CurrentTrack.ydir()
        zdir = self.__CurrentTrack.zdir()
        self.__Canvas.drawLine(x0, y0, z0, xdir, ydir, zdir, bot = 1000,
                               top = 1000, LineColor = color, LineWidth = 1,
                               LineStyle = 7)

    def displayResiduals(self, color, zpad = 4., textSize = 0.8):
        """ Display the best-track residuals.
        """
        if self.value('TimeOfFlight') < 0:
            zpad = -zpad
        for hit in self.__CurrentHits:
            resx = hit.x() - self.__CurrentTrack.extrapolate(hit.z()).x()
            text = '%.1f cm' % resx
            if resx > 0:
                text = '+%s' % text
            text = '  %s' % text
            self.__Canvas.annotateXZ(hit.x(), hit.z() + zpad, text,
                                     color = color, align = 12, size = textSize)
            resy = hit.y() - self.__CurrentTrack.extrapolate(hit.z()).y()
            text = '%.1f cm' % resy
            if resy > 0:
                text = '+%s' % text
            text = '  %s' % text
            self.__Canvas.annotateYZ(hit.y(), hit.z() + zpad, text,
                                     color = color, align = 12, size = textSize)

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
