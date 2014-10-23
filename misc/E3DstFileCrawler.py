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


import glob
import os


from e3pipe.misc.E3FileCrawlerBase import E3FileCrawlerBase
from e3pipe.config.__storage__ import E3PIPE_RECON_BASE
from e3pipe.dst.__time__ import date2str
from e3pipe.__logging__ import logger



class E3DstFileCrawler(E3FileCrawlerBase):

    """ Overloaded crawler class for the raw data.
    """
    
    ROOT_FOLDER = E3PIPE_RECON_BASE

    def __init__(self, station, endDate = None, daysSpanned = 1):
        """ Constructor.
        """
        E3FileCrawlerBase.__init__(self, [station], endDate, daysSpanned)

    def crawlFolder(self, folderPath):
        """ Overloaded methos.
        """
        fileList = glob.glob(os.path.join(folderPath, '*_dst.root'))
        fileList.sort()
        return fileList



def test():
    """ Test program.
    """
    crawler = E3DstFileCrawler('BARI-01')
    print crawler
    numFiles = len(crawler)
    curFile = 1
    for filePath in crawler:
        print 'File %d/%d: %s' % (curFile, numFiles, filePath)
        curFile += 1 


if __name__ == '__main__':
    test()

