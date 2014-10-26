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
import numpy
import ROOT

from e3pipe.__logging__ import logger, abort
from e3pipe.root.E3RootFileBase import E3RootFileBase
from e3pipe.root.E3H1D import E3H1D
from e3pipe.root.E3Tree import ROOT_TO_NUMPY_DICT


class E3Chain(ROOT.TChain):

    """ Small wrapper around the TChain class.

    TODO: we probably want to move all the plotting stuff to a base
    class so that we can use it both when while writing and while
    reading trees.
    """

    ALIAS_DICT = {}

    def __init__(self, treeName, *fileList):
        """ Constructor.
        """
        logger.info('Initializing TChain %s...' % treeName)
        ROOT.TChain.__init__(self, treeName)
        for filePath in fileList:
            self.Add(filePath)
        logger.info('Done, %d entries found.' % self.GetEntries())
        for key, value in self.ALIAS_DICT.items():
            logger.info('Setting alias "%s" -> "%s"...' % (key, value))
            self.SetAlias(key, value)
        self.__ArrayDict = {}
        self.__TreeFormulaDict = {}

    def arrayValue(self, key):
        """ Return the content of an array.
        """
        return self.__ArrayDict[key][0]

    def formulaValue(self, key):
        """ Return the content of a TTreeFormula, evaluated for a given event.
        """
        return self.__TreeFormulaDict[key].EvalInstance()

    def value(self, key):
        """
        """
        try:
            return self.formulaValue(key)
        except:
            return self.arrayValue(key)

    def Add(self, filePath):
        """ Add a file to the chain.
        
        Note that we are doing some basic check, here, in order to try
        and prevent simple issues.
        """
        if not '*' in filePath:
            if not os.path.exists(filePath):
                abort('Could not find input file %s' % filePath)
            if not filePath.endswith(E3RootFileBase.EXTENSION):
                abort('Wrong file extension for input file %s (%s expected)' %\
                      (filePath, E3RootFileBase.EXTENSION))
        logger.info('Adding %s...' % filePath)
        ROOT.TChain.Add(self, filePath)

    def selectBranches(self, *branches):
        """ 
        """
        logger.info('Disabling all branches...')
        self.SetBranchStatus('*', 0)
        for branch in branches:
            logger.info('Enabling branch %s...' % branch)
            self.SetBranchStatus(branch, 1)

    def __setupArray(self, branch):
        """ Setup an array to be attached to a tree branch.
        """
        branchTitle = branch.GetTitle()
        (branchName, branchType) = branchTitle.split('/')
        if self.GetBranchStatus(branchName):
            logger.info('Setting up numpy array for %s...' % branchTitle)
            x = numpy.empty((1,), ROOT_TO_NUMPY_DICT[branchType])
            self.__ArrayDict[branchName] = x
            self.SetBranchAddress(branchName, x)

    def setupArrays(self):
        """ Setup the arrays to be attached to all the enabled tree
        branches.
        """
        logger.info('Creating array(s) to be attached to the branches...')
        for branch in self.GetListOfBranches():
            self.__setupArray(branch)
        logger.info('Done, arrays ready.')

    def __setupTreeFormula(self, key, value):
        """ Setup a TTree formula.
        """
        logger.info('Compiling formula for %s -> %s...' % (key, value))
        formula = ROOT.TTreeFormula('TTF_%s' % key, value, self)
        self.__TreeFormulaDict[key] = formula

    def setupTreeFormulae(self):
        """ Setup tree formulae for all the aliases.
        """
        logger.info('Compiling TTreeFormula objects for the aliases...')
        for key, value in self.ALIAS_DICT.items():
            self.__setupTreeFormula(key, value)
        logger.info('Done.')

    def writeAscii(self, outputFilePath, delimiter = ','):
        """ Write the chain to a text file.
        """
        logger.info('Writing %s to %s...' % (self.GetName(), outputFilePath))
        outputFile = open(outputFilePath, 'w')
        branchList = []
        formatList = []
        for branch in self.GetListOfBranches():
            (branchName, branchType) = branch.GetTitle().split('/')
            if self.GetBranchStatus(branchName):
                branchList.append(branch.GetName())
                if branchType == 'D':
                    formatList.append('%.12e')
                elif branchType == 'F':
                    formatList.append('%.6e')
                else:
                    formatList.append('%d')
        outputFile.write('#')
        for branchName in branchList[:-1]:
            outputFile.write('%s,' % branchName)
        outputFile.write('%s\n' % branchList[-1])
        rowSpecifier = zip(branchList, formatList)
        for i in xrange(self.GetEntries()):
            self.GetEntry(i)
            for branchName, fmt in rowSpecifier[:-1]:
                val = fmt % self.arrayValue(branchName)
                outputFile.write('%s,' % val)
            val = formatList[-1] % self.arrayValue(branchList[-1])
            outputFile.write('%s\n' % val)
        outputFile.close()
        logger.info('Output file closed, done.')




def test(filePath, treeName):
    """ Test program.
    """
    t = E3Chain(filePath, treeName)
    print t



if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser()
    (opts, args) = parser.parse_args()
    for filePath in args:
        test(filePath, 'Events')
