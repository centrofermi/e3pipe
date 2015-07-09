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
from e3pipe.mc.E3PoissonService import E3PoissonService
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
        self.__PoissonService = E3PoissonService(7.5e-3*MRPC_ACTIVE_AREA)
        self.__FittingTool = E3FittingTool2d()

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
        timestamp = self.__PoissonService.next()
        # Extract a random direction from the flux service.
        mcDirection = self.__FluxService.next()
        # Extract a random point on the top plane.
        mcHitTop = self.randomPoint(plane = 2)
        # Create the MC track and extrapolate it to the other planes.
        mcTrack = E3Track(mcHitTop, mcDirection)
        mcHitMid = mcTrack.extrapolate(self.zmid())
        mcHitBot = mcTrack.extrapolate(self.zbot())
        # Check that the event triggered the telescope.
        if not self.withinActiveArea(mcHitBot.x(), mcHitBot.y()):
            return
        # Digitize the hits in the detector.
        digiHitTop = self.digitize(mcHitTop)
        digiHitMid = self.digitize(mcHitMid)
        digiHitBot = self.digitize(mcHitBot)
        # Find the best-fit track.
        self.__FittingTool.run([digiHitBot, digiHitMid, digiHitTop])
        reconTrack = self.__FittingTool.track()
        # Calculate the track length and the time of flight.
        pbot = reconTrack.extrapolate(self.zbot())
        ptop = reconTrack.extrapolate(self.ztop())
        trackLength = pbot.dist(ptop)
        c = 29979245800.
        tof = trackLength/c*1000000000
        # Rotate the director cosines in the absolute reference system.
        mcDirectionRot = mcDirection.rotatez(self.phiNorth(), deg = True)
        reconDirectionRot = reconTrack.direction().rotatez(self.phiNorth(),
                                                           deg = True)
        return {'Seconds'        : timestamp.seconds(),
                'Nanoseconds'    : timestamp.nanoseconds(),
                'McPosXBot'      : mcHitBot.x(),
                'McPosYBot'      : mcHitBot.y(),
                'McPosXMid'      : mcHitMid.x(),
                'McPosYMid'      : mcHitMid.y(),
                'McPosXTop'      : mcHitTop.x(),
                'McPosYTop'      : mcHitTop.y(),
                'McXDir'         : mcDirectionRot.x(),
                'McYDir'         : mcDirectionRot.y(),
                'McZDir'         : mcDirectionRot.z(),
                'PosXBot'        : digiHitBot.x(),
                'PosYBot'        : digiHitBot.y(),
                'PosXMid'        : digiHitMid.x(),
                'PosYMid'        : digiHitMid.y(),
                'PosXTop'        : digiHitTop.x(),
                'PosYTop'        : digiHitTop.y(),
                'IntersectXMid'  : reconTrack.x0(),
                'IntersectYMid'  : reconTrack.y0(),
                'IntersectZMid'  : reconTrack.z0(),
                'XDir'           : reconDirectionRot.x(),
                'YDir'           : reconDirectionRot.y(),
                'ZDir'           : reconDirectionRot.z(),
                'ChiSquare'      : reconTrack.chi2(),
                'TimeOfFlight'   : tof,
                'TrackLength'    : trackLength
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
