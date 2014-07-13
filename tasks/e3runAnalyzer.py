#!/usr/bin/env python
# *********************************************************************
# * Copyright (C) 2014 Luca Baldini (luca.baldini@pi.infn.it)         *
# *                                                                   *
# * For the license terms see the file LICENCE, distributed           *
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
import e3pipe.__utils__

from e3pipe.__logging__ import logger, startmsg, abort
from e3pipe.__package__ import E3FORTRAN_ANALYZER_PATH, E3CPP_ANALYZER_PATH,\
    E3ANALYZER_OUTPUTS
from e3pipe.misc.E3Chrono import E3Chrono


E3FORTRAN_SUFFIX = 'FORTRAN'


def e3runAnalyzer(binFilePath, useFortran = False, outputSuffix = None):
    """ Run the official EEE analyzer.

    Mind we are not doing anything, at this level, to make sure that you do
    have the right eee_calib.txt file---it is really your responsibility
    to do it.
    """
    chrono = E3Chrono()
    if not os.path.exists(binFilePath):
        logger.error('Could not find %s, giving up...' % binFilePath)
        return 1
    if not binFilePath.endswith('.bin'):
        logger.error('%s not a .bin file, giving up...' % binFilePath)
        return 1
    logger.info('Processing run data file %s...' % binFilePath)
    if useFortran:
        exePath = E3FORTRAN_ANALYZER_PATH
        if outputSuffix is None:
            outputSuffix = E3FORTRAN_SUFFIX 
        else:
            outputSuffix = '%s_%s' % (outputSuffix, E3FORTRAN_SUFFIX)
    else:
        exePath = E3CPP_ANALYZER_PATH
    sc = e3pipe.__utils__.cmd('%s %s' % (exePath, binFilePath))
    if sc:
        return None
    logger.info('Run processed in %.3f s.' % chrono.stop())
    baseFilePath = binFilePath.replace('.bin', '')
    if outputSuffix is not None:
        for extension in E3ANALYZER_OUTPUTS:
            src = '%s%s' % (baseFilePath, extension)
            dest = '%s_%s%s' % (baseFilePath, outputSuffix, extension)
            e3pipe.__utils__.mv(src, dest)
    baseFilePath = '%s_%s' % (baseFilePath, outputSuffix)
    return baseFilePath


	
if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser()
    (opts, args) = parser.parse_args()
    for arg in args:
        e3runAnalyzer(arg)
