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



"""
An outline of the directory layout for our data storage is at:
https://github.com/centrofermi/e3pipe/wiki/Basic-data-directory-structure

In this package we implement that very same layout.

Note that we do provide a mechanism to override each of the base folders
via environmental variables.
"""


import os
import time
import datetime
import copy

import e3pipe.__utils__ as __utils__

from e3pipe.__logging__ import logger, abort


""" Base folder for the raw data.
"""
try:
    E3PIPE_RAW_BASE = os.environ['E3PIPE_RAW_BASE']
except KeyError:
    E3PIPE_RAW_BASE = '/data'

""" Base folder for the output DST ROOT files.
"""
try:
    E3PIPE_RECON_BASE = os.environ['E3PIPE_RECON_BASE']
except KeyError:
    E3PIPE_RECON_BASE = '/recon'

""" Base folder for the eee_calib.txt files.
"""
try:
    E3PIPE_CALIB_BASE = os.environ['E3PIPE_CALIB_BASE']
except KeyError:
    E3PIPE_CALIB_BASE = '/calib'

""" Base folder for the output dqm folders.
"""
try:
    E3PIPE_DQM_BASE = os.environ['E3PIPE_DQM_BASE']
except KeyError:
    E3PIPE_DQM_BASE = '/dqm'

""" Base folder for the log files.
"""
try:
    E3PIPE_LOG_BASE = os.environ['E3PIPE_LOG_BASE']
except KeyError:
    E3PIPE_LOG_BASE = '/log'

""" Temporary folder we run the reconstruction in.

Note this is user-specific, and we do cleanup the folder after the
reconstruction has run.

We also do create the folder on the fly (if it does not exists) when
the module is imported.
"""
try:
    E3PIPE_TEMP = os.environ['E3PIPE_TEMP']
except KeyError:
    E3PIPE_TEMP = os.path.expanduser(os.path.join('~', 'eeetmp'))
__utils__.createFolder(E3PIPE_TEMP)

def cleanupTemp():
    """ Cleanup the temp folder.
    """
    __utils__.cleanup(E3PIPE_TEMP)

def listTemp():
    """ List the content of the temp folder.
    """
    logger.info('Content of %s: %s' % (E3PIPE_TEMP, os.listdir(E3PIPE_TEMP)))


""" Base folder on the centrofermi server to make the output of the dqm
public.
"""
E3PIPE_DQM_PUB_BASE = 'www.centrofermi.it:/var/www/html_eee/dqm/'



class E3RawDataInfo(dict):

    """ Small utility class to encapsulate the information about a
    binary (.bin) data file.

    The basic assumptions that go into the pasring of the file path is
    that the file name is written in the form:
    station-year-month-day-run.bin
    (mind that the station name generally contains a "-" and we split the
    file name in 5 pieces starting from the right).

    The underlying data structure is a python dictionary, but we do
    overload the __getattr__() class method so that we provide the
    possibility of retrieving property by, e.g.,
    >>> info.year
    in addition to
    >>> info['year']
    """

    def __init__(self, filePath):
        """ Constructor.
        """
        if not filePath.endswith('.bin'):
            abort('%s does not look like a raw binary file' % filePath)
        dict.__init__(self)
        self['RawFilePath'] = filePath
        self['RawDirName'], self['RawFileName'] = os.path.split(filePath)
        data = self['RawFileName'].split('.')[0].rsplit('-', 4)
        self['Station'] = data[0]
        self['Year'], self['Month'], \
            self['Day'] = [int(item) for item in data[1:4]]
        self['RunString'] = data[4]
        self['RunNumber'] = int(self.RunString)
        self['Date'] = datetime.date(self.Year, self.Month, self.Day)
        self['DateString'] = '%s-%s-%s' % (self.Year, self.Month, self.Day)
        self['DstFilePath'] = dstFilePath(self)
        self['CalibFilePath'] = calibFilePath(self)
        self['LogFilePath'] = logFilePath(self)
        self['DqmFolderPath'] = dqmFolderPath(self)

    def __getattr__(self, key):
        """ Overloaded method to facilitate access to class members.
        """
        return self[key]

    def daysSinceDataTaking(self):
        """ Return the age of the date in days.
        """
        delta = datetime.date.today() - self.Date
        return delta.days

    def takenToday(self):
        """ Return true if the data have been collected today.
        """
        return self.daysSinceDataTaking() == 0

    def lastSynch(self):
        """ Return the last modification time (and nicely formatted, too)
        of the raw data file.
        """
        return time.ctime(os.path.getmtime(self.RawFilePath))

    def secondsSinceSynch(self):
        """ Return the seconds since the last modification time.
        """
        return time.time() - os.path.getmtime(self.RawFilePath)

    def hoursSinceSynch(self):
        """ Return the hours since the last modification time.
        """
        return self.secondsSinceSynch()/3600.
    
    def processed(self):
        """ Return whether the output DST file exists in the location where
        it is expected to be,
        """
        return os.path.exists(self.DstFilePath)




