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


_usage = 'usage: %prog [options] binfile'
_synopsis = 'Run the standard EEE analyzer on a single .bin file'

# Set up the command-line switches.
from e3pipe.misc.E3OptionParser import E3OptionParser
parser = E3OptionParser(_usage, _synopsis)
parser.add_option('-R', '--recreate-calib', action = 'store_true',
                  default = False, dest = 'recreate_calib',
                  help = 'recreate the eee_calib.txt file')
parser.add_option('-s', '--output_suffix', type = str, default = None,
                  dest = 'output_suffix',
                  help = 'a text label to be attached to the output file names')
(opts, args) = parser.parse_args()

# Make sure we are passing some argument.
if not len(args):
    parser.print_help()
    parser.error('Please provide a single input file.')

# Print the start message.
from e3pipe.__logging__ import startmsg
startmsg()

# Import the necessary stuff.
import e3pipe.__utils__
import os
from e3pipe.__package__ import E3CALIB_FILE_NAME
from e3pipe.tasks.e3analyzer import e3analyzer

# If we are recreating the eee_calib.txt file we need to remove the old one
# and run the analyzer on the very first file.
if opts.recreate_calib:
    e3pipe.__utils__.rm(E3CALIB_FILE_NAME)
    e3analyzer(args[0])

# And now we are ready to go.
e3analyzer(args[0], opts.output_suffix)
