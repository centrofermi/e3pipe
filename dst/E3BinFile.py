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


import struct

from e3pipe.__logging__ import logger
from e3pipe.dst.E3WeatherStationRecord import E3WeatherStationRecord
from e3pipe.dst.E3GeometryRecord import E3GeometryRecord
from e3pipe.dst.E3GpsRecord import E3GpsRecord



class E3BinFile(file):
    
    """ Small class wrapping the EEE binary file structure.
    """

    HEADER_EEE_1 = 1162167584
    HEADER_EEE_2 = 1147237473
    HEADER_GPS_RECORD  = 0 # GPS.
    HEADER_TDC1_RECORD = 1 # TDC 1.
    HEADER_TDC2_RECORD = 2 # TDC 2.
    HEADER_SOR_RECORD  = 3 # Start of Run.
    HEADER_GEO_RECORD  = 5 # Geometry.
    HEADRE_WAD_RECORD  = 6 # Window and delay. 
    HEADER_VWS_RECORD  = 7 # Virtual Weather Station.

    def __init__(self, filePath, maxRecords = 4):
        """ Constructor.
        """
        self.__WeatherStationRecord = None
        self.__GeometryRecord = None
        logger.info('Opening input binary file %s...' % filePath)
        file.__init__(self, filePath, 'rb')
        self.__LastByteRead = None
        self.readWord(self.HEADER_EEE_1)
        self.readWord(self.HEADER_EEE_2)
        for i in xrange(maxRecords):
            try:
                blockType, blockSize, data = self.readBlock()
            except:
                logger.error('Could not parse file content, giving up.')
                break
            if blockType == self.HEADER_GEO_RECORD:
                self.__GeometryRecord = E3GeometryRecord(*data)
                logger.info('Geometry record found!')
                logger.info(self.__GeometryRecord)
            elif blockType == self.HEADER_GPS_RECORD:
                print data
            elif blockType == self.HEADER_VWS_RECORD:
                self.__WeatherStationRecord = E3WeatherStationRecord(*data)
                logger.info('Weather station record found!')
                logger.info(self.__WeatherStationRecord)
                break
        if self.__WeatherStationRecord is None:
            logger.info('Could not find any weather station record.')

    def weatherStationRecord(self):
        """
        """
        return self.__WeatherStationRecord

    def geometryRecord(self):
        """
        """
        return self.__GeometryRecord

    def scanGPS(self, maxRecords = 10):
        """
        """
        numRecords = 0
        while numRecords < maxRecords:
            try:
                blockType, blockSize, data = self.readBlock()
            except:
                logger.error('Could not parse file content, giving up.')
                break
            if blockType == self.HEADER_GPS_RECORD:
                print numRecords, E3GpsRecord(*data)
                numRecords += 1

    def readWord(self, expected = None):
        """ Read a byte from the binary file.

        If the expected argument is not None, the value which is read out is
        checked against that.
        """
        self.__LastByteRead = struct.unpack('i', self.read(4))[0]
        if expected is not None and self.__LastByteRead != expected:
            logger.error('Data mismatch (expected %d, found %d)' %\
                         (expected, self.__LastByteRead))
        return self.__LastByteRead

    def readBlock(self):
        """ Read a block from the binary file.
        """
        blockSize = self.readWord()
        blockType = self.readWord()
        data = [self.readWord() for i in xrange(blockSize - 2)]
        return blockType, blockSize, data



def test(filePath):
    """ Test program.
    """
    f = E3BinFile(filePath)
    record = f.weatherStationRecord()
    f.scanGPS()



if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser()
    (opts, args) = parser.parse_args()
    for filePath in args:
        test(filePath)
