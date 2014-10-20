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

import e3pipe.__utils__ as __utils__

from e3pipe.__logging__ import logger
from e3pipe.tasks.e3analyzer import e3analyzer
from e3pipe.tasks.e3dst import e3dst
from e3pipe.tasks.e3dqm import e3dqm
from e3pipe.config.__storage__ import E3PIPE_TEMP, E3RawDataInfo,\
    E3CENTRO_FERMI_SERVER, E3CENTRO_FERMI_DQM_BASE, E3PIPE_DQM_PUB_BASE,\
    E3PIPE_DQM_BASE
from e3pipe.config.__analyzer__ import E3_CALIB_FILE_NAME



def e3exportDQM(dqmFolderPath):
    """
    We want something along the lines of:
    ssh www.centrofermi.it mkdir -p /var/www/html_eee/dqm/FRAS-02/2014-10-20/FRAS-02-2014-10-20-00001/
    scp -r /dqm/FRAS-02/2014-10-20/FRAS-02-2014-10-20-00001/* www.centrofermi.it:/var/www/html_eee/dqm/FRAS-02/2014-10-20/FRAS-02-2014-10-20-00001/

    And we only want to do that when we run as the analisi user, i.e. when
    E3PIPE_DQM_BASE is /dqm
    """
    if E3PIPE_DQM_BASE != '/dqm':
        logger.info('E3PIPE_DQM_BASE is not /dqm, skipping export')
        return 
    relPath = dqmFolderPath.replace('/dqm/', '')
    target = os.path.join(E3CENTRO_FERMI_DQM_BASE, relPath)
    __utils__.cmd('ssh %s mkdir -p %s' % (E3CENTRO_FERMI_SERVER, target))
    source = os.path.join(dqmFolderPath, '*')
    dest = '%s:%s' % (E3CENTRO_FERMI_SERVER, target)
    __utils__.cmd('scp -r %s %s' % (source, dest))



def e3recon(rawFilePath, copyFiles = True, suffix = None, exportDQM = False):
    """ Run the analyzer, build the DST and run the DQM (i.e., effectively
    run the full reconstruction for one single run).

    TODO: we should add some protection to make sure that everything
    went fine before we actually try and copy the output files over.

    TODO: we are instantiating a E3RawDataInfo object, here, and therefore
    we are in principle recalculating all the path, which the crawler might
    have already done. While this is not elegant, I don't think we'll ever
    notice the overhead.
    """
    baseFilePath = e3analyzer(rawFilePath, suffix)
    dstFilePath = e3dst(baseFilePath)
    dqmFolderPath = '%s_DQM' % baseFilePath
    e3dqm(dstFilePath, dqmFolderPath)
    if copyFiles:
        logger.info('Setting up to copy files...')
        runInfo = E3RawDataInfo(rawFilePath)
        logger.info(runInfo)
        calibFilePath = os.path.join(E3PIPE_TEMP, E3_CALIB_FILE_NAME)
        __utils__.cp(calibFilePath, runInfo.CalibFilePath, True)
        __utils__.cp(dstFilePath, runInfo.DstFilePath, True)
        if os.path.exists(runInfo.DqmFolderPath):
            __utils__.rmdir(runInfo.DqmFolderPath)
        __utils__.cp(dqmFolderPath, runInfo.DqmFolderPath, True)
    if exportDQM:
        e3exportDQM(runInfo.DqmFolderPath)

        
