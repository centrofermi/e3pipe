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


import math

from e3pipe.root.__ROOT__ import *
from e3pipe.__logging__ import logger
from e3pipe.mc.E3Vector import E3Vector



class E3MuonFluxService:
    
    """ Flux service for muons.
    """

    def __init__(self):
        """ Constructor.
        """
        logger.info('Initializing muon flux service...')
        self.__ThetaDist = ROOT.TF1('muon_theta', 'cos(x)**[0]', 0, math.pi/2.)
        self.__ThetaDist.SetParameter(0, 1.85)
        self.__PhiDist = ROOT.TF1('muon_phi', '1', -math.pi, math.pi)

    def randomDirection(self):
        """ Return a random muon direction.
        """
        theta = self.__ThetaDist.GetRandom()
        phi = self.__PhiDist.GetRandom()
        xdir = math.cos(phi)*math.sin(theta)
        ydir = math.sin(phi)*math.sin(theta)
        zdir = math.cos(theta)
        return E3Vector(xdir, ydir, zdir)



def test(numEvents = 100000):
    """
    """
    from e3pipe.root.E3H1D import E3H1D
    svc = E3MuonFluxService()
    htheta = E3H1D('htheta', 'Theta', 100, 0, 90)
    hphi = E3H1D('hphi', 'Phi', 100, -180, 180)
    for i in xrange(numEvents):
        v = svc.randomDirection()
        htheta.Fill(v.theta())
        hphi.Fill(v.phi())
    return htheta, hphi



if __name__ == '__main__':
    from e3pipe.root.E3Canvas import E3Canvas
    htheta, hphi = test()
    c1 = E3Canvas('c1')
    htheta.Draw()
    c1.Update()
    c2 = E3Canvas('c2')
    hphi.SetMinimum(0)
    hphi.Draw()
    c2.Update()
