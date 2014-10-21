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


import logging
import sys
import time

logger = logging.getLogger('e3pipe')
logger.setLevel(logging.DEBUG)

# Terminal setting.
consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(logging.DEBUG)
consoleFormatter = logging.Formatter(">>> %(message)s")
consoleHandler.setFormatter(consoleFormatter)
logger.addHandler(consoleHandler)



class E3FileFormatter(logging.Formatter):
    
    """ Logging file formatter class.
    """

    def format(self, record):
        """ Overloaded format method.
        """
        timestamp = time.strftime('%d %b %Y @ %H:%M:%S',
                                  time.localtime(record.created))
        ms = 1000*(record.created - int(record.created))
        timestamp = '%s.%d' % (timestamp, ms)
        text = '---%s (from %s.%s)\n[%s] %s\n' %\
            (timestamp, record.module, record.funcName, record.levelname,
             record.msg)
        return text



class E3FileHandler(logging.FileHandler):
    
    """ Logging file handler class.
    """

    def __init__(self, filePath, mode = 'a', encoding = None, delay = False):
        """ Constructor.
        """
        logger.info('Opening output log file %s...' % filePath)
        logging.FileHandler.__init__(self, filePath, mode, encoding, delay)
        self.setLevel(logging.DEBUG)
        self.setFormatter(E3FileFormatter())
        logger.addHandler(self)

    def close(self):
        """
        """
        if self in logger.handlers:
            logger.removeHandler(self)
            logging.FileHandler.close(self)
            logger.info('Output log file %s closed.' % self.baseFilename)




def abort(message = ''):
    """ Abort the execution.
    """
    if message != '':
        message = '%s. Abort.' % message
    else:
        message = 'Abort.'
    sys.exit(message)


def startmsg():
    """ Print the start message.
    """
    from e3pipe.__version__ import TAG, BUILD_DATE
    print('\n    Welcome to e3pipe version %s (built on %s).\n' %\
              (TAG, BUILD_DATE))
    print('    Copyright (C) 2014 Luca Baldini '
          '(luca.baldini@pi.infn.it)\n\n'
          '    e3pipe comes with ABSOLUTELY NO WARRANTY.\n'
          '    This is free software, and you are welcome to redistribute '
          'it under certain\n'
          '    conditions. See the LICENSE file for details.\n\n'
          '    Visit https://github.com/centrofermi/e3pipe '
          'more information.\n')


