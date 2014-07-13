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


from e3pipe.__logging__ import logger
from e3pipe.dst.E3InputFile import E3InputFile


class E3AnalyzerSumFile(E3InputFile):

    """ Class encapsulating a .sum file from the analyzer.

    It is clear that the .sum file was not designed to be parsed by a program,
    so there's really much we can do except go patiently line by line.
    """

    def __init__(self, filePath):
        """ Constructor.
        
        Note that, at this point, we try and store all the data into a gigantic
        dictionary.
        """
        E3InputFile.__init__(self, filePath, '.sum')
        self.__parse()

    def __add(self, key, value):
        """ Add a piece of data to the underlying dictionary.
        """
        self.__Data[key] = value

    def __parse(self):
        """ Main parsing method.

        Note that we are actually skipping some of the data along the way.
        We might want to come back and create an exact in-memory replica of the
        sum file.

        And we might probably devise a more clever way to do it than repeating
        the same block of code many times.
        """
        self.__Data = {}
        logger.info('Parsing file content...')
        self.__add('NumEvents', self.nextval(int))
        self.__add('NumGpsEvents', self.nextval(int))
        for i in range(5):
            line = self.next()
        # Hit multiplicity chamber BOTTOM.
        line = self.next()
        hist = {}
        while not 'MIDDLE' in line:
            mul, evts = [int(item.strip()) for item in line.split()]
            hist[mul] = evts
            line = self.next()
        self.__add('HitMultBot', hist)
        # Hit multiplicity chamber BOTTOM.
        line = self.next()
        hist = {}
        while not ('UP' in line or 'TOP' in line):
            mul, evts = [int(item.strip()) for item in line.split()]
            hist[mul] = evts
            line = self.next()
        self.__add('HitMultMid', hist)
        # Hit multiplicity chamber UP.
        line = self.next()
        hist = {}
        while not 'total' in line:
            mul, evts = [int(item.strip()) for item in line.split()]
            hist[mul] = evts
            line = self.next()
        self.__add('HitMultTop', hist)
        # Hit multiplicity chamber UP.
        line = self.next()
        hist = {}
        while not '*****' in line:
            mul, evts = [int(item.strip()) for item in line.split()]
            hist[mul] = evts
            line = self.next()
        self.__add('HitMultTotal', hist)
        for i in range(4):
            line = self.next()
        # Cluster multiplicity chamber BOTTOM.
        line = self.next()
        hist = {}
        while not 'MIDDLE' in line:
            mul, evts = [int(item.strip()) for item in line.split()]
            hist[mul] = evts
            line = self.next()
        self.__add('ClusterMultBot', hist)
        # Cluster multiplicity chamber BOTTOM.
        line = self.next()
        hist = {}
        while not ('UP' in line or 'TOP' in line):
            mul, evts = [int(item.strip()) for item in line.split()]
            hist[mul] = evts
            line = self.next()
        self.__add('ClusterMultMid', hist)
        # Cluster multiplicity chamber UP.
        line = self.next()
        hist = {}
        while not 'total' in line:
            mul, evts = [int(item.strip()) for item in line.split()]
            hist[mul] = evts
            line = self.next()
        self.__add('ClusterMultTop', hist)
        # Cluster multiplicity chamber UP.
        line = self.next()
        hist = {}
        while not 'time cuts' in line:
            mul, evts = [int(item.strip()) for item in line.split()]
            hist[mul] = evts
            line = self.next()
        self.__add('ClusterMultTotal', hist)
        logger.info('Done.')

    def data(self):
        """ Return the __Data class member.
        """
        return self.__Data

    def next(self):
        """ This essentially calls the base class next method and strips the
        leading/trailing white spaces and return carriages, which are
        irrelevant.
        """
        return E3InputFile.next(self).strip(' \n')

    def nextval(self, dataType):
        """ Since many of the lines in the input file are in the form
        "key val", we provide this convenience method splitting by a space
        and casting the value to a specific data type.
        """
        return dataType(self.next().split()[-1])

    def get(self, key, default = None):
        """ Retrieve data from the underlying dictionary.
        """
        return self.__Data.get(key, default)

    def __str__(self):
        """ Text formatting.
        """
        return '%s' % self.__Data
        



def test(filePath):
    """ Test code.
    """
    f = E3AnalyzerSumFile(filePath)
    print f



if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser()
    (opts, args) = parser.parse_args()
    for filePath in args:
        test(filePath)

