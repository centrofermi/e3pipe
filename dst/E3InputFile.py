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

from e3pipe.__logging__ import logger, abort



class E3InputFile(file):

    """ Small convenience base class for input text files.

    This will essentially check that a file exists and, possibly, that
    it has the right extension.
    """

    def __init__(self, filePath, extension = None):
        """
        """
        if not os.path.exists(filePath):
            abort('Could not find input file %s' % filePath)
        if extension is not None and not filePath.endswith(extension):
            abort('Wrong file extension for input file %s (%s expected)' %\
                  (filePath, extension))
        logger.info('Opening input file %s...' % filePath)
        file.__init__(self, filePath)



def test(filePath):
    """ Test program.
    """
    f = E3InputFile(filePath)
    print f.next()



if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser()
    (opts, args) = parser.parse_args()
    for filePath in args:
        test(filePath)
