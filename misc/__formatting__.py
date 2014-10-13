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


import types
import math


def formatFloat(number):
    """ Format a floating point number with a reasonable number of
    decimal places.
    """
    try:
        if int(number) == number:
            return '%d' % int(number)
    except OverflowError:
        pass
    if abs(number) > 0.001 and abs(number) < 100:
        try:
	    numDecFigures = int(3 - math.log10(abs(number)))
        except:
	    numDecFigures = 3	
	formatString = '%' + '.%df' % numDecFigures
        return formatString % number
    elif abs(number) >= 100 and number < 10000:
        return '%.1f' % number
    else:
        return '%.2e' % number

def formatNumber(number):
    """ Generic formatting function for numbers.
    """
    if number == 0:
        return '0'
    elif type(number) == types.IntType:
        return '%d' % number
    elif type(number) == types.FloatType:
        return formatFloat(number)
    else:
        try:
            return formatFloat(float(number))
        except:
            return number



if __name__ == '__main__':
    print formatFloat(36.7413853085702)
    print formatNumber(2)
    print formatNumber(2.001)
