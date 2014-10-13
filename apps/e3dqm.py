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

_usage = 'usage: %prog [options] filePath'
_synopsis = 'Run the data quality monitor on a ROOT DST file'

# Set up the command-line switches.
from e3pipe.misc.E3OptionParser import E3OptionParser
parser = E3OptionParser(_usage, _synopsis)
parser.add_option('-o', '--output-folder', type = str, default = None,
                  dest = 'output_folder',
                  help = 'the output folder for the DQM products')
parser.add_option('-i', '--interactive', action = 'store_true',
                  default = False, dest = 'interactive',
                  help = 'run interactively (show the plots)')
(opts, args) = parser.parse_args()

# Make sure we are passing some argument.
if not len(args):
    parser.print_help()
    parser.error('Please provide a single input file.')

# Print the start message.
from e3pipe.__logging__ import startmsg
startmsg()

# Import the necessary stuff.
from e3pipe.tasks.e3dqm import e3dqm

# Mind that we have to pass the base path (with no extension) to the
# task, so we strip the extension itself, here, if necessary.
dstFilePath = args[0]
# And now we are ready to go.
e3dqm(dstFilePath, opts.output_folder)
if opts.interactive:
    os.environ['PYTHONINSPECT'] = 'True'
