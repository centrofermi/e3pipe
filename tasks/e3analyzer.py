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
import sys

import e3pipe.__utils__ as __utils__

from e3pipe.__logging__ import logger, startmsg, abort
from e3pipe.misc.E3Chrono import E3Chrono
from e3pipe.config.__storage__ import E3PIPE_TEMP, cleanupTemp, listTemp
from e3pipe.config.__analyzer__ import E3_ANALYZER, E3_CALIB_FILE_NAME,\
    E3_ANALYZER_OUTPUTS


def e3analyzer(binFilePath, suffix = None):
    """ Run the official EEE analyzer.

    Mind we are not doing anything, at this level, to make sure that you do
    have the right eee_calib.txt file---it is really your responsibility
    to do it.
    """
    chrono = E3Chrono()
    if not os.path.exists(binFilePath):
        abort('Could not find %s, giving up...' % binFilePath)
    if not binFilePath.endswith('.bin'):
        abort('%s not a .bin file, giving up...' % binFilePath)
    cleanupTemp()
    listTemp()
    logger.info('Processing run data file %s...' % binFilePath)
    binFileName = os.path.basename(binFilePath)
    copyFilePath = os.path.join(E3PIPE_TEMP, binFileName)
    __utils__.cp(binFilePath, copyFilePath)
    _cmd = 'cd %s; %s %s' % (E3PIPE_TEMP, E3_ANALYZER, copyFilePath)
    logger.info('Generating the calibration file...')
    exitCode = __utils__.cmd(_cmd)
    if exitCode:
        sys.exit(exitCode)
    logger.info('Running the EEE Analizer for real!')
    exitCode = __utils__.cmd(_cmd)
    if exitCode:
        sys.exit(exitCode)
    logger.info('Run processed in %.3f s.' % chrono.stop())
    baseFilePath = copyFilePath.replace('.bin', '')
    if suffix is not None:
        for extension in E3_ANALYZER_OUTPUTS:
            src = '%s%s' % (baseFilePath, extension)
            dest = '%s_%s%s' % (baseFilePath, suffix, extension)
            __utils__.mv(src, dest)
        baseFilePath = '%s_%s' % (baseFilePath, suffix)
    listTemp()
    logger.info('Returning base path: "%s"...' % baseFilePath)
    return baseFilePath


	
if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser()
    (opts, args) = parser.parse_args()
    for arg in args:
        e3analyzer(arg)
