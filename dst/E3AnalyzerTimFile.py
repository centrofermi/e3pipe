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


from e3pipe.dst.E3TextTupleField import E3TextTupleField
from e3pipe.dst.E3TextTupleRow import E3TextTupleRow
from e3pipe.dst.E3TextTupleBase import E3TextTupleBase


class E3AnalyzerTimRow(E3TextTupleRow):
    
    """ Class encapsulating a row of a .out file from the analyzer.
    """

    FIELDS = [E3TextTupleField('RunNumber', int),
              E3TextTupleField('EventNumber', int),
              E3TextTupleField('Seconds', int, 's'),
              E3TextTupleField('Nanoseconds', int, 'ns')
          ]



class E3AnalyzerTimFile(E3TextTupleBase):

    """ Class encapsulating a .tim file from the analyizer.

    The main purpose of this class is to be able to iterate on a .out file
    getting out structured objects rather than text lines, e.g.
    """

    ROW_DESCRIPTOR = E3AnalyzerTimRow

    def __init__(self, filePath):
        """ Constructor.
        
        Note we call the base class next() method once, right at the
        beginning, to skip the file header.
        """
        E3TextTupleBase.__init__(self, filePath, '.tim')
        file.next(self)



def test(filePath, numEvents = 5):
    """ Test code.
    """
    f = E3AnalyzerTimFile(filePath)
    for i in range(numEvents):
        print f.next()



if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser()
    (opts, args) = parser.parse_args()
    for filePath in args:
        test(filePath)
