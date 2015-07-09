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


import random

from e3pipe.dst.E3Timestamp import E3Timestamp
from e3pipe.__logging__ import logger



class E3PoissonService:

    """ Class to generate arrival times from an underlying Poisson process.
    """

    def __init__(self, rate):
        """ Constructor.
        """
        logger.info('Inizializing Poisson service @ %.3f Hz' % rate)
        self.__Rate = rate
        self.__Timestamp = E3Timestamp(0, 0)

    def next(self):
        """ Generate the next arrival time.
        """
        dns = int(1000000000*random.expovariate(self.__Rate) + 0.5)
        self.__Timestamp += E3Timestamp(0, dns)
        return self.__Timestamp

    def seconds(self):
        """ Return the seconds from the start.
        """
        return self.__Timestamp.seconds()

    def nanoseconds(self):
        """ Return the nanoseconds from the start.
        """
        return self.__Timestamp.nanoseconds()



if __name__ == '__main__':
    svc = E3PoissonService(2.5)
    for i in range(10):
        print svc.next()
