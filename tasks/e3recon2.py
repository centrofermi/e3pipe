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


import os

import e3pipe.__utils__ as __utils__

from e3pipe.__logging__ import logger
from e3pipe.tasks.e3analyzer2 import e3analyzer2
from e3pipe.tasks.e3dqm import e3dqm
from e3pipe.config.__storage2__ import E3PIPE_TEMP, E3RawDataInfo
from e3pipe.config.__analyzer__ import E3_CALIB_FILE_NAME



def e3recon2(rawFilePath, copyFiles = True, suffix = None, opts = '-b -r -c'):
    """ Run the analyzer, build the DST and run the DQM (i.e., effectively
    run the full reconstruction for one single run).

    TODO: we should add some protection to make sure that everything
    went fine before we actually try and copy the output files over.

    TODO: we are instantiating a E3RawDataInfo object, here, and therefore
    we are in principle recalculating all the path, which the crawler might
    have already done. While this is not elegant, I don't think we'll ever
    notice the overhead.
    """
    baseFilePath = e3analyzer2(rawFilePath, suffix, opts)
    dstFilePath = '%s_dst.root' % baseFilePath
    dqmFolderPath = '%s_DQM' % baseFilePath
    e3dqm(dstFilePath, dqmFolderPath)
    if copyFiles:
        logger.info('Setting up to copy files...')
        runInfo = E3RawDataInfo(rawFilePath)
        logger.info(runInfo)
        calibFilePath = os.path.join(E3PIPE_TEMP, E3_CALIB_FILE_NAME)
        if os.path.exists(calibFilePath):
            __utils__.cp(calibFilePath, runInfo.CalibFilePath, True)
        __utils__.cp(dstFilePath, runInfo.DstFilePath, True)
        if os.path.exists(runInfo.DqmFolderPath):
            __utils__.rmdir(runInfo.DqmFolderPath)
        __utils__.cp(dqmFolderPath, runInfo.DqmFolderPath, True)

