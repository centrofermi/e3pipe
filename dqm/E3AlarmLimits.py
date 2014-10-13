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
from e3pipe.misc.__formatting__ import formatNumber


class E3AlarmLimits:

    """ Small class describing a set of alarm limits.
    """

    WARNING_BADNESS = 1.0
    ERROR_BADNESS   = 2.0
    DELTA_BADNESS   = ERROR_BADNESS - WARNING_BADNESS

    def __init__(self, errMin, warnMin, warnMax, errMax):
        """ Constructor.
        """
        self.WarningMin = warnMin
        self.WarningMax = warnMax
        self.ErrorMin   = errMin
        self.ErrorMax   = errMax
        self.__validate()
        
    def __validate(self):
        """ Validate the limits (i.e. make sure that the min and max
        values are consistent and that the warning margins are smaller than
        the error margins.)
        """
        if self.WarningMin > self.WarningMax:
            abort('Warning min (%s) higher than warning max (%s).' %\
                  (self.WarningMin, self.WarningMax))
        if self.ErrorMin > self.ErrorMax:
            abort('Error min (%s) higher than error max (%s).' %\
                  (self.ErrorMin, self.ErrorMax))
        if self.WarningMin < self.ErrorMin:
            abort('Warning min (%s) lower than error min (%s).' %\
                  (self.WarningMin, self.ErrorMin))
        if self.WarningMax > self.ErrorMax:
            abort('Warning max (%s) is higher than error max (%s).' %\
                  (self.WarningMax, self.ErrorMax))

    def badness(self, value, error = None):
        """ Return the badness of a given number (possibly with its error),
        relative to the alarm limits.

        The "badness" is the basic measure for determining the status of an
        alarm; it is a function that is equal to the value of WARNING_BADNESS
        on the warning limits and is equal to the value of ERROR_BADNESS in
        correspondence of the error limits.
    
        It is essentially calculated according to the following steps:
        - the average of the warning limits (center) is calculated;
        - the best value (the one that best fits into the limits, once the
        associated error is taken into account is calculated). If the error bar
        does *not* cross the center, than the best value is the actual value
        plus or minus the error (possibly multiplicated by a constant),
        depending on whether the value itself lieas above or below the center.
        If the error bar *does* cross the center, then the best value is assumed
        to be the center itself.
        - the badness (i.e. the function defined above) is calculated on
        the best value.
        """
        # Make the value float.
        value = float(value)
        # If the error is not, set it to zero. Make it float.
        if error is None:
            error = 0.0
        else:
            error = float(error)
        # The center in the average value between the warning limits.
        center = (self.WarningMin + self.WarningMax)/2.0
        # Evaluation of the best value:
        if (value - error) >= center:
            bestValue = value - error
        elif (value + error) <= center:
            bestValue = value + error
        else:
            bestValue = center
        # Now enter the real logic involved in the algorithm.
        # Case 1: the best value is between warning min and warning max
        # (the status will be CLEAN).
        if (bestValue >= self.WarningMin) and (bestValue <= self.WarningMax):
            try:
                badness = self.WARNING_BADNESS*abs(bestValue - center)/\
                    (self.WarningMax - center)
            # If the center is on the warning max, set the badness to zero.
            except ZeroDivisionError:
                badness = 0.0
        # Case 2: the best value is below the warning min
        # (the status will be either WARNING or ERROR).
        elif bestValue < self.WarningMin:
            try:
                badness = self.WARNING_BADNESS + self.DELTA_BADNESS*\
                (self.WarningMin - bestValue)/(self.WarningMin - self.ErrorMin)
            except ZeroDivisionError:
                # If warning min and error min are the same, refer the
                # calculation of the badness to the center.
                try:
                    badness = self.WARNING_BADNESS + self.DELTA_BADNESS*\
                        (center - bestValue)/(center - self.ErrorMin)
                except ZeroDivisionError:
                    # And if event the center and the error min are the same
                    # (degenerate case in which all the four limits coincide)
                    # then set the badness to a constant, adding the absolute
                    # value of the distance between the center and the best
                    # value (possibly divided by the error) to preserve the
                    # sorting (as far as badness is concerned) between
                    # different data points.
                    db = abs(center - bestValue)
                    if error > 0.0:
                        db /= error
                    badness = self.ERROR_BADNESS + self.DELTA_BADNESS + db
        else:
            try:
                badness = self.WARNING_BADNESS + self.DELTA_BADNESS*\
                (bestValue - self.WarningMax)/(self.ErrorMax - self.WarningMax)
            except ZeroDivisionError:
                # If warning max and error max are the same, refer the
                # calculation of the badness to the center.
                try:
                    badness = self.WARNING_BADNESS + self.DELTA_BADNESS*\
                              (bestValue - center)/(self.ErrorMax - center)
                except ZeroDivisionError:
                    # And if event the center and the error min are the same
                    # (degenerate case in which all the four limits coincide)
                    # then set the badness to a constant, adding the absolute
                    # value of the distance between the center and the best
                    # value (possibly divided by the error) to preserve the
                    # sorting (as far as badness is concerned) between
                    # different data points.
                    db = abs(center - bestValue)
                    if error > 0.0:
                        db /= error
                    badness = self.ERROR_BADNESS + self.DELTA_BADNESS + db
        return badness

    def __str__(self):
        """ String formatting.
        """
        return '[%s / %s --- %s / %s]'%\
            (formatNumber(self.ErrorMin), formatNumber(self.WarningMin),
             formatNumber(self.WarningMax), formatNumber(self.ErrorMax))



if __name__ == '__main__':
    limits = E3AlarmLimits(5.0, 10.0, 30.0, 50.)
    print limits, limits.badness(22, 0.0), limits.badness(80, 0.0)
    
