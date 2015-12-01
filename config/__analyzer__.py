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


import os


""" Path to the official EEE analyzer.

A little bit of history, here (last updated on October 7, 2014).
* /opt/eee/bin/EEE_Analyzer_V0 was the original analyzer program
  when the work on the wrapper started.
* /opt/eee/bin/EEE_Analyzer is currently pointing to a slightly
  modified version where Richard is writing a complete row (with dummy
  values) for the GPS events and the events with no track in general.
"""
try:
    E3_ANALYZER  = os.environ['E3_ANALYZER']
except KeyError:
    E3_ANALYZER = '/opt/eee/bin/EEE_Analyzer_V3.1'


""" And of course we have a custom DAQ in Pisa and need a different
analyzer, otherwise life would have been too simple.
"""
try:
    E3_ANALYZER_PI  = os.environ['E3_ANALYZER_PI']
except KeyError:
    E3_ANALYZER_PI = '/opt/eee/bin/EEE_Analyzer_PI_V3.1'

    
""" And, if that was not enough, here is the brand new analyzer written
by Francesco Noferini that will eventually replace the old one.
"""
try:
    E3_ANALYZER_NEW  = os.environ['E3_ANALYZER_NEW']
except KeyError:
    E3_ANALYZER_NEW = '/opt/eee/bin/eeereco.exe'


""" Name of the calibration file that is created on the fly by the analysis
program.
"""
E3_CALIB_FILE_NAME = 'eee_calib.txt'


""" Extensions of the output files produced by the analyzer.
"""
E3_ANALYZER_OUTPUTS = ['.2tt', '.out', '.sum', '.tim']



if __name__ == '__main__':
    for key in dir():
        if key.startswith('E3'):
            print '%s = %s' % (key, eval(key))
