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
        self.__InfoDict = {'badness': None}
        self.validate()

    def validate(self):
        """ Validate the alarm configuration.
        """
        className = self.__RootObject.__class__.__name__
        if not className in self.SUPPORTED_ROOT_TYPES:
            abort('%s object not supported by alarm %s' %\
                  (className, self.name()))

    def setInfo(self, key, value):
        """ Insert a key/value pair in the self.__InfoDict data member.
        """
        self.__InfoDict[key] = value

    def info(self):
        """ Return the info dictionary.
        """
        return self.__InfoDict

    def name(self):
        """ Return the alarm algorithm name.
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

    def valueBadness(self, value, error = None):
        """ Calculate the badness for a given value (and, possibly, the
        associated error).

        This method turns out to be handy when the algorithm does not
        return a plain number in one step, but one has to loop explicitely,
        e.g., over the bins of a histogram or the entries of a tree.
        """
        return self.__Limits.badness(value, error)

    def badness(self):
        """ Return the badness, as stored in the self.__InfoDict data member.
        """
        return self.__InfoDict['badness']

    def setValue(self, value, error = None, badness = None):
        """ Set the alarm value (and error, if applicable).

        This is the main function, as it determines the alarm status too.

        Note that in some case we already have the badness precalculated when
        we call this function, e.g., if we have looped already on the 
        bin contents of an histogram in alarm_y_values. In this case we
        provide a third optional argument to pass the badness value from the
        outside.
        """
        self.__Value = value
        self.__Error = error
        if badness is None:
            badness = self.valueBadness(value, error)
        self.setInfo('badness', badness)
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

    def htmlRow(self):
        """ Return an HTML row for the output report.
        """
        pass

    def __str__(self):
        """ String formatting.
        
        TODO: format the value/error pair properly.
        """
        return '%s on %s -> %s +- %s %s (%s) %s' %\
            (self.name(), self.__RootObject.GetName(), self.__Value,
             self.__Error, self.__Limits, self.__Status, self.info())
