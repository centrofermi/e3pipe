#!/usr/bin/env python
# *********************************************************************
# * Copyright (C) 2015 Luca Baldini (luca.baldini@pi.infn.it)         *
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



class E3RunDbFileCrawlerBase:
    
    """ Base class for the db crawler.
    """

    def __init__(self, stations, startDate, endDate):
        """
        """
        self.__Stations = stations
        self.__StartDate = startDate
        self.__EndDate = endDate
        self.__FileList = []
        self.__FileDict = {}
        for station in stations:
            self.__FileDict[station] = []
        self.__Index = 0

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
        
    def addFilePath(self, station, filePath):
        """ Add a file path for a specific station.
        """
        if station not in self.__Stations:
            self.__Stations.append(station)
            self.__FileDict[station] = []
        self.__FileDict[station].append(filePath)
        self.__FileList.append(filePath)

    def __len__(self):
        """ Return the length of the underlying file list.
        """
        return len(self.__FileList)

    def stations(self):
        """ Return the list of stations.
        """
        return self.__Stations

    def startDate(self):
        """ Return the end date of the period of interest.
        """
        return self.__StartDate

    def endDate(self):
        """ Return the end date of the period of interest.
        """
        return self.__EndDate

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
