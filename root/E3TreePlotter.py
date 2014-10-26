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


import ROOT

from e3pipe.__logging__ import logger, abort
from e3pipe.root.E3H1D import E3H1D
from e3pipe.root.__ROOT__ import setupTimeDisplay
from e3pipe.root.E3Graph import E3Graph



class E3TreePlotter:

    """ Base class for making plots out of a root tree.
    """

    def __init__(self):
        """ Constructor.

        Note that we maintain both a dictionary and a list of the plots that
        have been made so that we can retrieve them according to the insertion
        order, if we want to.
        """
        self.__PlotDict = {}
        self.__PlotList = []

    def store(self, plot):
        """ Store a plot.
        """
        self.__PlotDict[plot.GetName()] = plot
        self.__PlotList.append(plot)

    def plot(self, name):
        """ Return a specific plot.
        """
        return self.__PlotDict[name]

    def plots(self):
        """ Return all the underlying plot objects.
        """
        return self.__PlotList

    def hist1d(self, expression, cut = '', name = None, title = None,
               xmin = None, xmax = None, xbins = 100, xpad = 0, **kwargs):
        """ Create a 1-dimensional histogram.
        """
        logger.info('Creating 1-d histogram for %s with cut "%s"...' %\
                    (expression, cut))
        kwargs['XTitle'] = kwargs.get('XTitle', expression)
        kwargs['YTitle'] = kwargs.get('YTitle', 'Entries/bin')
        name = name or expression
        title = title or name
        if xmin is None or xmax is None:
            _xmin = self.GetMinimum(expression)
            _xmax = self.GetMaximum(expression)
            if _xmin == 0 and _xmax == 0:
                _xmax = 1
            _xrange = _xmax - _xmin
        if xmin is None:
            xmin = _xmin - xpad*_xrange
        if xmax is None:
            xmax = _xmax + xpad*_xrange
        if xmin == xmax:
            if xmin == 0:
                xmin = -0.5
                xmax = 0.5
            else:
                xmin -= 0.1*xmin
                xmax += 0.1*xmax
        hist = E3H1D(name, title, xbins, xmin, xmax, **kwargs)
        self.Project(name, expression, cut)
        self.store(hist)
        return hist

    def hist2d(self, expression, cut = '', **kwargs):
        """ Create a 2-dimensional histogram.
        """
        pass

    def stripChart(self, branchName, errors = False, **kwargs):
        """ Create a strip chart.

        Note that, in order for this to work, the TTree/TChain class
        must have a stripChartTime() method defined.
        """
        title = kwargs.get('YTitle', None) or branchName
        g = E3Graph(branchName, title)
        for i in xrange(self.GetEntries()):
            self.GetEntry(i)
            x = self.stripChartTime()
            y = self.value(branchName)
            if errors:
                dy = self.arrayValue('%sErr' % branchName)
            else:
                dy = 0
            g.SetNextPoint(x, y, dy)
        setupTimeDisplay(g)
        g.GetYaxis().SetTitle(kwargs.get('YTitle', branchName))
        self.store(g)
        return g
