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


import datetime

from e3pipe.config.__storage__ import binFilePath
from e3pipe.db.E3RunDbInterface import E3RunDbInterface



class E3RunDbRawFileCrawler:
    
    """
    """

    def __init__(self, endDate = None, daysSpanned = 2, minSize = 0,
                 blackList = None, overwrite = False):
        """
        """
        self.__Stations = []
        self.__EndDate = endDate or datetime.date.today()
        self.__DaysSpanned = daysSpanned
        self.__MinSize = minSize
        self.__BlackList = blackList or []
        self.__FileList = []
        self.__FileDict = {}
        self.__Index = 0
        db = E3RunDbInterface()
        query = 'SELECT station_name,run_date,run_id from runs WHERE run_date BETWEEN DATE_SUB("%s", INTERVAL %d DAY) AND "%s" AND bin_file_size > %d' % (self.__EndDate, self.__DaysSpanned, self.__EndDate, self.__MinSize)
        if not overwrite:
            query += ' AND processing_status_code IS NULL'
        query += ';'
        db.execute(query, commit = False)
        for station, date, runId in db.fetchall():
            if station not in self.__BlackList:
                if station not in self.__Stations:
                    self.__Stations.append(station)
                    self.__FileDict[station] = []
                filePath = binFilePath(station, date, runId)
                self.__FileDict[station].append(filePath)
                self.__FileList.append(filePath)
        db.close()

    def __iter__(self):
        """ Overloaded methos to make the object iterable.
        """
        return self

    def next(self):
        """ Iterator next() method.
        """
        try:
            filePath = self.__FileList[self.__Index]
            self.__Index += 1
            return filePath
        except IndexError:
            raise StopIteration()

    def __len__(self):
        """ Return the length of the underlying file list.
        """
        return len(self.__FileList)

    def stations(self):
        """ Return the list of stations.
        """
        return self.__Stations

    def endDate(self):
        """ Return the end date of the period of interest.
        """
        return self.__EndDate

    def daysSpanned(self):
        """ Return the length of the period of interest in days.
        """
        return self.__DaysSpanned

    def fileDict(self):
        """ Return the file dict, i.e., a dictionary of file lists indexed
        by station.
        """
        return self.__FileDict

    def fileList(self):
        """ Return the complete file list.
        """
        return self.__FileList

    def __str__(self):
        """ String formatting.
        """
        text = 'DbCrawler file summary:\n'
        for station in self.stations():
            text += '%s: %d file(s)\n' %\
                    (station, len(self.__FileDict[station]))
        text += 'Total number of files: %d' % len(self.__FileList)
        return text



def test():
    """ Test program.
    """
    crawler = E3RunDbRawFileCrawler(daysSpanned = 1,
                                    blackList = ['FRAS-03'])
    print crawler
  

  
if __name__ == '__main__':
    test()
