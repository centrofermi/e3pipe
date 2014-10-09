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


from e3pipe.dst.E3TextTupleField import E3TextTupleField
from e3pipe.dst.E3TextTupleRow import E3TextTupleRow
from e3pipe.dst.E3TextTupleBase import E3TextTupleBase


class E3AnalyzerOutRow(E3TextTupleRow):
    
    """ Class encapsulating a row of a .out file from the analyzer.
    """

    FIELDS = [E3TextTupleField('RunNumber', int),
              E3TextTupleField('EventNumber', int),
              E3TextTupleField('Seconds', int, 0, 's'),
              E3TextTupleField('Nanoseconds', int, 0, 'ns'),
              E3TextTupleField('Microseconds', int, 0, 'us'),
              E3TextTupleField('XDir', float, -1.),
              E3TextTupleField('YDir', float, -1.),
              E3TextTupleField('ZDir', float, -1.),
              E3TextTupleField('ChiSquare', float, -1.),
              E3TextTupleField('TimeOfFlight', float, -1., 'ns'),
              E3TextTupleField('TrackLength', float, -1., 'cm')
          ]



class E3AnalyzerOutFile(E3TextTupleBase):

    """ Class encapsulating a .out file from the analyizer.

    The main purpose of this class is to be able to iterate on a .out file
    getting out structured objects rather than text lines, e.g.
    """

    ROW_DESCRIPTOR = E3AnalyzerOutRow
    NO_TRACK_MARKER = 'no hit'

    def __init__(self, filePath):
        """ Constructor.
        
        Note we call the base class next() method once, right at the
        beginning, to skip the file header.
        """
        E3TextTupleBase.__init__(self, filePath, '.out')
        file.next(self)

    def next(self):
        """ Overloaded next() method.
        
        Here is essentially a horrible hack to tell which events have no
        reconstructed track and therefore should have all the fields
        initialized to the default values.
        """
        data = file.next(self)
        if self.NO_TRACK_MARKER in data:
            data = data.split(self.NO_TRACK_MARKER)[0]
            for field in self.ROW_DESCRIPTOR.FIELDS[2:]:
                data += '  %s' % field.Default
        return self.ROW_DESCRIPTOR(data)



def test(filePath, numEvents = 5):
    """ Test code.
    """
    f = E3AnalyzerOutFile(filePath)
    for i in range(numEvents):
        print f.next()



if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser()
    (opts, args) = parser.parse_args()
    for filePath in args:
        test(filePath)
