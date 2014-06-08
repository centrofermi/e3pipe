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


class E3TextTupleBase(E3InputFile):

    """ Class encapsulating a file containing a text tuple.

    The main purpose of this class is to be able to iterate on a text tuple file
    getting out structured objects rather than text lines.
    """

    ROW_DESCRIPTOR = None

    def __init__(self, filePath, extension):
        """ Constructor.
        """
        E3InputFile.__init__(self, filePath, extension)

    def next(self):
        """ Overloaded next() method.

        Here we serve an actual ROW_DESCRIPTOR object (whatever that is) rather
        than a line of text.
        """
        return self.ROW_DESCRIPTOR(file.next(self))
