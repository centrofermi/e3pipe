#!/usr/bin/env python
# *********************************************************************
# * Copyright (C) 2014 Luca Baldini (luca.baldini@pi.infn.it)         *
# *                                                                   *
# * For the license terms see the file LICENCE, distributed           *
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


import time


class E3Chrono:

    """ Small utility class to benchmark applications.
    """
    
    def __init__(self):
        """ Constructor.

        Note the chronometer is automatically started at creation time.
        """
        self.__LastTimestamp = None
        self.start()

    def start(self):
        """ Start the chronometer.
        """
        self.__LastTimestamp = time.time()

    def stop(self):
        """ Stop the chronometer and return the elapsed time.
        """
        if self.__LastTimestamp is None:
            return None
        elpsedTime = time.time() - self.__LastTimestamp
        self.__LastTimestamp = None
        return elpsedTime
