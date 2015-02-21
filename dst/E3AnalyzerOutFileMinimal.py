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


from e3pipe.dst.E3TextTupleField import E3TextTupleField
from e3pipe.dst.E3TextTupleRow import E3TextTupleRow
from e3pipe.dst.E3TextTupleBase import E3TextTupleBase
from e3pipe.__logging__ import logger
from e3pipe.config.__dst__ import MAX_GOOD_CHISQUARE



class E3AnalyzerOutFileMinimal(E3TextTupleBase):

    """ Class encapsulating a .out file from the analyizer.

    The main purpose of this class is to be able to iterate on a .out file
    getting out structured objects rather than text lines, e.g.
    """
    
    def __init__(self, filePath):
        """ Constructor.
        
        Note we call the base class next() method once, right at the
        beginning, to skip the file header.
        """
        E3TextTupleBase.__init__(self, filePath, '.out')
        self.__CurrentLine = 1
        self.__MinTimestamp = None
        self.__MaxTimestamp = None
        file.next(self)

    def minTimestamp(self):
        """ Return the smallest timestamp found so far.
        """
        return self.__MinTimestamp

    def maxTimestamp(self):
        """ Return the largest timestamp found so far.
        """
        return self.__MaxTimestamp

    def __split(self, line):
        """
        """
        if 'hit' in line:
            return None
        try:
            data = [int(item) for item in line.split(None, 4)[:4]]
        except:
            data = None
        return data

    def next(self):
        """ Overloaded next() method.
        
        The parsing of this thing has become so complicated that we
        essentially give up on using the general machinery put in place
        with the E3TextTupleRow class. Here we just pass a plain dictionary
        out of the iterator to fill the output ROOT tree.
        """
        data = self.__split(file.next(self))
        self.__CurrentLine += 1
        while data is None:
            data = self.__split(file.next(self))
            self.__CurrentLine += 1
        return data



def test(filePath, numEvents = 20):
    """ Test code.
    """
    f = E3AnalyzerOutFileMinimal(filePath)
    for i in range(numEvents):
        print f.next()



if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser()
    (opts, args) = parser.parse_args()
    for filePath in args:
        test(filePath)
