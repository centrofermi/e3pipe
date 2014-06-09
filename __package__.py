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


E3PIPE_BASE = os.path.abspath(os.path.dirname(__file__))
E3PIPE_APPS = os.path.join(E3PIPE_BASE, 'apps')
E3PIPE_DST = os.path.join(E3PIPE_BASE, 'dst')
E3PIPE_RECON = os.path.join(E3PIPE_BASE, 'recon')
E3PIPE_ROOT = os.path.join(E3PIPE_BASE, 'ROOT')
E3PIPE_TEST = os.path.join(E3PIPE_BASE, 'test')

FORTRAN_ANALYIZER_PATH = os.path.join(E3PIPE_RECON, 'fortran', 'EEE_V15')



if __name__ == '__main__':
    print('E3PIPE_ROOT: %s' % E3PIPE_ROOT)

