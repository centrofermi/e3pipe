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
_synopsis = 'Do a backfill of the run database'


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
                  help = 'the maximum number of runs to be processed')
parser.add_option('-s', '--station', action = 'append', type = str,
                  default = None, dest = 'stations',
                  help = 'the station(s) to be processed')
(opts, args) = parser.parse_args()

# Make sure we are passing some argument.
if len(args):
    parser.print_help()
    parser.error('This apps only takes options.')

# Print the start message.
from e3pipe.__logging__ import startmsg
startmsg()

# Import the necessary stuff.
from e3pipe.tasks.e3dbbackfill import e3dbbackfill

# And now we are ready to go.
end = opts.end
if end is None:
    import datetime
    end = datetime.date.today()
else:
    from e3pipe.dst.__time__ import str2date
    end = str2date(end)
e3dbbackfill(opts.stations, end, opts.span, opts.maxruns)
