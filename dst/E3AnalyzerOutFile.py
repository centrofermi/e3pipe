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
from e3pipe.config.__dst__ import MAX_GOOD_CHISQUARE



class E3AnalyzerOutFile(E3TextTupleBase):

    """ Class encapsulating a .out file from the analyizer.

    The main purpose of this class is to be able to iterate on a .out file
    getting out structured objects rather than text lines, e.g.
    """

    STATUS_CODE_GOOD = 0x0
    STATUS_CODE_NO_HITS = 0x1
    STATUS_CODE_NO_HIT = 0x10
    STATUS_CODE_MALFORMED = 0x100
    STATUS_CODE_UNDEFINED = 0x1000000

    def __init__(self, filePath):
        """ Constructor.
        
        Note we call the base class next() method once, right at the
        beginning, to skip the file header.
        """
        E3TextTupleBase.__init__(self, filePath, '.out')
        self.__CurrentLine = 1
        self.__LastGoodTimestamp = None
        self.__EventStat = {'total'    : 0, 
                            'hits'     : 0,
                            'track'    : 0,
                            'malformed': 0,
                            'no_hits'  : 0,
                            'no_hit'   : 0,
                            }
        file.next(self)

    def eventStat(self):
        """ Return the event statistics.
        """
        return self.__EventStat

    def next(self):
        """ Overloaded next() method.
        
        The parsing of this thing has become so complicated that we
        essentially give up on using the general machinery put in place
        with the E3TextTupleRow class. Here we just pass a plain dictionary
        out of the iterator to fill the output ROOT tree.
        """
        # Initialize the output dictionary with sensible default values.
        outputData = {'RunNumber'   : None,
                      'EventNumber' : None,
                      'StatusCode'  : self.STATUS_CODE_UNDEFINED,
                      'Seconds'     : 0,
                      'Nanoseconds' : 0,
                      'Microseconds': 0,
                      'XDir'        : -1.,
                      'YDir'        : -1.,
                      'ZDir'        : -1.,
                      'ChiSquare'   : -1.,
                      'TimeOfFlight': -99.,
                      'TrackLength' : -1.,
                      'DeltaTime'   : -1.
                  }
        data = file.next(self)
        self.__CurrentLine += 1
        self.__EventStat['total'] += 1
        # Does the line end with "no hits" (whatever that means)?
        if data.endswith('no hits\n'):
            self.__EventStat['no_hits'] += 1
            run, evt, dummy = data.split(None, 2)
            outputData['RunNumber'] = int(run)
            outputData['EventNumber'] = int(evt)
            outputData['StatusCode'] = self.STATUS_CODE_NO_HITS
            return outputData
        # Does the line end with "no hits" (whatever that means)?
        # Note that this is different wrt the previous case.
        if data.endswith('no hit\n'):
            self.__EventStat['no_hit'] += 1
            run, evt, dummy = data.split(None, 2)
            outputData['RunNumber'] = int(run)
            outputData['EventNumber'] = int(evt)
            outputData['StatusCode'] = self.STATUS_CODE_NO_HIT
            return outputData
        # At this point we try and parse the line as if it was normal.
        try:
            run, evt, sec, ns, us, xdir, ydir, zdir, chi2, tof,\
                length = data.split()
            run = int(run)
            evt = int(evt)
            sec = int(sec)
            ns = int(ns)
            us = int(us)
            xdir = float(xdir)
            ydir = float(ydir)
            zdir = float(zdir)
            chi2 = float(chi2)
            tof = float(tof)
            length = float(length)
        except Exception, e:
            logger.error('Line %d of %s file is malformed ("%s")' %\
                         (self.__CurrentLine, self.name, data.strip('\n')))
            logger.info('Exception: %s' % e)
            self.__EventStat['malformed'] += 1
            run, evt, dummy = data.split(None, 2)
            outputData['RunNumber'] = int(run)
            outputData['EventNumber'] = int(evt)
            outputData['StatusCode'] = self.STATUS_CODE_MALFORMED
            return outputData
        # And at this point we know that the event is good.
        self.__EventStat['hits'] += 1
        timestamp = sec + 1.e-9*ns
        outputData['RunNumber'] = run
        outputData['EventNumber'] = evt
        outputData['StatusCode'] = self.STATUS_CODE_GOOD
        outputData['Seconds'] = sec
        outputData['Nanoseconds'] = ns
        outputData['Microseconds'] = us
        outputData['XDir'] = xdir
        outputData['YDir'] = ydir
        outputData['ZDir'] = zdir
        outputData['ChiSquare'] = chi2
        outputData['TimeOfFlight'] = tof
        outputData['TrackLength'] = length
        # And if the chisquare is low enough, it even has tracks!
        if chi2 < MAX_GOOD_CHISQUARE:
            self.__EventStat['track'] += 1
        # Finally: update the delta event time.
        if self.__LastGoodTimestamp is not None:
            delta = timestamp - self.__LastGoodTimestamp
            outputData['DeltaTime'] = delta
        self.__LastGoodTimestamp = timestamp
        return outputData



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
