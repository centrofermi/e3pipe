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


import ROOT
import math

from e3pipe.dqm.E3Alarm import E3Alarm



class alarm_x_average(E3Alarm):

    """
    """

    SUPPORTED_ROOT_TYPES = [ROOT.TH1]
    SUPPORTED_PARAMETERS = []
    SUPPORTED_CONDITIONS = []
    OUTPUT_DESCRIPTION = None

    def run(self):
        """
        """
        obj = self.rootObject()
        value = obj.GetMean()
        try:
            error = obj.GetRMS()/math.sqrt(obj.GetEntries())
        except ZeroDivisionError:
            error = 0.
        self.setValue(value, error)




def test():
    """ Test program.
    """
    h = ROOT.TH1F('h', 'h', 100, 0, 1)
    h.FillRandom('pol0', 100)
    a = alarm_x_average(h, 0.2, 0.49, 0.51, 0.8)
    a.run()
    print a


if __name__ == '__main__':
    test()
