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


import e3pipe.__utils__ as __utils__

from e3pipe.misc.E3Chrono import E3Chrono
from e3pipe.__logging__ import logger
from e3pipe.config.__storage__ import doDbRegister, E3RawDataInfo
from e3pipe.dst.__runid__ import uniqueRunId
from e3pipe.db.__register__ import registerRun


_usage = 'usage: %prog [options] binfile'
_synopsis = 'Run the full e3recon in a shell and, if needed, register the results in the database'

# Set up the command-line switches.
from e3pipe.misc.E3OptionParser import E3OptionParser
parser = E3OptionParser(_usage, _synopsis)
(opts, args) = parser.parse_args()

# Make sure we are passing some argument.
if not len(args) == 1:
    parser.print_help()
    parser.error('Please provide a single input file.')
rawFilePath = args[0]

# Print the start message.
from e3pipe.__logging__ import startmsg
startmsg()

# Run e3recon
chrono = E3Chrono()
_cmd = 'e3recon2.py %s' % rawFilePath
exitCode = __utils__.cmd(_cmd)
if exitCode == 0:
    logger.info('Run processed in %.3f s.' % chrono.stop())
else:
    logger.error('Processing terminated with exit code %d after %.3f s.' %\
                 (exitCode, chrono.stop()))
if doDbRegister():
    runInfo = E3RawDataInfo(rawFilePath)
    registerRun(runInfo, exitCode)
