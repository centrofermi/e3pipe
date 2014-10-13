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


import math

from e3pipe.dqm.E3Alarm import E3Alarm



class alarm_exp_fit_lambda(E3Alarm):

    """ Derived class for setting alarm on the lambda value from an exponential
    fit to a histogram.
    """

    SUPPORTED_ROOT_TYPES = ['TH1I', 'TH1F', 'TH1D']
    SUPPORTED_PARAMETERS = []
    SUPPORTED_CONDITIONS = []
    OUTPUT_DESCRIPTION = 'tau value from an exponential fit'
    FIT_FUNC_NAME = 'exp'

    def __init__(self, rootObject, errMin, warnMin, warnMax, errMax):
        """ Overloaded constructor.
        """
        E3Alarm.__init__(self, rootObject, errMin, warnMin, warnMax, errMax)
        import ROOT
        self.__FitFunction = ROOT.TF1(self.FIT_FUNC_NAME, '[0]*exp(-x*[1])')
        self.__FitFunction.SetParameters(1., 1.)

    def run(self):
        """ Overloaded method.
        """
        obj = self.rootObject()
        xmin = obj.GetXaxis().GetXmin()
        xmax = obj.GetXaxis().GetXmax()
        self.__FitFunction.SetRange(xmin, xmax)
        obj.Fit(self.__FitFunction)
        value = self.__FitFunction.GetParameter(1)
        error = self.__FitFunction.GetParError(1)
        self.setValue(value, error)

    def draw(self):
        """ Overloaded method.
        """
        import ROOT
        _f = self.__FitFunction.Clone()
        _f.SetLineWidth(2)
        for par in [self.warningMin(), self.warningMax()]:
            _f.SetParameter(1, par)
            _f.SetLineColor(ROOT.kOrange)
            _f.DrawCopy('same')
        for par in [self.errorMin(), self.errorMax()]:
            _f.SetParameter(1, par)
            _f.SetLineColor(ROOT.kRed)
            _f.DrawCopy('same')



def test():
    """ Test program.
    """
    import ROOT
    f = ROOT.TF1('f', '[0]*exp(-x/*[1])', 0, 10)
    f.SetParameters(1, 2.5)
    h = ROOT.TH1F('h', 'h', 100, 0, 10)
    h.FillRandom('f', 10000)
    a = alarm_exp_fit_tau(h, 1, 2, 3, 4)
    a.run()
    print a


if __name__ == '__main__':
    test()

