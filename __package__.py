#!/usr/bin/env python
# *********************************************************************
# * Copyright (C) 2014 Luca Baldini (luca.baldini@pi.infn.it)         *
# *                                                                   *
# * For the license terms see the file LICENCE, distributed           *
# * along with this software.                                         *
# *********************************************************************
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU GengReral Public License as published by
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

""" Basic folder structure of the package.
"""
E3PIPE_BASE = os.path.abspath(os.path.dirname(__file__))
E3PIPE_APPS = os.path.join(E3PIPE_BASE, 'apps')
E3PIPE_DST = os.path.join(E3PIPE_BASE, 'dst')
E3PIPE_RECON = os.path.join(E3PIPE_BASE, 'recon')
E3PIPE_ROOT = os.path.join(E3PIPE_BASE, 'ROOT')
E3PIPE_TASKS = os.path.join(E3PIPE_BASE, 'tasks')
E3PIPE_TEST = os.path.join(E3PIPE_BASE, 'test')

""" Paths to the analysis program executables. 
"""
E3FORTRAN_ANALYZER_PATH = os.path.join(E3PIPE_RECON, 'fortran', 'EEE_V15')
E3CPP_ANALYZER_PATH = os.path.join(E3PIPE_RECON, 'cpp', 'EEE_V15')

""" Name of the calibration file that is created on the fly by the analysis
program.
"""
E3CALIB_FILE_NAME = 'eee_calib.txt'


if __name__ == '__main__':
    print('E3PIPE_ROOT: %s' % E3PIPE_ROOT)

