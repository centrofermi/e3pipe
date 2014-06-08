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
        


class E3TextTupleRow(dict):

    """ Basic data structure encapsulating a row of a text ntuple (e.g., a
    row in the .out file from the analyzer).

    The row structure is encapsulated in the FIELDS class member, which is
    just a list of (name, type) tuples.

    This container is implemented as a dictionary as we will typically access
    the row fields by name, e.g., when converting the thing into a ROOT
    tree. However, we do provide facilities to represent an event as an ordered
    list of values as well.

    We provide a text-formatting facility, too.
    """
    
    FIELDS = []

    def __init__(self, data):
        """ Constructor.

        This essentially tranforms a line from a .out file into a fully-fledged
        E3Event object.
        """
        dict.__init__(self)
        for field, datum in zip(self.FIELDS, data.split()):
            self[field.Name] = field.Type(datum)
    
    def values(self):
        """ Return an ordered list of the field values.

        Note the order is dictated by the FIELD class member.
        """
        return [self[field.Name] for field in self.FIELDS]

    def __str__(self):
        """ Text formatting.
        """
        text = ''
        for field in self.FIELDS:
            text += '%15s = %s\n' % (field.Name, self[field.Name])
        return text

