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
import decimal


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

def float_to_decimal(f):
    """
    Convert a floating point number to a Decimal with no loss of information

    This is essentially a nuisance in order to be able to deal with
    python 2.6 on the CNAF machine and is taken from:
    https://docs.python.org/release/2.6.7/library/decimal.html#decimal-faq
    """
    n, d = f.as_integer_ratio()
    numerator, denominator = decimal.Decimal(n), decimal.Decimal(d)
    ctx = decimal.Context(prec=60)
    result = ctx.divide(numerator, denominator)
    while ctx.flags[decimal.Inexact]:
        ctx.flags[decimal.Inexact] = False
        ctx.prec *= 2
        result = ctx.divide(numerator, denominator)
    return result

def formatValErr(value, error):
    """ Format a value/error pair.

    From http://code.activestate.com/lists/python-list/616578/
    """
    value = float_to_decimal(value)
    error = float_to_decimal(error)
    scale = error.adjusted()
    scale += error.scaleb(-scale).to_integral().adjusted()
    scale -= 1
    quant = decimal.Decimal('1e%d' % scale)
    value = value.quantize(quant)
    error = error.quantize(quant)
    return '%s +- %s' % (value, error)



if __name__ == '__main__':
    print formatFloat(36.7413853085702)
    print formatNumber(2)
    print formatNumber(2.001)
    print formatValErr(3.638738276, 0.08557687)
    print formatValErr(33623287.864298, 74587.7)
