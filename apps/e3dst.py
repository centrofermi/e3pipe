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
_synopsis = 'Create the ROOT dst from the outputs of the Analyzer'

# Set up the command-line switches.
from e3pipe.misc.E3OptionParser import E3OptionParser
parser = E3OptionParser(_usage, _synopsis)
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
from e3pipe.tasks.e3dst import e3dst

# Mind that we have to pass the base path (with no extension) to the
# task, so we strip the extension itself, here, if necessary.
from e3pipe.config.__analyzer__ import E3_ANALYZER_OUTPUTS
basePath = args[0]
for ext in E3_ANALYZER_OUTPUTS:
    if basePath.endswith(ext):
        basePath = basePath.replace(ext, '')

# And now we are ready to go.
e3dst(basePath)
