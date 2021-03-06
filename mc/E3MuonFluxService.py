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
from e3pipe.tracking.E3VectorSpherical import E3VectorSpherical



class E3MuonFluxService:
    
    """ Flux service for muons.
    """

    def __init__(self):
        """ Constructor.
        """
        logger.info('Initializing muon flux service...')
        self.__ThetaDist = ROOT.TF1('muon_theta', 'sin(x)*cos(x)**[0]',
                                    0, math.pi/2.)
        self.__ThetaDist.SetParameter(0, 2.0)
        self.__PhiDist = ROOT.TF1('muon_phi', '1', -math.pi, math.pi)

    def setThetaDistParameter(self, i, value):
        """ Set a parameter for the theta distribution.
        """
        logger.info('Setting parameter %d for theta distribution to %.3f...' %\
                    (i, value))
        self.__ThetaDist.SetParameter(i, value)

    def next(self):
        """ Return a random muon direction.
        """
        theta = self.__ThetaDist.GetRandom()
        phi = self.__PhiDist.GetRandom()
        return E3VectorSpherical(theta, phi)



def test(numEvents = 100000):
    """
    """
    from e3pipe.root.E3H1D import E3H1D
    svc = E3MuonFluxService()
    htheta = E3H1D('htheta', 'Theta', 100, 0, 90)
    hphi = E3H1D('hphi', 'Phi', 100, -180, 180)
    for i in xrange(numEvents):
        d = svc.next()
        htheta.Fill(d.theta())
        hphi.Fill(d.phi())
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
