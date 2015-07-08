#!/usr/bin/env python
# *********************************************************************
# * Copyright (C) 2015 Luca Baldini (luca.baldini@pi.infn.it)         *
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

from e3pipe.tracking.E3Point import E3Point
from e3pipe.tracking.E3Vector import E3Vector
from e3pipe.tracking.E3Track import E3Track
from e3pipe.tracking.E3FittingToolBase import E3FittingToolBase


class E3FittingToolAnalyzer(E3FittingToolBase):

    """ Simple two-dimensional track-fitting tool.
    """

    def fitTrack(self, hits):
        """ Run the track fitting.

        This is a stripped-down version of the code in the Analyzer, with the
        variable names being the same to facilitate a direct comparison.
        """
        # Initialize the hits.
	xxB = hits[0].x()
        yyB = hits[0].y()
        zzB = hits[0].z()
	xxM = hits[1].x()
        yyM = hits[1].y()
        zzM = hits[1].z()
	xxT = hits[2].x()
        yyT = hits[2].y()
        zzT = hits[2].z()
        #----------------------------------------------------------------------
        sumX = xxB + xxM + xxT
	sumY = yyB + yyM + yyT
	sumZ = zzB + zzM + zzT

        sXZ = xxB*zzB + xxM*zzM + xxT*zzT
	sYZ = yyB*zzB + yyM*zzM + yyT*zzT
	sX2 = xxB*xxB + xxM*xxM + xxT*xxT
	sY2 = yyB*yyB + yyM*yyM + yyT*yyT
	sZ2 = zzB*zzB + zzM*zzM + zzT*zzT
	sumZ2 = sumZ*sumZ
        
	# Fit procedure in the 3D-space	        
	p0 = (3.*sXZ - sumX*sumZ) / (3.*sZ2 - sumZ2)
	p1 = (sumX - p0*sumZ) / 3.
	p2 = (3.*sYZ - sumY*sumZ) / (3.*sZ2 - sumZ2)
	p3 = (sumY - p2*sumZ) / 3.        
	n0 = p0 / math.sqrt(1. + p0*p0 + p2*p2)
	n1 = p2 / math.sqrt(1. + p0*p0 + p2*p2)
	n2 = 1. / math.sqrt(1. + p0*p0 + p2*p2)
	zzz = n0*n0 + n1*n1 + n2*n2
        
        # Evaluation of distances between points and line in 3D-space.
	dd = math.sqrt(zzz) 
	axB = n2*(yyB - p3) - n1*zzB
	ayB = -1 * n2 * (xxB - p1) + n0 * zzB
	azB = n1 * (xxB - p1) - n0*(yyB - p3)
        distB = math.sqrt((axB)**2. + (ayB)**2. + (azB)**2.) / dd

        axM = n2*(yyM - p3) - n1*zzM
	ayM = -1 * n2 * (xxM - p1) + n0 * zzM
	azM = n1 * (xxM - p1) - n0*(yyM - p3)
	distM = math.sqrt((axM)**2. + (ayM)**2. + (azM)**2.) / dd

        axT = n2*(yyT - p3) - n1*zzT
	ayT = -1 * n2 * (xxT - p1) + n0 * zzT
	azT = n1 * (xxT - p1) - n0*(yyT - p3)
	distT = math.sqrt((axT)**2. + (ayT)**2. + (azT)**2.) / dd

        chi2 = math.sqrt(distB**2. + distM**2. + distT**2.)
        #----------------------------------------------------------------------
        # Build the best-fit track object.
        # Note that, in order to recover the track origin, I add back the
        # original hit coordinates to the distances calculated into the
        # chisquare loop (wow!)
        p0 = E3Point(xxM + axM, yyM + ayM, zzM)
        v0 = E3Vector(n0, n1, n2)
        track = E3Track(p0, v0)
        track.setChi2(chi2)
        return track



def test():
    """
    """
    fitTool = E3FittingToolAnalyzer()
    # Real event from FRAS-02-2014-10-30-00018_dst.root (11878)
    # Processed with e3pipe 2.1.0 gives:
    # root [4] Events.Scan("XDir:YDir:ZDir:ChiSquare", "EventNumber==11878")
    # ************************************************************
    # *    Row   *      XDir *      YDir *      ZDir * ChiSquare *
    # ************************************************************
    # *    11878 * -0.050563 * 0.1976770 * 0.9789620 * 1.6044100 *
    # ************************************************************
    hits = [E3Point(79.229, 38.400, 0.000),
            E3Point(82.742, 32.000, 40.000),
            E3Point(83.922, 22.400, 80.000)
            ]
    fitTool.run(hits)
    print fitTool.track()



if __name__ == '__main__':
    test()
