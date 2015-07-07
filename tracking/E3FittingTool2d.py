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

from e3pipe.tracking.E3Point import E3Point
from e3pipe.tracking.E3Vector import E3Vector
from e3pipe.tracking.E3Track import E3Track
from e3pipe.tracking.E3FittingToolBase import E3FittingToolBase


class E3FittingTool2d(E3FittingToolBase):

    """ Simple two-dimensional track-fitting tool.
    """

    def fitTrack(self, hits):
        """ Run the track fitting.
        """
        # Initialize some variables for the fit.
        n = 0
        sx = 0.
        sx_z = 0.
        sx_zz = 0.
        sx_x = 0.
        sx_zx = 0.
        sy = 0.
        sy_z = 0.
        sy_zz = 0.
        sy_y = 0.
        sy_zy = 0.
        wx = 1
        wy = 1
        # Loop over the points.
        # Note that, since the weights correspond to errors in the x and y
        # directions, the two views are fitted in the z-x and z-y (as opposed to
        # x-z and y-z) planes (i.e. z acts as the abscissa in both cases). This
        # also turns out to be handy since we measure the theta angle
        # (i.e. zdir) from the z axis, rather than the x-y plane.
        for hit in hits:
            n += 1
            sy += wy
            sy_z += hit.z()*wy
            sy_zz += hit.z()*hit.z()*wy;
            sy_y += hit.y()*wy;
            sy_zy += hit.z()*hit.y()*wy;
            sx += wx;
            sx_z += hit.z()*wx;
            sx_zz += hit.z()*hit.z()*wx;
            sx_x += hit.x()*wx;
            sx_zx += hit.z()*hit.x()*wx;
        # Go ahead with the fit parameters, i.e. the slopes in the two views.
        zxslope = (sx_zx*sx - sx_z*sx_x)/(sx_zz*sx - sx_z*sx_z)
        zyslope = (sy_zy*sy - sy_z*sy_y)/(sy_zz*sy - sy_z*sy_z)
        zxintercept = (sx_x*sx_zz - sx_zx*sx_z)/(sx_zz*sx - sx_z*sx_z)
        zyintercept = (sy_y*sy_zz - sy_zy*sy_z)/(sy_zz*sy - sy_z*sy_z)
        # Convert from the slope/intercept representation to the director
        # cosines.
        denom = math.sqrt(1 + zxslope*zxslope + zyslope*zyslope)
        xdir  = zxslope/denom
        ydir  = zyslope/denom
        zdir  = 1./denom
        v0 = E3Vector(xdir, ydir, zdir)
        # Refer the centroid to a common z0 value (e.g., the z of the
        # first hit)
        z0 = hits[0].z()
        x0 = zxintercept + z0*zxslope
        y0 = zyintercept + z0*zyslope
        p0 = E3Point(x0, y0, z0)
        track = E3Track(p0, v0)
        # Need a final loop to calculate the chisquare, here.
        chi2 = 0.
        err = 1.0
        for hit in hits:
            extr = track.extrapolate(hit.z())
            resx = hit.x() - extr.x()
            resy = hit.y() - extr.y()
            chi2 += (resx**2 + resy**2)
        track.setChi2(chi2)
        return track



def test():
    """
    """
    fitTool = E3FittingTool2d()
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
