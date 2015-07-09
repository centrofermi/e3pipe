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


import random
import math

from e3pipe.tracking.E3Point import E3Point
from e3pipe.tracking.E3Vector import E3Vector
from e3pipe.tracking.E3Track import E3Track
from e3pipe.mc.E3MuonFluxService import E3MuonFluxService
from e3pipe.tracking.E3FittingTool2d import E3FittingTool2d
from e3pipe.mc.__mrpc__ import *


class E3TelescopeBase:

    """ Base class describing the basic geometry of a telescope.

    We use a coordinate system whose origin is in one of the corners of the
    lowermost RPC plane.
    """

    def __init__(self, name = 'EEE-00',
                 d12 = 50., d23 = 50., phiNorth = 0.,
                 latitude = 0., longitude = 0, altitude = 0.,
                 triggerMask = 0b111):
        """ Constructor.
        """
        self.__Name = name
        self.__Z = [0., d12, d12 + d23]
        self.__PhiNorth = phiNorth
        self.__TriggerMask = triggerMask
        self.__Longitude = longitude
        self.__Latitude = latitude
        self.__Altitude = altitude
        self.__FluxService = E3MuonFluxService()
        self.__FittingTool = E3FittingTool2d()
        self.__CurrentSeconds = 0
        self.__CurrentNanoseconds = 0
        self.__MuonRate = 75./10000.*MRPC_ACTIVE_AREA

    def name(self):
        """ Return the name.
        """
        return self.__Name

    def fluxService(self):
        """
        """
        return self.__FluxService

    def z(self, plane):
        """ Return the z coordinate of a given plane (0 is the lowermost one,
        2 is the uppermost one.)
        """
        return self.__Z[plane]

    def ztop(self):
        """ Return the z coordinate of the uppermost plane.
        """
        return self.__Z[2]

    def zmid(self):
        """ Return the z coordinate of the mid plane.
        """
        return self.__Z[1]

    def zbot(self):
        """ Return the z coordinate of the lowermost plane.
        """
        return self.__Z[0]

    def phiNorth(self):
        """ Return the angle w.r.t. the magnetic North,
        """
        return self.__PhiNorth

    def randomPoint(self, plane = 2):
        """
        """
        x = random.uniform(0., MRPC_LENGTH)
        y = random.uniform(0., MRPC_WIDTH)
        z = self.z(plane)
        return E3Point(x, y, z)

    def shootMuon(self):
        """ Generate and propagate a muon track through the detector.

        This is actually the main class method as far as Monte Carlo
        simulations are concerned.
        
        TODO: we have to generalize for a generic trigger mask, which
        shouldn't be too hard.
        """
        # Extract a random time for a stationary Poisson process.
        dt = random.expovariate(self.__MuonRate)
        ns = int(dt*1000000 + 0.5)
        self.__CurrentNanoseconds += ns
        if self.__CurrentNanoseconds >= 1000000:
            s = self.__CurrentNanoseconds/1000000
            self.__CurrentSeconds += s
            self.__CurrentNanoseconds -= s*1000000
        # Extract a random point on the top plane.
        ptop = self.randomPoint(plane = 2)
        hits = [self.digitize(ptop)]
        trig = False
        # Extract a random direction from the flux service.
        mcTheta, mcPhi = self.__FluxService.randomDirection()
        # Calculate the cosine directors.
        mcXdir = math.cos(mcPhi)*math.sin(mcTheta)
        mcYdir = math.sin(mcPhi)*math.sin(mcTheta)
        mcZdir = math.cos(mcTheta)
        mcDirection = E3Vector(mcXdir, mcYdir, mcZdir)        
        # Extrapolate the MC track to the bottom plane---note this has to be
        # done in instrument coordinates, e.g., before we rotate taking the
        # angle to North into account.
        mcTrack = E3Track(ptop, mcDirection)
        pmid = mcTrack.extrapolate(self.zmid())
        if self.withinActiveArea(pmid.x(), pmid.y()):
            hits.append(self.digitize(pmid))
        pbot = mcTrack.extrapolate(self.zbot())
        if self.withinActiveArea(pbot.x(), pbot.y()):
            hits.append(self.digitize(pbot))
            trig = True
        # If we have more than three hits we can run the reconstruction!
        if len(hits) < 3:
            return
        self.__FittingTool.run(hits)
        recTrack = self.__FittingTool.track()
        chi2 = recTrack.chi2()
        recTheta = math.radians(recTrack.theta())
        recPhi = math.radians(recTrack.phi())
        # Rotate phi from instrument coordinates to absolute coordinates.
        mcPhi += math.radians(self.phiNorth())
        recPhi += math.radians(self.phiNorth())
        if mcPhi > math.pi:
            mcPhi -= 2*math.pi
        if recPhi > math.pi:
            recPhi -= 2*math.pi
        # Calculate the new xdir and ydir.
        mcXdir = math.cos(mcPhi)*math.sin(mcTheta)
        mcYdir = math.sin(mcPhi)*math.sin(mcTheta)
        recXdir = math.cos(recPhi)*math.sin(recTheta)
        recYdir = math.sin(recPhi)*math.sin(recTheta)
        recZdir = math.cos(recTheta)
        # Calculate the track length and the time of flight.
        p0 = recTrack.extrapolate(hits[0].z())
        p1 = recTrack.extrapolate(hits[2].z())
        length = math.sqrt((p0.x() - p1.x())**2. +\
                           (p0.y() - p1.y())**2. +\
                           (p0.z() - p1.z())**2.)
        v = 2997924.58
        tof = int(length/v*1000000 + 0.5)
        return {'Seconds'        : self.__CurrentSeconds,
                'Nanoseconds'    : self.__CurrentNanoseconds,
                'McPosXBot'      : pbot.x(),
                'McPosYBot'      : pbot.y(),
                'McPosXMid'      : pmid.x(),
                'McPosYMid'      : pmid.y(),
                'McPosXTop'      : ptop.x(),
                'McPosYTop'      : ptop.y(),
                'McXDir'         : mcXdir,
                'McYDir'         : mcYdir,
                'McZDir'         : mcZdir,
                'PosXBot'        : hits[2].x(),
                'PosYBot'        : hits[2].y(),
                'PosXMid'        : hits[1].x(),
                'PosYMid'        : hits[1].y(),
                'PosXTop'        : hits[0].x(),
                'PosYTop'        : hits[0].y(),
                'IntersectXMid'  : recTrack.x0(),
                'IntersectYMid'  : recTrack.y0(),
                'IntersectZMid'  : recTrack.z0(),
                'XDir'           : recXdir,
                'YDir'           : recYdir,
                'ZDir'           : recZdir,
                'ChiSquare'      : chi2,
                'TimeOfFlight'   : tof,
                'TrackLength'    : length
        }

    def withinActiveArea(self, x, y):
        """ Return whether a given (x, y) two-dimensional point is within
        the active area.
        """
        return x >= 0 and x <= MRPC_LENGTH and y >= 0 and y <= MRPC_WIDTH

    def digitize(self, point):
        """
        """
        x = random.gauss(point.x(), MRPC_LONGITUDINAL_SIGMA)
        y = int(point.y()/MRPC_STRIP_PITCH)*MRPC_STRIP_PITCH
        z = point.z()
        return E3Point(x, y, z)

    def __str__(self):
        """ String formatting.
        """
        return '%s: z = %s, phi to N = %.3f' %\
            (self.name(), self.__Z, self.phiNorth())



if __name__ == '__main__':
    telescope = E3TelescopeBase()
    print telescope
    p = telescope.randomPoint(2)
    print p, telescope.digitize(p)
