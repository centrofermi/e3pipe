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


from e3pipe.__logging__ import logger, abort
from e3pipe.dqm.E3AlarmLimits import E3AlarmLimits



class E3Alarm:

    """ Utility class representing an alarm.
    """

    STATUS_UNSET = 'Unset'
    STATUS_CLEAN = 'Clean'
    STATUS_WARNING = 'Warning'
    STATUS_ERROR = 'Error'
    SUPPORTED_ROOT_TYPES = []
    SUPPORTED_PARAMETERS = []
    SUPPORTED_CONDITIONS = []
    OUTPUT_DESCRIPTION = None
    
    def __init__(self, rootObject, errMin, warnMin, warnMax, errMax):
        """ Constructor.
        """
        self.__RootObject = rootObject
        self.__Limits = E3AlarmLimits(errMin, warnMin, warnMax, errMax)
        self.__Value = None
        self.__Error = None
        self.__Status = self.STATUS_UNSET
        self.__InfoDict = {}

    def name(self):
        """
        """
        return self.__class__.__name__.replace('alarm_', '')

    def rootObject(self):
        """ Return the underlying ROOT object.
        """
        return self.__RootObject

    def status(self):
        """ Return the alarm status.
        """
        return self.__Status

    def unset(self):
        """ Return whether the alarm status is Unset.
        """
        return self.status() == self.STATUS_UNSET

    def clean(self):
        """ Return whether the alarm status is Clean.
        """
        return self.status() == self.STATUS_CLEAN

    def warning(self):
        """ Return whether the alarm status is Warning.
        """
        return self.status() == self.STATUS_WARNING

    def error(self):
        """ Return whether the alarm status is Error.
        """
        return self.status() == self.STATUS_ERROR

    def setValue(self, value, error = None):
        """ Set the alarm value (and error, if applicable).

        This is the main function, as it determines the alarm status too.
        """
        self.__Value = value
        self.__Error = error
        badness = self.__Limits.badness(value, error)
        self.__InfoDict['badness'] = badness
        if badness <= E3AlarmLimits.WARNING_BADNESS:
            self.__Status = self.STATUS_CLEAN
        elif badness <= E3AlarmLimits.ERROR_BADNESS:
            self.__Status = self.STATUS_WARNING
        else:
            self.__Status = self.STATUS_ERROR

    def run(self):
        """ Do nothing method, to be reimplemented by the derived classes.
        """
        pass

    def __str__(self):
        """ String formatting.
        
        TODO: format the value/error pair properly.
        """
        return '%s on %s -> %s +- %s %s (%s)' %\
            (self.name(), self.__RootObject.GetName(),
             self.__Value, self.__Error, self.__Limits, self.__Status)
