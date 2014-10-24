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


_usage = 'usage: %prog [options] filePath'
_synopsis = 'Convert a ROOT tree into text format'

# Set up the command-line switches.
from e3pipe.misc.E3OptionParser import E3OptionParser
parser = E3OptionParser(_usage, _synopsis)
parser.add_option('-o', '--output-file', type = str, default = None,
                  dest = 'out',
                  help = 'path to the output file')
parser.add_option('-t', '--tree-name', type = str, default = None,
                  dest = 'tree',
                  help = 'the name of the tree into the file')
(opts, args) = parser.parse_args()

# Check the options.
if opts.tree is None:
    parser.print_help()
    parser.error('Please specify the tree name (e3root2text -t tree).')
# Make sure we are passing some argument.
if len(args) != 1:
    parser.print_help()
    parser.error('Please provide a single input file.')

# Print the start message.
from e3pipe.__logging__ import startmsg
startmsg()

# Import the necessary stuff.
from e3pipe.tasks.e3root2text import e3root2text

e3root2text(args[0], opts.tree, opts.out)
