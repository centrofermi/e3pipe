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


from e3pipe.root.__ROOT__ import *
from e3pipe.root.E3RootObject import E3RootObject


class E3H2D(ROOT.TH2D, E3RootObject):

    """ Wrapper around the ROOT.TH2D object.
    """

    def __init__(self, name, title, xbins, xmin, xmax, ybins, ymin, ymax,
                 **kwargs):
        """ Constructor.
        """
        ROOT.TH2D.__init__(self, name, title, xbins, xmin, xmax,
                           ybins, ymin, ymax)
        E3RootObject.init(self, **kwargs)
