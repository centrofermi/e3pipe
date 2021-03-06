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


from e3pipe.dst.E3AnalyzerOutFileMinimal import E3AnalyzerOutFileMinimal


def test(*args):
    """
    """
    inputFiles = [E3AnalyzerOutFileMinimal(arg) for arg in args]
    labels = [arg.split('_')[-1].replace('.out', '') for arg in args]
    while 1:
        _curlist = []
        _allthesame = True
        for f in inputFiles:
            _data = '%5d%10d%15d%15d' % tuple(f.next())
            if len(_curlist) and _data != _curlist[-1]:
                _allthesame = False
            _curlist.append(_data)
        if not _allthesame:
            for i, _data in enumerate(_curlist):
                print '%5s' % labels[i], _data




if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser()
    (opts, args) = parser.parse_args()
    test(*args)
