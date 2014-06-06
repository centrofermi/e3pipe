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



class E3AnalyzerEventField:

    """ Small utility class describing an "atomic" field in an actual event,
    as contained in the .out file produced by the analyzer.

    This encapsulates things such as the field name (e.g., the run number and
    the event number), type (e.g., int or float) and the measurement units,
    if available.
    """

    def __init__(self, fieldName, fieldType, units = None):
        """
        """
        self.Name = fieldName
        self.Type = fieldType
        self.Units = units
        


class E3AnalyzerEvent(dict):

    """ Basic data structure encapsulating a DST event.

    There is a one-to-one correspondence between this data structure and one
    line in the .out file produced by the EEE analyzer, which is captured in
    the FIELDS data member below.

    This container is implemented as a dictionary as we will typically access
    the event properties by name, e.g., when converting the thing into a ROOT
    tree. However, we do provide facilities to represent an event as an ordered
    list of values as well.
    """

    FIELDS = [E3AnalyzerEventField('RunNumber', int),
              E3AnalyzerEventField('EventNumber', int),
              E3AnalyzerEventField('Seconds', int),
              E3AnalyzerEventField('Nanoseconds', int),
              E3AnalyzerEventField('Microseconds', int),
              E3AnalyzerEventField('XDir', float),
              E3AnalyzerEventField('YDir', float),
              E3AnalyzerEventField('ZDir', float),
              E3AnalyzerEventField('ChiSquare', float),
              E3AnalyzerEventField('TimeOfFlight', float, 'ns'),
              E3AnalyzerEventField('TrackLengths', float, 'cm')
          ]

    def __init__(self, data):
        """ Constructor.

        This essentially tranforms a line from a .out file into a fully-fledged
        E3Event object.
        """
        dict.__init__(self)
        for field, datum in zip(self.FIELDS, data.split()):
            self[field.Name] = field.Type(datum)
    
    def values(self):
        """ Return an ordered list of the field values.

        Note the order is dictated by the FIELD class member.
        """
        return [self[field.Name] for field in self.FIELDS]




def test():
    """ Test code.

    The data are taken from an actual .out file.
    """
    data = '     1          0  231408003    4193514         4193   0.37030   0.09268   0.92428  2.78417     -2.900      95.21'
    e = E3AnalyzerEvent(data)
    print(e)
    print(e.values())



if __name__ == '__main__':
    test()
