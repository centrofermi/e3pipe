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
from e3pipe.dst.__time__ import E3_TIME_OFFSET


class E3Graph(ROOT.TGraphErrors, E3RootObject):

    """ Wrapper around the ROOT.TGraphErrors object.
    """

    def __init__(self, name, title, **kwargs):
        """ Constructor.
        """
        ROOT.TGraphErrors.__init__(self)
        self.SetNameTitle(name, title)
        E3RootObject.init(self, **kwargs)

    def SetNextPoint(self, x, y, dy = 0., dx = 0.):
        """
        """
        n = self.GetN()
        self.SetPoint(n, x, y)
        self.SetPointError(n, dx, dy)
