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


from e3pipe.__logging__ import logger, abort
from e3pipe.root.E3H1D import E3H1D


class E3TreePlotter:

    """ Base class for making plots out of a root tree.
    """

    def __init__(self):
        """ Constructor.
        """
        self.__PlotDict = {}

    def plot(self, name):
        """ Return a specific plot.
        """
        return self.__PlotDict[name]

    def plots(self):
        """ Return all the underlying plot objects.
        """
        return self.__PlotDict.values()

    def hist1d(self, expression, cut = '', name = None, title = None,
               xmin = None, xmax = None, xbins = 100, xpad = 0, **kwargs):
        """ Create a 1-dimensional histogram.
        """
        logger.info('Creating 1-d histogram for %s...' % expression)
        kwargs['XTitle'] = kwargs.get('XTitle', expression)
        kwargs['YTitle'] = kwargs.get('YTitle', 'Entries/bin')
        name = name or expression
        title = title or name
        if xmin is None or xmax is None:
            _xmin = self.GetMinimum(expression)
            _xmax = self.GetMaximum(expression) 
            _xrange = _xmax - _xmin
        if xmin is None:
            xmin = _xmin - xpad*_xrange
        if xmax is None:
            xmax = _xmax + xpad*_xrange
        hist = E3H1D(name, title, xbins, xmin, xmax, **kwargs)
        self.Project(name, expression, cut)
        self.__PlotDict[hist.GetName()] = hist
        return hist

    def hist2d(self, expression, cut = '', **kwargs):
        """ Create a 2-dimensional histogram.
        """
        pass
