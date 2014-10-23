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



class E3RootFileBase:

    """ Base class for the ROOT I/O.
    """
    
    CREATOR_KEY = 'creator'
    VERSION_KEY = 'version'
    CREATION_TIME_KEY = 'creation_time'
    STATION_KEY = 'station'
    DATE_KEY = 'date'
    EXTENSION = '.root'



if __name__ == '__main__':
    print E3RootFileBase.CREATION_TIME_KEY
