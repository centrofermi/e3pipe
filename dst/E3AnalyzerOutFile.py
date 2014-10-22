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
from e3pipe.__logging__ import logger


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
              E3TextTupleField('TimeOfFlight', float, -99., 'ns'),
              E3TextTupleField('TrackLength', float, -1., 'cm'),
              E3TextTupleField('DeltaTime', float, -1., 's')
          ]

    def timestamp(self):
        """ Return the event timestamp.
        """
        return self['Seconds'] + 1.e-9*self['Nanoseconds']



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
        self.__CurrentLine = 1
        self.__LastTimestamp = None
        self.__EventStat = {'total'    : 0, 
                            'good'     : 0,
                            'malformed': 0,
                            'no_hits'  : 0,
                            'no_hit'   : 0
                            }
        file.next(self)

    def eventStat(self):
        """ Return the event statistics.
        """
        return self.__EventStat

    def next(self):
        """ Overloaded next() method.
        
        Here is essentially a horrible hack to tell which events have no
        reconstructed track and therefore should have all the fields
        initialized to the default values.

        And we also add the delta event time :-)
        """
        data = file.next(self)
        self.__CurrentLine += 1
        self.__EventStat['total'] += 1
        # Is this a line with either "no hit" or "no hits".
        if self.NO_TRACK_MARKER in data:
            if data.endswith('no hits\n'):
                self.__EventStat['no_hits'] += 1
            if data.endswith('no hit\n'):
                self.__EventStat['no_hit'] += 1  
            data = data.split(self.NO_TRACK_MARKER)[0]
            for field in self.ROW_DESCRIPTOR.FIELDS[2:]:
                data += '  %s' % field.Default
            return self.ROW_DESCRIPTOR(data)
        # If no go ahead and try and parse it.
        try:
            data = self.ROW_DESCRIPTOR(data)
        except:
            logger.error('Line %d of %s file is malformed:\n->%s' %\
                             (self.__CurrentLine, self.name, data.strip('\n')))
            self.__EventStat['malformed'] += 1
            runId, evtId = data.split()[:2]
            data = '%s %s' % (runId, evtId)
            for field in self.ROW_DESCRIPTOR.FIELDS[2:]:
                data += '  %s' % field.Default
            return self.ROW_DESCRIPTOR(data)
        # The event looks good!
        self.__EventStat['good'] += 1
        timestamp = data.timestamp()
        if self.__LastTimestamp is None:
            deltaTime = -1.
        else:
            deltaTime = timestamp - self.__LastTimestamp
        data['DeltaTime'] = deltaTime
        self.__LastTimestamp = timestamp
        return data



def test(filePath, numEvents = 20):
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
