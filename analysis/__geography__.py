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


from math import sin, cos, acos, radians


EARTH_RADIUS = 6371000.


def spheredist(lat1, lon1, lat2, lon2):
    """
    """
    return EARTH_RADIUS*acos(sin(radians(lat1))*sin(radians(lat2)) + \
                             cos(radians(lat1))*cos(radians(lat2))* \
                             cos(abs(radians(lon1) - radians(lon2))))




if __name__ == '__main__':
    from e3pipe.config.__stations__ import E3_LOCATION_DICT
    lat1 = E3_LOCATION_DICT['CAGL-01']['lat']
    lon1 = E3_LOCATION_DICT['CAGL-01']['lon']
    lat2 = E3_LOCATION_DICT['CAGL-02']['lat']
    lon2 = E3_LOCATION_DICT['CAGL-02']['lon']
    print spheredist(lat1, lon1, lat2, lon2)
