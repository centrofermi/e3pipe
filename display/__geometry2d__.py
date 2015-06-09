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


import math
import numpy

from e3pipe.__logging__ import logger
from e3pipe.root.__ROOT__ import *



def setupObject(obj, **kwargs):
    """ Setup a geometrical object.
    """
    for (key, value) in kwargs.items():
        try:
            if isinstance(value, str):
                value = '"%s"' % value
            exec('obj.Set%s(%s)' % (key, value))
        except AttributeError, e:
            logger.warn('Cannot process kwarg "%s = %s" (%s).' %\
                        (key, value, e))


def annotate(x, y, text, size = 1, ndc = False,
             align = 22, color = ROOT.kBlack, angle = 0):
    """ Custom annotations.
    """
    ROOT.gPad.annotate(x, y, text, size*0.65*LABEL_TEXT_SIZE, ndc, align,
                       color, angle)


def box(xc, yc, width, height, **kwargs):
    """ Draw a box.
    """
    x1 = xc - 0.5*width
    y1 = yc - 0.5*height
    x2 = xc + 0.5*width
    y2 = yc + 0.5*height
    b = ROOT.TBox(x1, y1, x2, y2)
    if not kwargs.get('FillColor'):
        kwargs['FillColor'] = ROOT.kWhite
    setupObject(b, **kwargs)
    store(b)
    b.Draw('l')
    return b


def trapezoid(xc, yc, topWidth, botWidth, height, **kwargs):
    """ Draw a trapezoid.
    """
    x = [xc - 0.5*topWidth, xc + 0.5*topWidth, xc + 0.5*botWidth,
         xc - 0.5*botWidth, xc - 0.5*topWidth]
    y = [yc + 0.5*height, yc + 0.5*height, yc - 0.5*height, yc - 0.5*height,
         yc + 0.5*height,]
    l = ROOT.TPolyLine(5, numpy.array(x), numpy.array(y))
    setupObject(l, **kwargs)
    store(l)
    l.Draw()
    return l


def circle(xc, yc, r, phimin = 0, phimax = 360, **kwargs):
    """ Draw an arc of a circle.
    """
    c = ROOT.TEllipse(xc, yc, r, r, phimin, phimax)
    if not kwargs.get('FillStyle'):
        kwargs['FillStyle'] = 0
    setupObject(c, **kwargs)
    store(c)
    c.Draw()
    return c


def arc(xc, yc, r, phimin = 0, phimax = 360, **kwargs):
    """ Draw an arc.
    """
    c = circle(xc, yc, r, phimin, phimax, **kwargs)
    c.SetNoEdges()
    return c


def line(x1, y1, x2, y2, extend1 = 0, extend2 = 0, curly = False, **kwargs):
    """ Draw a line.
    """
    if x2 != x1 and y2 != y1:
        theta = math.atan2((y2 - y1), (x2 - x1))
        x1 -= extend1*math.cos(theta)
        y1 -= extend1*math.sin(theta)
        x2 += extend2*math.cos(theta)
        y2 += extend2*math.sin(theta)
    if curly:
        l = ROOT.TCurlyLine(x1, y1, x2, y2, 0.01, 0.005)
        l.SetWavy()
    else:
        l = ROOT.TLine(x1, y1, x2, y2)
    setupObject(l, **kwargs)
    store(l)
    l.Draw()
    return l


def hline(xc, yc, length, **kwargs):
    """ Draw a horizontal line.
    """
    l = ROOT.TLine(xc - 0.5*length, yc, xc + 0.5*length, yc)
    setupObject(l, **kwargs)
    store(l)
    l.Draw()
    return l


def vline(xc, yc, length, **kwargs):
    """ Draw a horizontal line.
    """
    l = ROOT.TLine(xc, yc - 0.5*length, xc, yc + 0.5*length)
    setupObject(l, **kwargs)
    store(l)
    l.Draw()
    return l


def marker(x, y, markerStyle = 20, **kwargs):
    """ Draw a marker.
    """
    m = ROOT.TMarker(x, y, markerStyle)
    setupObject(m, **kwargs)
    store(m)
    m.Draw()
    return m

def arrow(x1, y1, x2, y2, **kwargs):
    """
    """
    a = ROOT.TArrow(x1, y1, x2, y2, 0.01, '-|>')
    setupObject(a, **kwargs)
    store(a)
    a.Draw()
    return a

def hquote(x1, x2, y):
    """
    """
    line(x1, y, x2, y, LineStyle = 7, LineWidth = 1)
    marker(x1, y, MarkerSize = 0.7)
    marker(x2, y, MarkerSize = 0.7)
    annotate(0.5*(x1 + x2), y - 2, '%.1f cm' % abs(x2 - x1), align = 23,
             size = 0.8)


def vquote(y1, y2, x):
    """
    """
    line(x, y1, x, y2, LineStyle = 7, LineWidth = 1)
    marker(x, y1, MarkerSize = 0.7)
    marker(x, y2, MarkerSize = 0.7)
    annotate(x + 2, 0.5*(y1 + y2), '%.1f cm' % abs(y2 - y1), align = 23,
             angle = 90, size = 0.8)



if __name__ == '__main__':
    from E3PhysicalCanvas import E3PhysicalCanvas
    c = E3PhysicalCanvas('c', 100, 100, logo = False)
    box(0, 0, 20, 2)
    hline(0, 0, 200)
    c.Update()
