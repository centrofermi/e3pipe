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
import ROOT

from e3pipe.__logging__ import logger, abort
from e3pipe.root.E3Chain import E3Chain
from e3pipe.mc.E3McEventTree import E3McEventTree


class E3McEventChain(E3Chain):

    """ Small wrapper around the TChain class.
    """

    TREE_NAME = E3McEventTree.NAME
    ALIAS_DICT = E3McEventTree.ALIAS_DICT

    def __init__(self, *fileList):
        """ Constructor.
        """
        E3Chain.__init__(self, self.TREE_NAME, *fileList)
        



def test(*fileList):
    """ Test program.
    """
    t = E3McEventChain(*fileList)



if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser()
    (opts, args) = parser.parse_args()
    test(*args)
