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


_usage = 'usage: %prog [options]'
_synopsis = 'Create a series of DQM reports'


# Set up the command-line switches.
from e3pipe.misc.E3OptionParser import E3OptionParser
parser = E3OptionParser(_usage, _synopsis)
parser.add_option('-E', '--end-date', type = str,
                  default = None, dest = 'end',
                  help = 'the end date for the time span of interest')
parser.add_option('-N', '--days-spanned', type = int,
                  default = 2, dest = 'span',
                  help = 'the duration (in days) of the time span of interest')
parser.add_option('-m', '--max-runs', type = int,
                  default = None, dest = 'maxruns',
                  help = 'the maximum number of runs to be merged')
parser.add_option('-F', '--station-file', type = str,
                  default = None, dest = 'statfile',
                  help = 'path to the list of stations')
parser.add_option('-o', '--output-folder', type = str,
                  default = None, dest = 'out',
                  help = 'path to the output folder')
(opts, args) = parser.parse_args()

# Print the start message.
from e3pipe.__logging__ import logger, startmsg, abort
startmsg()

# Import the necessary stuff.
from e3pipe.tasks.e3report import e3report

if len(args):
    parser.error('This app only takes options.')
if opts.statfile is None:
    parser.error('Please select an input file (e3report.py -F file)')

# And now we are ready to go.
if opts.end is None:
    import datetime
    end = datetime.date.today()
else:
    from e3pipe.dst.__time__ import str2date
    end = str2date(opts.end)

import os
    
if not os.path.isfile(opts.statfile):
    abort('Could not find input file %s' % opts.statfile)
stations = [line.split()[0] for line in open(opts.statfile)]

import e3pipe.__utils__ as __utils__

for station in stations:
    logger.info('Creating report for %s...' % station)
    _cmd = 'e3report.py -s %s -E %s -N %d -o %s' %\
        (station, end, opts.span, opts.out)
    exitCode = __utils__.cmd(_cmd)

