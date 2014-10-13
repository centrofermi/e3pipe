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


import e3pipe.__utils__

from e3pipe.tasks.e3runAnalyzer import e3runAnalyzer
from e3pipe.tasks.e3buildDst import e3buildDst
from e3pipe.__package__ import E3ANALYZER_OUTPUTS


def e3recon(binFilePath, deleteAscii = False, useFortran = False,
            outputSuffix = None):
    """ Run the analyzer and build the DST (i.e., run the full
    reconstruction).
    """
    baseFilePath = e3runAnalyzer(binFilePath, useFortran, outputSuffix)
    dstFilePath = e3buildDst(baseFilePath)
    if deleteAscii:
        for extension in E3ANALYZER_OUTPUTS:
            e3pipe.__utils__.rm('%s%s' % (baseFilePath, extension))
    return dstFilePath
