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


from e3pipe.mc.E3TelescopeBase import E3TelescopeBase
from e3pipe.config.__stations__ import E3_LOCATION_DICT, E3_GEOMETRY_DICT



class E3Telescope(E3TelescopeBase):

    """ Derived class to construct actual instances of the telescopes in
    operation.
    """

    def __init__(self, stationName, triggerMask = 0b111):
        """ Constructor.
        """
        geo = E3_GEOMETRY_DICT[stationName]
        loc = E3_LOCATION_DICT[stationName]
        E3TelescopeBase.__init__(self, stationName,
                                 geo['d12'], geo['d23'], geo['phi_north'],
                                 loc['lat'], loc['lon'], loc['alt'],
                                 triggerMask)


if __name__ == '__main__':
    telescope = E3Telescope('SAVO-01')
    print telescope
