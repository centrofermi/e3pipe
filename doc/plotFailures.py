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
from e3pipe.root.E3Canvas import E3Canvas
from e3pipe.root.E3H1D import E3H1D

import math


class dataset:

    def __init__(self, filePath, fileSize):
        self.FilePath = filePath
        self.FileSize = fileSize

    def __cmp__(self, other):
        if self.FileSize > other.FileSize:
            return 1
        return -1

    def __str__(self):
        return '%s (%d)' % (self.FilePath, self.FileSize)
    


if __name__ == '__main__':
    h139 = E3H1D('h139', 'Exit code 139', 100, 1, 9,
                 XTitle = 'log_{10}(File size [Byte])',
                 YTitle = 'Number of runs per bin')
    l139 = []
    for line in open('failures_139.dat'):
        filePath, size = line.strip('\n').split('\t')
        size = float(size)
        h139.Fill(math.log10(size))
        l139.append(dataset(filePath, size))
    c139 = E3Canvas('c139', Logy = True)
    h139.Draw()
    c139.annotate(0.15, 0.875, 'Analyzer segfault (139)')
    c139.Update()
    c139.save()
    l139.sort()
    print 'Biggest files for exit code 139:'
    for d in l139[-3:]:
        print d
    print
 
    h137 = E3H1D('h137', 'Exit code 137', 100, 1, 9,
                 XTitle = 'log_{10}(File size [Byte])',
                 YTitle = 'Number of runs per bin')
    l137 = []
    for line in open('failures_137.dat'):
        filePath, size = line.strip('\n').split('\t')
        size = float(size)
        h137.Fill(math.log10(size))
        l137.append(dataset(filePath, size))
    c137 = E3Canvas('c137', Logy = True)
    h137.Draw()
    c137.annotate(0.15, 0.875, 'Analyzer killed (137)')
    c137.Update()
    c137.save()
    l137.sort()
    print 'Biggest files for exit code 137:'
    for d in l137[-3:]:
        print d
    print

    l100 = []
    h100 = E3H1D('h100', 'Exit code 100', 100, 1, 9,
                 XTitle = 'log_{10}(File size [Byte])',
                 YTitle = 'Number of runs per bin')
    for line in open('failures_100.dat'):
        filePath, size = line.strip('\n').split('\t')
        size = float(size)
        h100.Fill(math.log10(size))
        l100.append(dataset(filePath, size))
    c100 = E3Canvas('c100', Logy = True)
    h100.Draw()
    c100.annotate(0.15, 0.875, 'No hits events (100)')
    c100.Update()
    c100.save()
    l100.sort()
    print 'Biggest files for exit code 100:'
    for d in l100[-3:]:
        print d
