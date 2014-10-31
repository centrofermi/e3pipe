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

from e3pipe.dst.__time__ import E3_DATETIME_REFERENCE, isDST



class E3WeatherStationRecord:

    """ Small utility class to encapsulate a record from the weather station.
    """
    
    def __init__(self, *args):
        """ Constructor.

        All the temperatures are in degrees and the pressure in hPa.
        """
        self.__Datetime = datetime.datetime(*args[:5])
        self.__IndoorTemperature = args[5]/100.
        self.__OutdoorTemperature = args[6]/100.
        self.__Pressure = args[7]
        
    def seconds(self):
        """ Mind we're not using delta.total_seconds(), here, as apparently
        that is new in python 2.7 and it would not work at CNAF.
        
        We try and take into account the daylight saving time in the crudest
        possible way, as the __time__.isDST() method relies on the fact that
        the computer that is running the reconstruction is in the same time
        zone of the DAQ. This ugly!
        """
        delta = self.__Datetime - E3_DATETIME_REFERENCE
        secs = delta.seconds + delta.days*24*3600
        if isDST(self.__Datetime):
            secs -= 7200
        else:
            secs -= 3600
        return float(secs)

    def indoorTemperature(self):
        """
        """
        return self.__IndoorTemperature

    def outdoorTemperature(self):
        """
        """
        return self.__OutdoorTemperature

    def pressure(self):
        """
        """
        return self.__Pressure

    def data(self):
        """ Return the data in a form which is suitable for the corresponding
        DST tree.
        """
        return {'Seconds': self.seconds(),
                'IndoorTemperature': self.__IndoorTemperature,
                'OutdoorTemperature': self.__OutdoorTemperature,
                'Pressure': self.__Pressure
                }

    def __str__(self):
        """ String representation.
        """
        return '%s: out = %.2f deg C, in = %.2f deg C, P = %d hPa' %\
            (self.__Datetime, self.__OutdoorTemperature,
             self.__IndoorTemperature, self.__Pressure)
