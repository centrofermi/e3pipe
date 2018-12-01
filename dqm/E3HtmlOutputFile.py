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


import time

from e3pipe.__logging__ import logger


HTML_HEADER = \
"""
<!DOCTYPE html>

<html lang="en">
  
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
<title>%s</title>
<link rel="stylesheet" href="%s" type="text/css" media="all">
</head>
<body>

<div id="header">
<h1>%s</h1>
</div>

<div id="container">
"""

HTML_FOOTER = \
"""
</div>

<div id="footer">
Extreme Energy Events (EEE) is powered by
<a href="https://github.com/centrofermi/e3pipe">e3pipe</a> version %s.<br>
This page validates as
<a href="https://validator.w3.org/check?uri=referer">HTML5</a> and 
<a href="https://jigsaw.w3.org/css-validator/check/referer">css level 3</a>.<br>
Generated on %s.
</div>
</body>
</html>
"""


def htmlAttributes(**kwargs):
    """ Format a python dictionary as a collection of html attributes.
    """
    attributes = ''
    for key, value in kwargs.items():
        attributes += '%s = %s ' % (key, value)
    return attributes.strip()

def htmlTableHeader(*args, **kwargs):
    """ Format a list of arguments as a html table header.
    """
    text = '<tr class="tableheader">'
    for arg in args:
        text += '<th>%s</th>' % arg
    text += '</tr>'
    return text



class E3HtmlOutputFile(file):

    """ Utility class for html output.
    """

    DEFAULT_CSS_FILE_PATH = 'e3pipe.css'
    DEFAULT_TITLE = 'EEE Data Quality Monitoring'
    DEFAULT_HEADER_TEXT = 'EEE DQM run report'

    def __init__(self, filePath, **kwargs):
        """ Constructor.
        """
        css = kwargs.get('css', self.DEFAULT_CSS_FILE_PATH)
        title = kwargs.get('title', self.DEFAULT_TITLE)
        header = kwargs.get('header', self.DEFAULT_HEADER_TEXT)
        logger.info('Opening output file %s...' % filePath)
        file.__init__(self, filePath, 'w')
        self.write(HTML_HEADER % (title, css, header))

    def section(self, title):
        """ Start a new section in the output file.
        """
        self.write('\n<h3>%s</h3>\n' % title)

    def li(self, text, **kwargs):
        """
        """
        self.write('<li %s>%s</li>\n' % (htmlAttributes(**kwargs), text))

    def image(self, filePath, **kwargs):
        """ Add an image to the output file.
        """
        self.write('<a href="%s"><img %s src="%s"/></a>\n' %\
                   (filePath, htmlAttributes(**kwargs), filePath))

    def close(self):
        """ Write the footer and close the file.
        """
        from e3pipe.__version__ import TAG
        self.write(HTML_FOOTER %\
                   (TAG, time.strftime('%A, %B %d %Y at %H:%M (%z)')))
        file.close(self)
