#!/usr/bin/env python
# *********************************************************************
# * Copyright (C) 2015 Luca Baldini (luca.baldini@pi.infn.it)         *
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
_synopsis = 'Run the new EEE analyzer on a single .bin file'

# Set up the command-line switches.
from e3pipe.misc.E3OptionParser import E3OptionParser
parser = E3OptionParser(_usage, _synopsis)
parser.add_option('-s', '--suffix', type = str, default = None, dest = 'suffix',
                  help = 'a text label to be attached to the output file names')
parser.add_option('-o', '--options', type = str, default = '-b -r -c',
                  dest = 'options',
                  help = 'the command-line switches for the new analyzer')
(opts, args) = parser.parse_args()

# Make sure we are passing some argument.
if not len(args) == 1:
    parser.print_help()
    parser.error('Please provide a single input file.')
rawFilePath = args[0]

# Print the start message.
from e3pipe.__logging__ import startmsg
startmsg()

# Import the necessary stuff.
from e3pipe.tasks.e3analyzer2 import e3analyzer2

# And now we are ready to go.
e3analyzer2(rawFilePath, opts.suffix, opts.options)
