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

from e3pipe.tasks.e3analyzer import e3analyzer
from e3pipe.tasks.e3dst import e3dst
from e3pipe.tasks.e3dqm import e3dqm
from e3pipe.config.__storage__ import *



def e3recon(binFilePath, copyFiles = True, suffix = None):
    """ Run the analyzer, build the DST and run the DQM (i.e., effectively
    run the full reconstruction for one single run).
    """
    baseFilePath = e3analyzer(binFilePath, suffix)
    dstFilePath = e3dst(baseFilePath)
    dqmFolder = '%s-DQM' % baseFilePath
    e3dqm(dstFilePath, dqmFolder)
    #if copyFiles:
    #    src = os.path.join()
