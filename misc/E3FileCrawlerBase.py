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
import glob
import os

from e3pipe.config.__stations__ import E3_ACTIVE_STATIONS
from e3pipe.dst.__time__ import date2str
from e3pipe.__logging__ import logger



class E3FileCrawlerBase:

    """ Base class for a file crawler.

    This provides the basic functionality to list all the files of a given
    type for a generic list of stations in a generic timespan, given the
    overall deirectory structure described in config/__storage__.py.

    In this context we're typically interested in crawling data folders
    back in time a fixed number of days starting from today, so these
    (the end date and the number of days spanned) are the two parameters that
    we pass to the constructor to define the time range. Note that an
    arbitrary time span
    """

    ROOT_FOLDER = ''

    def __init__(self, stations = None, endDate = None, daysSpanned = 2):
        """ Constructor.
        """
        self.__Stations = stations or E3_ACTIVE_STATIONS
        self.__EndDate = endDate or datetime.date.today()
        self.__DaysSpanned = daysSpanned
        self.__FileList = []
        self.__FileDict = {}
        self.__Index = 0
        self.__crawl()

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

    def __crawl(self):
        """ Crawl into the directory structure and fill the file list.

        Note that we don't do anything clever with the file list returned
        by the crawlFolder() method---i.e., if you want it to be sorted you
        should do it in the derived classes.
        """
        startDate = self.endDate() - datetime.timedelta(self.daysSpanned() - 1)
        logger.info('Data crawler started.')
        logger.info('Root directory: %s' % self.ROOT_FOLDER)
        logger.info('Time range: %s--%s' % (startDate, self.endDate()))
        dates = [startDate + datetime.timedelta(i) for \
                 i in range(self.daysSpanned())]
        for station in self.stations():
            self.__FileDict[station] = []
            logger.info('Searching for data products for station %s...' %\
                        station)
            for date in dates:
                folderPath = self.folderPath(station, date)
                logger.info('Crawling %s...' % folderPath)
                fileList = self.crawlFolder(folderPath)
                logger.info('%d file(s) found.' % len(fileList))
                self.__FileDict[station] += fileList
                self.__FileList += fileList

    def folderPath(self, station, date):
        """ Return the path to the data folder for a given station and date
        for the data products of interest.

        Note that this can be overloaded in derived classes.
        """
        return os.path.join(self.ROOT_FOLDER, station, date2str(date))

    def crawlFolder(self, folderPath):
        """ Do nothing hook to be overloaded in derived classes.

        This is supposed to return the list of files in a given folder,
        to be append to the basic data members.
        """
        return []
        
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
        text = 'Crawler file summary:\n'
        for station in self.stations():
            text += '%s: %d file(s)\n' %\
                    (station, len(self.__FileDict[station]))
        text += 'Total number of files: %d' % len(self.__FileList)
        return text



def test():
    """ Test program.
    """
    crawler = E3FileCrawlerBase()
    print crawler


if __name__ == '__main__':
    test()