def rawDataFolder(station, date = datetime.date.today()):
    """ Return the base folder with the raw data for a given station and
    date.
    """
    return os.path.join(E3PIPE_RAW_BASE, station, 'data',
                        '%s-%s-%s' % (date.year, date.month, date.day))

def rawDataFolders(station, endDate = datetime.date.today(), daysSpanned = 2):
    """ Return a list of folders with the raw data for a given station
    and a given time span.

    The time span is given as the end date and a look-back period in days.
    
    The default is to look back two days from today.
    """
    folders = [rawDataFolder(station, endDate)]
    for i in range(1, daysSpanned + 1):
        date = endDate - datetime.timedelta(i)
        folders.append(rawDataFolder(station, date))
    return folders

def dstFilePath(rawFileInfo):
    """ Return the path to the output dst ROOT file corresponding to a given
    input binary raw data file (.bin).
    """
    fileName = rawFileInfo.RawFileName.replace('.bin', '_dst.root')
    return os.path.join(E3PIPE_RECON_BASE, rawFileInfo.Station,
                        rawFileInfo.DateString, fileName)

def calibFilePath(rawFileInfo):
    """ Return the path to the calib file corresponding to a given input binary
    raw data file (.bin).
    """
    fileName = rawFileInfo.RawFileName.replace('.bin', '_eeecalib.txt')
    return os.path.join(E3PIPE_CALIB_BASE, rawFileInfo.Station,
                        rawFileInfo.DateString, fileName)

def dqmFolderPath(rawFileInfo):
    """ Return the path to the output ROOT dqm file corresponding to a given
    input binary raw data file (.bin).
    """
    folderName = rawFileInfo.RawFileName.replace('.bin', '')
    return os.path.join(E3PIPE_DQM_BASE, rawFileInfo.Station,
                        rawFileInfo.DateString, folderName)

def logFilePath(rawFileInfo):
    """ Return the path to the log file corresponding to a given input binary
    raw data file (.bin).
    """
    fileName = rawFileInfo.RawFileName.replace('.bin', '.log')
    return os.path.join(E3PIPE_LOG_BASE, rawFileInfo.Station,
                        rawFileInfo.DateString, fileName)

def dataProductLocations(rawFilePath):
    """ Return the file paths for the relevant output files corresponding to
    a given input raw data (.bin) file path
    """
    info = E3RawDataInfo(rawFilePath)
    return dstFilePath(info), calibFilePath(info), dqmFolderPath(info),\
        logFilePath(info)



if __name__ == '__main__':
    for key in dir():
        if key.startswith('E3PIPE'):
            print '%s = %s' % (key, eval(key))
    filePath = '/data/ALTA-01/data/2014-10-11/ALTA-01-2014-10-11-00001.bin'
    runInfo = E3RawDataInfo(filePath)
    print runInfo
    print runInfo.daysSinceDataTaking()
    print runInfo.takenToday()
    print runInfo.processed()
    print filePath
    for location in dataProductLocations(filePath):
        print location
    print rawDataFolder('ALTA-01')
    print rawDataFolders('ALTA-01')
    runInfo = E3RawDataInfo('../data/CERN-01-2014-05-16-00003.bin')
    print runInfo.lastSynch()
    print runInfo.hoursSinceSynch()
