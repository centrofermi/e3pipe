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


class E3BinFile(file):
    
    """
    """

    HEADER_EEE_1 = 1162167584
    HEADER_EEE_2 = 1147237473
    HEADER_WS_RECORD = 7
    HEADER_TDC_1 = 1
    HEADER_TDC_2 = 2

    def __init__(self, filePath, maxRecords = 50):
        """ Constructor.
        """
        self.__WeatherStationRecord = None
        logger.info('Opening input binary file %s...' % filePath)
        file.__init__(self, filePath, 'rb')
        self.readByte()
        self.readByte()
        for i in xrange(maxRecords):
            try:
                blockType, blockSize, data = self.readBlock()
            except:
                logger.error('Could not parse file content, giving up.')
                break
            if blockType == self.HEADER_WS_RECORD:
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

    def readByte(self):
        """ Read a byte from the binary file.
        """
        return struct.unpack('i', self.read(4))[0]

    def readBlock(self):
        """ Read a block from the binary file.
        """
        blockSize = self.readByte()
        blockType = self.readByte()
        data = [self.readByte() for i in xrange(blockSize - 2)]
        return blockType, blockSize, data



def test(filePath):
    """ Test program.
    """
    f = E3BinFile(filePath)
    record = f.weatherStationRecord()
    if record is not None:
        print record.seconds()



if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser()
    (opts, args) = parser.parse_args()
    for filePath in args:
        test(filePath)
