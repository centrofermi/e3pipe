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


HTML_HEADER = \
"""
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"
          "http://www.w3.org/TR/html4/strict.dtd">

<html lang="en">
  
  <head>
    <meta http-equiv="content-type" content="text/html; charset=iso-8859-1">
    <title>EEE DQM report</title>
    <link rel="stylesheet" href="e3pipe.css" type="text/css" media="all">
  </head>
  <body>

"""

HTML_FOOTER = \
"""
  </body>
</html>
"""


class E3HtmlOutputFile(file):

    """ Utility class for html output.
    """

    def __init__(self, filePath):
        """ Constructor.
        """
        logger.info('Opening output file %s...' % filePath)
        file.__init__(self, filePath, 'w')
        self.write(HTML_HEADER)

    def close(self):
        """
        """
        self.write(HTML_FOOTER)
        file.close(self)
