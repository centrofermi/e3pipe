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
from e3pipe.dst.E3Analyzer2ttFile import E3Analyzer2ttFile
from e3pipe.__logging__ import logger
from e3pipe.config.__dst__ import MAX_GOOD_CHISQUARE



class E3AnalyzerOutFile(E3TextTupleBase):

    """ Class encapsulating a .out file from the analyzer.

    The main purpose of this class is to be able to iterate on a .out file
    getting out structured objects rather than text lines, e.g.
    """

    STATUS_CODE_GOOD = 0x0
    STATUS_CODE_NO_HITS = 0x1
    STATUS_CODE_NO_HIT = 0x10
    STATUS_CODE_MALFORMED = 0x100
    STATUS_CODE_UNDEFINED = 0x1000000
    NON_PHYSICAL_FLOAT_VALUE = -999.

    def __init__(self, filePath, read2tt = True):
        """ Constructor.
        
        Note we call the base class next() method once, right at the
        beginning, to skip the file header.
        """
        E3TextTupleBase.__init__(self, filePath, '.out')
        self.__CurrentLine = 1
        self.__LastGoodTimestamp = None
        self.__EventStat = {'total'     : 0, 
                            'hits'      : 0,
                            'track'     : 0,
                            'two_tracks': 0,
                            'malformed' : 0,
                            'no_hits'   : 0,
                            'no_hit'    : 0,
                            'backward'  : 0
                            }
        self.__MinTimestamp = None
        self.__MaxTimestamp = None
        file.next(self)
        self.__Dict2T = {}
        if read2tt:
            f2tt = E3Analyzer2ttFile(filePath.replace('.out', '.2tt'))
            f2tt.fillEventDict()
            self.__Dict2T = f2tt.eventDict()
            f2tt.close()

    def eventStat(self):
        """ Return the event statistics.
        """
        return self.__EventStat

    def minTimestamp(self):
        """ Return the smallest timestamp found so far.
        """
        return self.__MinTimestamp

    def maxTimestamp(self):
        """ Return the largest timestamp found so far.
        """
        return self.__MaxTimestamp

    def next(self):
        """ Overloaded next() method.
        
        The parsing of this thing has become so complicated that we
        essentially give up on using the general machinery put in place
        with the E3TextTupleRow class. Here we just pass a plain dictionary
        out of the iterator to fill the output ROOT tree.
        """
        # Initialize the output dictionary with sensible default values.
        outputData = {'RunNumber'       : None,
                      'EventNumber'     : None,
                      'StatusCode'      : self.STATUS_CODE_UNDEFINED,
                      'Seconds'         : 0,
                      'Nanoseconds'     : 0,
                      'Microseconds'    : 0,
                      'PosXBot'         : self.NON_PHYSICAL_FLOAT_VALUE,
                      'PosYBot'         : self.NON_PHYSICAL_FLOAT_VALUE,
                      'TimeBot'         : self.NON_PHYSICAL_FLOAT_VALUE,
                      'PosXMid'         : self.NON_PHYSICAL_FLOAT_VALUE,
                      'PosYMid'         : self.NON_PHYSICAL_FLOAT_VALUE,
                      'TimeMid'         : self.NON_PHYSICAL_FLOAT_VALUE,
                      'PosXTop'         : self.NON_PHYSICAL_FLOAT_VALUE,
                      'PosYTop'         : self.NON_PHYSICAL_FLOAT_VALUE,
                      'TimeTop'         : self.NON_PHYSICAL_FLOAT_VALUE,
                      'IntersectXMid'   : self.NON_PHYSICAL_FLOAT_VALUE,
                      'IntersectYMid'   : self.NON_PHYSICAL_FLOAT_VALUE,
                      'IntersectZMid'   : self.NON_PHYSICAL_FLOAT_VALUE,
                      'XDir'            : self.NON_PHYSICAL_FLOAT_VALUE,
                      'YDir'            : self.NON_PHYSICAL_FLOAT_VALUE,
                      'ZDir'            : self.NON_PHYSICAL_FLOAT_VALUE,
                      'NumHitsBot'      : 0,
                      'NumHitsMid'      : 0,
                      'NumHitsTop'      : 0,
                      'NumClustersBot'  : 0,
                      'NumClustersMid'  : 0,
                      'NumClustersTop'  : 0,
                      'ChiSquare'       : self.NON_PHYSICAL_FLOAT_VALUE,
                      'TimeOfFlight'    : self.NON_PHYSICAL_FLOAT_VALUE,
                      'TrackLength'     : self.NON_PHYSICAL_FLOAT_VALUE,
                      'DeltaTime'       : self.NON_PHYSICAL_FLOAT_VALUE,
                      'PosXBot2T'       : self.NON_PHYSICAL_FLOAT_VALUE,
                      'PosYBot2T'       : self.NON_PHYSICAL_FLOAT_VALUE,
                      'TimeBot2T'       : self.NON_PHYSICAL_FLOAT_VALUE,
                      'PosXMid2T'       : self.NON_PHYSICAL_FLOAT_VALUE,
                      'PosYMid2T'       : self.NON_PHYSICAL_FLOAT_VALUE,
                      'TimeMid2T'       : self.NON_PHYSICAL_FLOAT_VALUE,
                      'PosXTop2T'       : self.NON_PHYSICAL_FLOAT_VALUE,
                      'PosYTop2T'       : self.NON_PHYSICAL_FLOAT_VALUE,
                      'TimeTop2T'       : self.NON_PHYSICAL_FLOAT_VALUE,
                      'IntersectXMid2T' : self.NON_PHYSICAL_FLOAT_VALUE,
                      'IntersectYMid2T' : self.NON_PHYSICAL_FLOAT_VALUE,
                      'IntersectZMid2T' : self.NON_PHYSICAL_FLOAT_VALUE,
                      'XDir2T'          : self.NON_PHYSICAL_FLOAT_VALUE,
                      'YDir2T'          : self.NON_PHYSICAL_FLOAT_VALUE,
                      'ZDir2T'          : self.NON_PHYSICAL_FLOAT_VALUE,
                      'ChiSquare2T'     : self.NON_PHYSICAL_FLOAT_VALUE,
                      'TimeOfFlight2T'  : self.NON_PHYSICAL_FLOAT_VALUE,
                      'TrackLength2T'   : self.NON_PHYSICAL_FLOAT_VALUE
                  }
        data = file.next(self)
        self.__CurrentLine += 1
        self.__EventStat['total'] += 1
        # Does the line end with "no physical hits" (whatever that means)?
        # Note that this used to be "no hits". We are assuming that the
        # current "no physical hits" is just the equivalent of such old label.
        if data.endswith('no physical hits\n'):
            self.__EventStat['no_hits'] += 1
            run, evt, dummy = data.split(None, 2)
            outputData['RunNumber'] = int(run)
            outputData['EventNumber'] = int(evt)
            outputData['StatusCode'] = self.STATUS_CODE_NO_HITS
            return outputData
        # Does the line end with "no hit" (whatever that means)?
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
            run, evt, sec, ns, us, xbot, ybot, tbot, xmid, ymid, tmid, xtop,\
                ytop, ttop, intxmid, intymid, intzmid, xdir, ydir, zdir,\
                nhitbot, nhitmid, nhittop, nclubot, nclumid, nclutop, chi2,\
                tof, length = data.split()
            run = int(run)
            evt = int(evt)
            sec = int(sec)
            ns = int(ns)
            us = int(us)
            xbot = float(xbot)
            ybot = float(ybot)
            tbot = float(tbot)
            xmid = float(xmid)
            ymid = float(ymid)
            tmid = float(tmid)
            xtop = float(xtop)
            ytop = float(ytop)
            ttop = float(ttop)
            intxmid = float(intxmid)
            intymid = float(intymid)
            intzmid = float(intzmid)
            xdir = float(xdir)
            ydir = float(ydir)
            zdir = float(zdir)
            nhitbot = int(nhitbot)
            nhitmid = int(nhitmid)
            nhittop = int(nhittop)
            nclubot = int(nclubot)
            nclumid = int(nclumid)
            nclutop = int(nclutop)
            chi2 = float(chi2)
            tof = float(tof)
            length = float(length)
        except Exception, e:
            # I removed the following lines as, for some reason, they were
            # really hurting our capability of processing runs in batch for
            # runs with a massive fraction of malformed events.
            #
            # Think twice before putting it back.
            #
            #logger.error('Line %d of %s file is malformed ("%s")' %\
            #             (self.__CurrentLine, self.name, data.strip('\n')))
            #logger.info('Exception: %s' % e)
            self.__EventStat['malformed'] += 1
            run, evt, dummy = data.split(None, 2)
            outputData['RunNumber'] = int(run)
            outputData['EventNumber'] = int(evt)
            outputData['StatusCode'] = self.STATUS_CODE_MALFORMED
            return outputData
        # And at this point we know that the event is good.
        self.__EventStat['hits'] += 1
        timestamp = sec + 1.e-9*ns
        # We keep track of the minimum and maximum timestamp in the
        # file here, as if the events are not time ordered it would
        # essentially be necessary to loop over the entire file one more
        # time.
        if self.__MinTimestamp is None or timestamp < self.__MinTimestamp:
            self.__MinTimestamp = timestamp
        if self.__MaxTimestamp is None or timestamp > self.__MaxTimestamp:
            self.__MaxTimestamp = timestamp
        outputData['RunNumber'] = run
        outputData['EventNumber'] = evt
        outputData['StatusCode'] = self.STATUS_CODE_GOOD
        outputData['Seconds'] = sec
        outputData['Nanoseconds'] = ns
        outputData['Microseconds'] = us
        outputData['PosXBot'] = xbot
        outputData['PosYBot'] = ybot
        outputData['TimeBot'] = tbot
        outputData['PosXMid'] = xmid
        outputData['PosYMid'] = ymid
        outputData['TimeMid'] = tmid
        outputData['PosXTop'] = xtop
        outputData['PosYTop'] = ytop
        outputData['TimeTop'] = ttop
        outputData['IntersectXMid'] = intxmid
        outputData['IntersectYMid'] = intymid
        outputData['IntersectZMid'] = intzmid
        outputData['XDir'] = xdir
        outputData['YDir'] = ydir
        outputData['ZDir'] = zdir
        outputData['NumHitsBot'] = nhitbot
        outputData['NumHitsMid'] = nhitmid
        outputData['NumHitsTop'] = nhittop
        outputData['NumClustersBot'] = nclubot
        outputData['NumClustersMid'] = nclumid
        outputData['NumClustersTop'] = nclutop
        outputData['ChiSquare'] = chi2
        outputData['TimeOfFlight'] = tof
        outputData['TrackLength'] = length
        # Do we have two tracks?
        if self.__Dict2T.has_key(evt):
            info2t = self.__Dict2T[evt]
            for key, value in info2t.items():
                outputData[key] = value
            if info2t['ChiSquare2T'] < MAX_GOOD_CHISQUARE:
                self.__EventStat['two_tracks'] += 1
        # And if the chisquare is low enough, it even has tracks!
        if chi2 < MAX_GOOD_CHISQUARE:
            self.__EventStat['track'] += 1
        # Finally: update the delta event time.
        if self.__LastGoodTimestamp is not None:
            delta = timestamp - self.__LastGoodTimestamp
            if delta < 0:
                self.__EventStat['backward'] += 1
            outputData['DeltaTime'] = delta
        self.__LastGoodTimestamp = timestamp
        return outputData



def test(filePath, numEvents = 20):
    """ Test code.
    """
    f = E3AnalyzerOutFile(filePath)
    for i in range(numEvents):
        print f.next()
    print f.eventStat()



if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser()
    (opts, args) = parser.parse_args()
    for filePath in args:
        test(filePath)
