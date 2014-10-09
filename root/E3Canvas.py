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


import time

from e3pipe.root.__ROOT__ import *
from e3pipe.root.E3RootObject import E3RootObject
from e3pipe.root.E3Latex import E3Latex
from e3pipe.root.E3Logo import E3Logo



class E3Canvas(ROOT.TCanvas, E3RootObject):

    """ Wrapper around the ROOT.TCanvas object.
    """

    DEFAULT_OPTIONS = {'Gridx': True,
                       'Gridy': True
    }
    
    def __init__(self, name, title = None, timestamp = False, **kwargs):
        """ Conctructor.
        """
        ROOT.TCanvas.__init__(self, name, title or name)
        self.init(**kwargs)
        self.Timestamp = timestamp
        self.Logo = E3Logo()

    def annotate(self, x, y, text, size = LABEL_TEXT_SIZE, ndc = True,
                 align = 11, color = ROOT.kBlack, angle = 0):
        """ Annotate the canvas with some text.
        """
        label = E3Latex(x, y, text, TextSize = size, NDC = ndc,
                        TextAlign = align, TextColor = color, TextAngle = angle)
        store(label)
        label.Draw()

    def Update(self):
        """ Overloaded method to update the canvas and write the style
        version, if in debug mode.
        """
        self.Logo.Draw()
        if self.Timestamp:
            self.annotate(0.02, 0.99, 'Created on %s' % time.asctime(),
                          size = SMALLEST_TEXT_SIZE, align = 13)
        ROOT.TCanvas.Update(self)
        
    def save(self, folderPath = None, formats = ['eps', 'pdf', 'png']):
        """ Save the canvas.
        """
        for format in formats:
            filePath = '%s.%s' % (self.GetName(), format)
            if folderPath is not None:
                filePath = os.path.join(folderPath, filePath)
            self.SaveAs(filePath)


def test():
    c = E3Canvas('ctest')
    h = ROOT.TH1F('htest', 'htest', 100, 0, 1)
    store(h)
    h.Draw()
    c.annotate(0.5, 0.5, 'Test annotation')
    c.Update()


if __name__ == '__main__':
    test()
