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


from e3pipe.__logging__ import logger


class E3RootObject:

    """ Generic ROOT object wrapper.
    
    This class only defines an init(**kwargs) method that loops over the
    keyword arguments and attempts at calling the appropriate underlying class
    methods.

    The basic idea is that, whenever a ROOT object has a "SetXXX(val)" method
    you can invoke it by passing the keyword argument "XXX = val".
    """

    DEFAULT_OPTIONS = {}

    def init(self, **kwargs):
        """ Workhorse class method.
        """
        for (key, value) in self.DEFAULT_OPTIONS.items():
            if not kwargs.has_key(key):
                kwargs[key] = value
        for (key, value) in kwargs.items():
            try:
                if isinstance(value, str):
                    value = '"%s"' % value
                exec('self.Set%s(%s)' % (key, value))
            except AttributeError, e:
                logger.warn('Cannot process kwarg "%s = %s" (%s).' %\
                                (key, value, e))
            
