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


import os
import glob

from e3pipe.__logging__ import logger
from e3pipe.misc.E3FileCrawlerBase import E3FileCrawlerBase
from e3pipe.misc.E3RawFileCrawler import E3RawFileCrawler
from e3pipe.misc.E3DstFileCrawler import E3DstFileCrawler
from e3pipe.misc.E3LockFileCrawler import E3LockFileCrawler
from e3pipe.dst.__time__ import str2date, date2str


END_DATE = str2date('2014-11-14')
DAYS_SPANNED = 19
STATIONS = [
    'ALTA-01',
    'BARI-01',
    'BOLO-03',
    'CAGL-01',
    'CAGL-02',
    'CAGL-03',
    'CATA-02',
    'CATZ-01',
    'FRAS-02',
    'GROS-01',
    'LAQU-01',
    'LAQU-02',
    'LECC-01',
    'LECC-02',
    'LODI-01',
    'PISA-01',
    'SAVO-01',
    'SAVO-02',
    'TORI-04',
    'TRAP-01',
    'TRIN-01',
    'VIAR-01',
    'VIAR-02'
]



class E3RawFileCrawlerStat(E3RawFileCrawler):

    """
    """

    def __init__(self):
        """ Constructor.
        """
        self.__StatDict = {'num_files'  : 0,
                           'disk_space' : 0
                           }
        E3RawFileCrawler.__init__(self, STATIONS, END_DATE, DAYS_SPANNED)

    def crawlFolder(self, folderPath):
        """  Overloaded class method.
        """
        fileList = []
        for filePath in glob.glob(os.path.join(folderPath, '*.bin')):
            fileList.append(filePath)
            self.__StatDict['num_files'] += 1
            self.__StatDict['disk_space'] += os.stat(filePath).st_size
        return fileList

    def __str__(self):
        """
        """
        return '%s' % self.__StatDict



class E3DstFileCrawlerStat(E3FileCrawlerBase, E3DstFileCrawler):

    """
    """

    ROOT_FOLDER = '/recon'

    def __init__(self):
        """ Constructor.
        """
        self.__StatDict = {'num_files'  : 0,
                           'disk_space' : 0
                           }
        E3FileCrawlerBase.__init__(self, STATIONS, END_DATE, DAYS_SPANNED)

    def crawlFolder(self, folderPath):
        """  Overloaded class method.
        """
        fileList = []
        for filePath in glob.glob(os.path.join(folderPath, '*_dst.root')):
            fileList.append(filePath)
            self.__StatDict['num_files'] += 1
            self.__StatDict['disk_space'] += os.stat(filePath).st_size
        return fileList

    def __str__(self):
        """
        """
        return '%s' % self.__StatDict


class E3LockFileCrawlerStat(E3LockFileCrawler):

    """
    """

    ROOT_FOLDER = '/home/analisi/eeelock'

    def __init__(self):
        """ Constructor.
        """
        self.__StatDict = {'num_files'  : 0,
                           'status_code': {}
                           }
        E3LockFileCrawler.__init__(self, STATIONS, END_DATE, DAYS_SPANNED)

    def crawlFolder(self, folderPath):
        """  Overloaded class method.
        """
        fileList = []
        for filePath in glob.glob(os.path.join(folderPath, '*.lock')):
            fileList.append(filePath)
            self.__StatDict['num_files'] += 1
            sc = open(filePath).readline().strip('\n')
            try:
                self.__StatDict['status_code'][sc] += 1
            except KeyError:
                self.__StatDict['status_code'][sc] = 1
        return fileList

    def __str__(self):
        """
        """
        return '%s' % self.__StatDict




def e3stat():
    """
    """
    rawCrawler = E3RawFileCrawlerStat()
    dstCrawler = E3DstFileCrawlerStat()
    lockCrawler = E3LockFileCrawlerStat()
    logger.info('Raw data stat: %s' % rawCrawler)
    logger.info('DST file stat: %s' % dstCrawler)
    logger.info('Locked file stat: %s' % lockCrawler)


if __name__ == '__main__':
    e3stat()
