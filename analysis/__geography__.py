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


from math import sin, cos, acos, radians, atan2, degrees

from e3pipe.config.__stations__ import location


EARTH_RADIUS = 6371000.


def greatCircleDist(lat1, lon1, lat2, lon2):
    """ Return the shortest distance between two points on the surface of
    the Earth, measured along the surface of the Earth itself.

    The formula is taken from
    http://en.wikipedia.org/wiki/Great-circle_distance
    """
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)
    ds = acos(sin(lat1)*sin(lat2) + cos(lat1)*cos(lat2)*cos(abs(lon1 - lon2)))
    return EARTH_RADIUS*ds


def dist(station1, station2):
    """ Return the distance between two stations.
    """
    lat1, lon1, alt1 = location(station1)
    lat2, lon2, alt2 = location(station2)
    return greatCircleDist(lat1, lon1, lat2, lon2)


def phi(station1, station2):
    """ Return the angle phi, in degrees, between the segment connecting two
    stations and the north direction.

    Mind this is horrible and only valid in the Euclidean approximation.
    I believe it is aduquate for our needs, though.
    """
    lat1, lon1, alt1 = location(station1)
    lat2, lon2, alt2 = location(station2)
    dns = greatCircleDist(lat1, lon1, lat2, lon1)
    if lat1 > lat2:
        dns *= -1.
    dew = greatCircleDist(lat1, lon1, lat1, lon2)
    if lon1 > lon2:
        dew *= -1.
    return 90. - degrees(atan2(dns, dew))



if __name__ == '__main__':
    print dist('CAGL-01', 'CAGL-02'), phi('CAGL-01', 'CAGL-02')
    print dist('CAGL-01', 'CAGL-03'), phi('CAGL-01', 'CAGL-03')
    print dist('CAGL-02', 'CAGL-03'), phi('CAGL-02', 'CAGL-03')
