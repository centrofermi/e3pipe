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


from e3pipe.dst.E3TextTupleBase import E3TextTupleBase
from e3pipe.__logging__ import logger



class E3Analyzer2ttFile(E3TextTupleBase):

    """ Class encapsulating a .out file from the analyizer.

    The main purpose of this class is to be able to iterate on a .2tt file
    getting out structured objects rather than text lines.

    [0] run_number
    [1] event_number
    [2] secs_since_1.1.2007
    [3] nanosecs
    [4] microseconds_since_start_of_run
    //track1
    [5] posX_Bottom
    [6] posY_Bottom
    [7] time_Bottom
    [8] posX_Middle
    [9] posY_Middle
    [10] time_Middle
    [11] posX_Top
    [12] posY_Top
    [13] time_Top
    [14] intersect_middle_X
    [15] intersect_middle_Y
    [16] intersect_middle_Z
    [17] unit_vector_x
    [18] unit_vector_y
    [19] unit_vector_z
    [20] chi_squared
    [21] time of flight[ns]
    [22] track length[cm]
    //track2
    [23] posX_Bottom
    [24] posY_Bottom
    [25] time_Bottom
    [26] posX_Middle
    [27] posY_Middle
    [28] time_Middle
    [29] posX_Top
    [30] posY_Top
    [31] time_Top
    [32] intersect_middle_X
    [33] intersect_middle_Y
    [34] intersect_middle_Z
    [35] unit_vector_x
    [36] unit_vector_y
    [37] unit_vector_z
    [38] chi_squared
    [39] time of flight[ns]
    [40] track length[cm]
    [41] hitted_Strips_Bottom
    [42] hitted_Strips_Middle
    [43] hitted_Strips_Top
    [44] clusters_Bottom
    [45] clusters_Middle
    [46] clusters_Top
    """

    NON_PHYSICAL_FLOAT_VALUE = -999.

    def __init__(self, filePath):
        """ Constructor.
        
        Note we call the base class next() method once, right at the
        beginning, to skip the file header.
        """
        E3TextTupleBase.__init__(self, filePath, '.2tt')
        file.next(self)
        self.__EventDict = {}

    def next(self):
        """ Overloaded next() method.
        """
        outputData = {'EventNumber'     : None,
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
        data = data.split()
        evt = int(data[1])
        outputData['EventNumber'] = evt
        try:
            xdir2t = float(data[37])
            ydir2t = float(data[38])
            zdir2t = float(data[39])
            chi22t = float(data[40])
            tof2t = float(data[41])
            length2t = float(data[42])
        except:
            return outputData
        outputData['XDir2T'] = xdir2t
        outputData['YDir2T'] = ydir2t
        outputData['ZDir2T'] = zdir2t
        outputData['ChiSquare2T'] = chi22t
        outputData['TimeOfFlight2T'] = tof2t
        outputData['TrackLength2T'] = length2t
        return outputData

    def fillEventDict(self):
        """ Fill a dictionary with the information about the second tracks.
        """
        logger.info('Parsing .2tt file and filling the event dict...')
        for event in self:
            self.__EventDict[event['EventNumber']] = event
        logger.info('Done, %d event(s) with two tracks found.' %\
                    len(self.__EventDict))

    def eventDict(self):
        """
        """
        return self.__EventDict

    def hasEvent(self, eventNumber):
        """
        """
        return self.__EventDict.has_key(eventNumber)

    def event(self, eventNumber):
        """
        """
        try:
            return self.__EventDict[eventNumber]
        except KeyError:
            return None



def test(filePath, numEvents = 100):
    """ Test code.
    """
    f = E3Analyzer2ttFile(filePath)
    f.fillEventDict()
    for i in range(numEvents):
        evt = f.event(i)
        if evt is not None:
            print i, evt



if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser()
    (opts, args) = parser.parse_args()
    for filePath in args:
        test(filePath)
