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
import numpy

from e3pipe.__logging__ import logger
from e3pipe.root.E3TreePlotter import E3TreePlotter


ROOT_TO_NUMPY_DICT = {'C': '',
                      'B' : 'int8',
                      'b' : 'uint8',
                      'S' : 'int16',
                      's' : 'uint16',
                      'I' : 'int32',
                      'i' : 'uint32',
                      'F' : 'float32',
                      'D' : 'float64',
                      'L' : 'int64',
                      'l' : 'uint64',
                      'O' : 'bool_'
                  }

def root2numpy(rootType):
    """ Convert a ROOT branch type into the corresponding numpy type.
    """
    return ROOT_TO_NUMPY_DICT[rootType]




class E3Tree(ROOT.TTree, E3TreePlotter):
    
    """ Small wrapper around the ROOT.Tree class.

    Compared to the base class, this class provides some additional facility to
    create and manipulate branches and it's mainly used to write ROOT tree
    to file.

    The list of supported types, straight from the ROOT documentation, is:
    - C : a character string terminated by the 0 character
    - B : an 8 bit signed integer (Char_t)
    - b : an 8 bit unsigned integer (UChar_t)
    - S : a 16 bit signed integer (Short_t)
    - s : a 16 bit unsigned integer (UShort_t)
    - I : a 32 bit signed integer (Int_t)
    - i : a 32 bit unsigned integer (UInt_t)
    - F : a 32 bit floating point (Float_t)
    - D : a 64 bit floating point (Double_t)
    - L : a 64 bit signed integer (Long64_t)
    - l : a 64 bit unsigned integer (ULong64_t)
    - O : [the letter 'o', not a zero] a boolean (Bool_t)
    """

    NAME = 'Tree'
    BRANCHES = []
    ALIAS_DICT = {}

    def __init__(self, title = None):
        """ Constructor.
        """
        ROOT.TTree.__init__(self, self.NAME, title or self.NAME)
        E3TreePlotter.__init__(self)
        self.__ArrayDict = {}
        for branch in self.BRANCHES:
            self.addBranch(branch.Name, branch.Type)
        self.BranchList = [branch.Name for branch in self.BRANCHES]
        for key, value in self.ALIAS_DICT.items():
            logger.info('Setting alias "%s" -> "%s"...' % (key, value))
            self.SetAlias(key, value)

    def addBranch(self, branchName, branchType):
        """ Add a branch to the output tree.
        """
        branchTitle = '%s/%s' % (branchName, branchType)
        logger.info('Adding branch %s to %s...' % (branchTitle, self.GetName()))
        a = numpy.array([0], dtype = root2numpy(branchType))
        self.__ArrayDict[branchName] = a
        self.Branch(branchName, a, branchTitle)

    def fillRow(self, row):
        """ Fill a row of the tree.

        This really set the value for all the branches of the tree and calls the
        ROOT.TTree.Fill() method at the end.

        The argument row is essentially a dictionary which is supposed to
        contain all the branch names as keys (note that the loop is actually
        done over the branch names, so that the dictionary can contain a
        superset of the branch names as its keys.)
        """
        for branchName in self.BranchList:
            self.setValue(branchName, row[branchName])
        self.Fill()

    def setValue(self, branchName, value):
        """ Set the value of a specific array.
        """
        self.__ArrayDict[branchName][0] = value

    def value(self, branchName, entry = None):
        """ Return the value of a specific array.
        """
        if entry is not None:
            self.GetEntry(entry)
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
