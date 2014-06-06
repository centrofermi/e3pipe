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



from e3pipe.dst.E3InputFile import E3InputFile
from e3pipe.dst.E3Event import E3Event



class E3AnalyzerOutFile(E3InputFile):

    """ Class encapsulating a .out file from the analyizer.

    The main purpose of this class is to be able to iterate on a .out file
    getting out E3Event objects rather than text lines, e.g.

    f = E3AnalyzerOutFile(filePath)
    e = f.next()

    will return an E3Event object e.
    """

    def __init__(self, filePath):
        """ Constructor.
        
        Note we call the base class next() method once, right at the
        beginning, to skip the file header.
        """
        E3InputFile.__init__(self, filePath, '.out')
        file.next(self)

    def next(self):
        """ Overloaded next() method.

        Here we serve an actual E3Event object rather than a line of text.
        """
        return E3Event(file.next(self))



def test(filePath):
    """ Test code.
    """
    f = E3AnalyzerOutFile(filePath)
    print f.next()



if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser()
    (opts, args) = parser.parse_args()
    for filePath in args:
        test(filePath)
