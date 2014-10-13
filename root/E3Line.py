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



class E3Line(ROOT.TLine, E3RootObject):

    """ Wrapper around the ROOT.TLine object.
    """
    
    def __init__(self, x1, y1, x2, y2, **kwargs):
        """ Conctructor.
        """
        ROOT.TLine.__init__(self, x1, y1, x2, y2)
        self.init(**kwargs)



class E3YellowLine(E3Line):

    """ Yellow line (for alarm warnings).
    """

    DEFAULT_OPTIONS = {'LineColor': ROOT.kOrange}
    


class E3RedLine(E3Line):

    """ Red line (for alarm errors).
    """

    DEFAULT_OPTIONS = {'LineColor': ROOT.kRed}
