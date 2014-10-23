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
import sys
import ROOT

# Top-level settings.
STYLE_NAME  = 'EEE'
STYLE_TITLE = 'ROOT style for EEE'
PALETTE = 'Default'
TEXT_FONT = 43
TEXT_SIZE = 31
BIG_TEXT_SIZE = 1.5*TEXT_SIZE
LABEL_TEXT_SIZE = 0.9*TEXT_SIZE
LEGEND_TEXT_SIZE = 0.9*TEXT_SIZE
SMALL_TEXT_SIZE = 0.8*TEXT_SIZE
SMALLER_TEXT_SIZE = 0.7*TEXT_SIZE
SMALLEST_TEXT_SIZE = 0.6*TEXT_SIZE
CANVAS_DEF_WIDTH  = 840
CANVAS_DEF_HEIGHT = 600
CANVAS_RIGHT_MARGIN = 0.04
CANVAS_TOP_MARGIN = 0.08
CANVAS_LEFT_MARGIN = 0.125*TEXT_SIZE/31.
CANVAS_BOTTOM_MARGIN = 0.130*TEXT_SIZE/31.

# Create a new style using the functionalities implemented in Eric's package.
STYLE = ROOT.TStyle(STYLE_NAME, STYLE_TITLE)
STYLE.SetPadColor(ROOT.kWhite)
STYLE.SetPadTickX(1)
STYLE.SetPadTickY(1)
STYLE.SetPadBorderMode(0)
STYLE.SetFrameFillColor(ROOT.kWhite)
STYLE.SetTitleFillColor(ROOT.kWhite)
STYLE.SetCanvasColor(ROOT.kWhite)
STYLE.SetStatColor(ROOT.kWhite)
STYLE.SetLineWidth(2)
STYLE.SetHistLineWidth(2)
STYLE.SetMarkerStyle(6)
STYLE.SetFrameBorderMode(0)
STYLE.SetCanvasBorderMode(0)
STYLE.SetTitleBorderSize(0)
STYLE.SetOptTitle(0)
STYLE.SetOptStat(111111)
STYLE.SetTitleXOffset(1.1)
STYLE.SetTitleYOffset(1.25)
STYLE.SetTitleOffset(1.25,'Z')
STYLE.SetLegendBorderSize(0)
STYLE.SetPadRightMargin(CANVAS_RIGHT_MARGIN)
STYLE.SetPadTopMargin(CANVAS_TOP_MARGIN)
STYLE.SetPadLeftMargin(CANVAS_LEFT_MARGIN)
STYLE.SetPadBottomMargin(CANVAS_BOTTOM_MARGIN)
STYLE.SetStatBorderSize(0)
STYLE.SetStatFont(TEXT_FONT)
STYLE.SetStatFontSize(SMALLER_TEXT_SIZE)
STYLE.SetStatY(0.88)
STYLE.SetStatX(0.93)
STYLE.SetGridColor(ROOT.kGray + 1)
STYLE.SetGridStyle(2)
STYLE.SetStatStyle(0)
STYLE.SetMarkerStyle(1)
STYLE.SetCanvasDefW(CANVAS_DEF_WIDTH)
STYLE.SetCanvasDefH(CANVAS_DEF_HEIGHT)

# Text Font and Precision
# The text font code is combination of the font number and the precision.
#
#   Text font code = 10*fontnumber + precision
#
# Font numbers must be between 1 and 14.
#
# The precision can be:
# 0 fast hardware fonts (steps in the size)
# 1 scalable and rotatable hardware fonts (see below)
# 2 scalable and rotatable hardware fonts
# 3 scalable and rotatable hardware fonts. Text size is given in pixels. 
STYLE.SetTextFont(TEXT_FONT)
STYLE.SetTextSize(TEXT_SIZE)
STYLE.SetTitleFont(TEXT_FONT, 'XYZ')
STYLE.SetTitleSize(TEXT_SIZE, 'XYZ')
STYLE.SetLabelFont(TEXT_FONT, 'XYZ')
STYLE.SetLabelSize(LABEL_TEXT_SIZE, 'XYZ')
STYLE.SetTitleYOffset(1.16)
STYLE.SetTitleXOffset(1.08)
STYLE.SetTitleOffset(1.0, 'Z')

# Apply the style
ROOT.gROOT.SetStyle(STYLE_NAME)
ROOT.gROOT.ForceStyle()

ROOT_OBJECT_POOL = []

def store(rootObject):
    ROOT_OBJECT_POOL.append(rootObject)

from e3pipe.__logging__ import logger

def cleanup():
    """
    """
    global ROOT_OBJECT_POOL
    logger.info('Cleaning up ROOT pool...')
    for obj in ROOT_OBJECT_POOL:
        if isinstance(obj, ROOT.TFile):
            logger.info('Closing %s...' % obj.GetName())
            obj.Close()
        ROOT_OBJECT_POOL.remove(obj)

def setupBox(box, x, y, numRows, width = 0.25):
    """ Setup a stat box or a fit box with a given number of rows.
    (x, y) is the top-left corner of the box.
    """
    box.SetX1NDC(x)
    box.SetX2NDC(x + width)
    box.SetY1NDC(y - numRows*TLegend.ROW_SPACING)
    box.SetY2NDC(y)
    ROOT.gPad.Modified()
    ROOT.gPad.Update()


def setupTimeDisplay(plot, **kwargs):
    """ Setup the x-axis labels for strip charts.
    """
    plot.GetXaxis().SetNdivisions(kwargs.get('Ndivisions', 504))
    plot.GetXaxis().SetLabelOffset(kwargs.get('LabelOffset', 0.04))
    plot.GetXaxis().SetTimeFormat('#splitline{%d/%m/%y}{%H:%M:%S}')
    plot.SetStats(False)

