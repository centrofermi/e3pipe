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

The basic rules are the following:
1\ the x-axis is oriented along the strips;
2\ the y coordinate (orthogonal to the strip direction) is quantized at the
   level of the strip pitch and can take 24 values from 3.2 to 76.8
   (although things are not as simple,
   see https://github.com/centrofermi/e3pipe/issues/85)
3\ the x coordinate runs from 0 to 158, with long tails on either sides
   (even when requiring well-reconstructed events.)
"""

# Basic quantities
MRPC_STRIP_PITCH = 3.2
MRPC_NUM_STRIPS_PER_PLANE = 24
MRPC_LENGTH = 158.0
MRPC_LONGITUDINAL_SIGMA = 0.7

# Derived quantities.
MRPC_X_MIN = 0.
MRPC_X_MAX = MRPC_LENGTH
MRPC_Y_MIN = 0.5*MRPC_STRIP_PITCH
MRPC_Y_MAX = (MRPC_NUM_STRIPS_PER_PLANE + 0.5)*MRPC_STRIP_PITCH
MRPC_WIDTH = MRPC_STRIP_PITCH*MRPC_NUM_STRIPS_PER_PLANE
MRPC_ACTIVE_AREA = MRPC_WIDTH*MRPC_LENGTH
