#!/usr/bin/env python
# *********************************************************************
# * Copyright (C) 2014 Luca Baldini (luca.baldini@pi.infn.it)         *
# *                                                                   *
# * For the license terms see the file LICENCE, distributed           *
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


import ROOT
import array

from e3pipe.__logging__ import logger


class E3Tree(ROOT.TTree):
    
    """ Small wrapper around the ROOT.Tree class.

    Compared to the base class, this class provides some additional facility to
    create and manipulate branches and it's mainly used to write ROOT tree
    to file.
    """

    def __init__(self, name, title = None):
        """ Constructor.
        """
        ROOT.TTree.__init__(self, name, title or name)
        self.__ArrayDict = {}

    def addBranch(self, branchName, branchType):
        """ Add a branch to the output tree.
        """
        branchTitle = '%s/%s' % (branchName, branchType)
        logger.info('Adding branch %s to %s...' % (branchTitle, self.GetName()))
        a = array.array(branchType.lower(), [0])
        self.__ArrayDict[branchName] = a
        self.Branch(branchName, a, branchTitle)

    def setValue(self, branchName, value):
        """ Set the value of a specific array.
        """
        self.__ArrayDict[branchName][0] = value

    def getValue(self, branchName):
        """ Return the value of a specific array.
        """
        return self.__ArrayDict[branchName][0]




def test():
    """ Test code.
    """
    t = E3Tree('Tree')
    t.addBranch('Var1', 'I')
    t.addBranch('Var2', 'F')
    for i in range(10):
        t.setValue('Var1', i)
        t.setValue('Var2', i**0.5)
        t.Fill()
    t.Draw('Var2')
    raw_input('Press enter to exit')



if __name__ == '__main__':
    test()
