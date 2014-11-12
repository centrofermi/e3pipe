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

from e3pipe.mc.E3Point import E3Point
from e3pipe.mc.E3Vector import E3Vector
from e3pipe.mc.E3Track import E3Track
from e3pipe.mc.E3MuonFluxService import E3MuonFluxService



class E3BaseTelescope:

    """ Base class describing the basic geometry of a telescope.

    Here is an extract from the analyzer:

    Y-coordinate is perpendicular to strip direction:
    Y=0 for strip 1 Y=82 for strip 24

    X-coordinate is along the strip direction and obtained from the
    time-difference is proportional to (T_left-T_right) which goes from -10 ns
    to +10 ns:
    (T_left - T_right)=-9 X=0
    (T_left - T_right)=+9 X=158

    We use a coordinate system whose origin is in one of the corners of the
    lowermost RPC plane.
    """

    WIDTH = 85.56
    LENGTH = 158.0
    ACTIVE_AREA = WIDTH*LENGTH
    NUM_STRIPS_PER_PLANE = 24

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

    def name(self):
        """ Return the name.
        """
        return self.__Name

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

    def shootMuon(self):
        """ Generate and propagate a muon track through the detector. 
        """
        # Extract a random point on the top plane.
        x = random.uniform(0., self.LENGTH)
        y = random.uniform(0., self.WIDTH)
        z = self.ztop()
        ptop = E3Point(x, y, z)
        # Extract a random direction from the flux service.
        theta, phi = self.__FluxService.randomDirection()
        # Calculate the cosine directors.
        xdir = math.cos(phi)*math.sin(theta)
        ydir = math.sin(phi)*math.sin(theta)
        zdir = math.cos(theta)
        v0 = E3Vector(xdir, ydir, zdir)
        # Extrapolate the MC track to the bottom plane---note this has to be
        # done in instrument coordinates, e.g., before we rotate taking the
        # angle to North into account.
        track = E3Track(ptop, v0)
        pmid = track.extrapolate(self.zmid())
        pbot = track.extrapolate(self.zbot())
        trg = self.withinActiveArea(pbot.x(), pbot.y())
        # Rotate phi from instrument coordinates to absolute coordinates.
        phi += math.radians(self.phiNorth())
        if phi > math.pi:
            phi -= 2*math.pi
        # Calculate the new xdir and ydir.
        xdir = math.cos(phi)*math.sin(theta)
        ydir = math.sin(phi)*math.sin(theta)
        return {'McXDir': xdir, 'McYDir': ydir, 'McZDir': zdir, 'Trigger': trg}

    def withinActiveArea(self, x, y):
        """ Return whether a given (x, y) two-dimensional point is within
        the active area.
        """
        return x >= 0 and x <= self.LENGTH and y >= 0 and y <= self.WIDTH

    def __str__(self):
        """ String formatting.
        """
        return '%s: z = %s, phi to N = %.3f' %\
            (self.name(), self.__Z, self.phiNorth(), )



if __name__ == '__main__':
    telescope = E3BaseTelescope()
    p = telescope.randomPoint()
    print p
    print telescope.withinActiveArea(p.x(), p.y())
