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


class E3Timestamp:

    """ Basic timestamp class.
    """

    def __init__(self, seconds, nanoseconds):
        """ Constructor.
        """        
        self.__Seconds = int(seconds)
        self.__Nanoseconds = int(nanoseconds)
        # Enforce sign matching between seconds and nanoseconds.
        if self.__Seconds < 0 and self.__Nanoseconds > 0:
            self.__Nanoseconds = -self.__Nanoseconds
        # Take into account possible overflows of the ns counter.
        if abs(self.__Nanoseconds) > 999999999:
            self.__Seconds += self.__Nanoseconds / 1000000000
            self.__Nanoseconds = self.__Nanoseconds % 1000000000

    def seconds(self):
        """
        """
        return self.__Seconds

    def nanoseconds(self):
        """
        """
        return self.__Nanoseconds

    def __float__(self):
        """ Cast to float.
        """
        return self.__Seconds + 1.e-9*self.__Nanoseconds

    def __add__(self, other):
        """ Add timestamps.
        """
        seconds = self.seconds() + other.seconds()
        nanoseconds = self.nanoseconds() + other.nanoseconds()
        # Check for overflow in the nanoseconds field.
        if nanoseconds >= 1000000000:
            nanoseconds -= 1000000000
            seconds += 1
        # And we still have to enforce the sign matching between seconds and
        # nanoseconds.
        if seconds < 0 and nanoseconds > 0:
            seconds += 1
            nanoseconds -= 1000000000
        elif seconds > 0 and nanoseconds < 0:
            seconds -= 1
            nanoseconds += 1000000000
        return E3Timestamp(seconds, nanoseconds)

    def __sub__(self, other):
        """
        """
        seconds = self.seconds() - other.seconds()
        nanoseconds = self.nanoseconds() - other.nanoseconds()
        # Check for underflow in the m_nanoseconds field.
        if nanoseconds <= -1000000000:
            nanoseconds += 1000000000
            seconds -= 1
        # And we still have to enforce the sign matching between seconds and
        # nanoseconds.
        if seconds < 0 and nanoseconds > 0:
            seconds += 1
            nanoseconds -= 1000000000
        elif seconds > 0 and nanoseconds < 0:
            seconds -= 1
            nanoseconds += 1000000000
        return E3Timestamp(seconds, nanoseconds)

    def __cmp__(self, other):
        """ Comparison operator.
        """
        if self.seconds() < other.seconds():
            return 1
        elif self.seconds() > other.seconds():
            return -1
        else:
            return self.nanoseconds() - other.nanoseconds()

    def __str__(self):
        """ String formatting.
        """
        text = '%d[s].' % self.seconds()
        if self.nanoseconds() == 0:
            text += '+000000000'
        elif self.nanoseconds() > 0:
            text += '+%s' % ('%d' % abs(self.nanoseconds())).zfill(9)
        else:
            text += '-%s' % ('%d' % abs(self.nanoseconds())).zfill(9)
        text += '[ns] (%.9f)' % self
        return text



def test():
    """
    """
    t1 = E3Timestamp(1, 800000000)
    t2 = E3Timestamp(1, 100000000)
    t3 = E3Timestamp(7, 7764)
    t4 = E3Timestamp(-7, 7764)
    print t1
    print t2
    print t1 + t2
    print t1 - t2
    print t2 - t1
    print t3
    print t4
    print t1 > t2, t1 == t2, t1 < t2, t1 == t1

if __name__ == '__main__':
    test()

