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
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">

<html lang="en">
  
<head>
<meta http-equiv="content-type" content="text/html; charset=iso-8859-1">
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
<a href="https://github.com/centrofermi/e3pipe">e3pipe</a>.<br>
This page validates as
<a href="http://validator.w3.org/check?uri=referer">HTML 4.01 strict</a> and 
<a href="http://jigsaw.w3.org/css-validator/check/referer">css level 3</a>.<br>
Generated on %s.
</div>
</body>
</html>
"""


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
        header = kwargs.get('text', self.DEFAULT_HEADER_TEXT)
        logger.info('Opening output file %s...' % filePath)
        file.__init__(self, filePath, 'w')
        self.write(HTML_HEADER % (title, css, header))

    def __attributes(self, **kwargs):
        """ Format a python dictionary as a collection of html attributes.
        """
        attributes = ''
        for key, value in kwargs.items():
            attributes += '%s = %s ' % (key, value)
        return attributes.strip()

    def section(self, title):
        """ Start a new section in the output file.
        """
        self.write('\n<h3>%s</h3>\n' % title)

    def li(self, text, **kwargs):
        """
        """
        self.write('<li %s>%s</li>\n' %\
                   (self.__attributes(**kwargs), text))

    def image(self, filePath, **kwargs):
        """ Add an image to the output file.
        """
        self.write('<a href="%s"><img %s src="%s"/></a>\n' %\
                   (filePath, self.__attributes(**kwargs), filePath))

    def close(self):
        """ Write the footer and close the file.
        """
        self.write(HTML_FOOTER % time.strftime('%A, %B %d %Y at %H:%M (%z)'))
        file.close(self)
