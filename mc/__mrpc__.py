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


""" Basic definition of the detector geometry for the simulation and
reconstruction.

All the dimensions are in cm.
"""

MRPC_STRIP_PITCH = 3.2
MRPC_NUM_STRIPS_PER_PLANE = 24
MRPC_WIDTH = MRPC_STRIP_PITCH*MRPC_NUM_STRIPS_PER_PLANE
MRPC_LENGTH = 158.0
MRPC_ACTIVE_AREA = MRPC_WIDTH*MRPC_LENGTH
MRPC_LONGITUDINAL_SIGMA = 0.7
