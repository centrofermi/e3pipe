#!/usr/bin/env python
# *********************************************************************
# * Copyright (C) 2012 Luca Baldini (luca.baldini@pi.infn.it)         *
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


from e3pipe.root.__ROOT__ import *
from e3pipe.root.E3Latex  import E3Latex


class E3Logo:

    """ EEE logo to be put on a ROOT canvas.

    We haven't made a huge effort, yet, to make the logo scalable or
    anything like that. It is made of three pieces and we realy on the
    TLatex alignmnent for the relative positioning.
    """

    def __init__(self, x = 0.75, y = 0.99, subtitle = 'Powered by e3py',
                 color = ROOT.kBlue, shadowColor = ROOT.kGray):
        """
        """
        self.BigPrint = E3Latex(x, y, 'EEE', NDC = True, TextAlign = 33,
                                TextSize = BIG_TEXT_SIZE, TextColor = color)
        self.Shadow = E3Latex(x, y, 'EEE', NDC = True, TextAlign = 33,
                              TextSize = BIG_TEXT_SIZE, TextColor = shadowColor)
        self.Shadow.shift(0.0075, -0.0075)
        text = '#splitline{  Extreme Energy Events}{  %s}' % subtitle
        self.SmallPrint = E3Latex(x, y, text, NDC = True, TextAlign = 13,
                                  TextSize = SMALLEST_TEXT_SIZE,
                                  TextColor = color)
        
    def Draw(self, opts = ''):
        """
        """
        self.Shadow.Draw(opts)
        self.BigPrint.Draw(opts)
        self.SmallPrint.Draw(opts)


def test():
    logo = E3Logo()
    logo.Draw()


if __name__ == '__main__':
    test()
