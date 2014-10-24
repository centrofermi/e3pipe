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

from e3pipe.dst.__time__ import E3_DATETIME_REFERENCE



class E3WeatherStationRecord:

    """ Small utility class to encapsulate a record from the weather station.
    """
    
    def __init__(self, year, month, day, hours, minutes, indoorTemperature,
                 outdoorTemperature, pressure):
        """ Constructor.

        All the temperatures are in degrees and the pressure in hPa.
        """
        self.__Datetime = datetime.datetime(year, month, day, hours, minutes)
        self.__IndoorTemperature = indoorTemperature/100.
        self.__OutdoorTemperature = outdoorTemperature/100.
        self.__Pressure = pressure
        
    def timestamp(self):
        """ Mind we're not using delta.total_seconds(), here, as apparently
        that is new in python 2.7 and it would not work at CNAF.
        
        TODO: we subtract two hours to take into account the timezone, but
        we'll be introuble with daylight savings time!
        """
        delta = self.__Datetime - E3_DATETIME_REFERENCE
        return float(delta.seconds + delta.days*24*3600 - 2*3600)

    def __str__(self):
        """ String representation.
        """
        return '%s: out = %.2f deg C, in = %.2f deg C, P = %d hPa' %\
            (self.__Datetime, self.__OutdoorTemperature,
             self.__IndoorTemperature, self.__Pressure)
