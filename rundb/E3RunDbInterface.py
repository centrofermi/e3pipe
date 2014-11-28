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


import MySQLdb

from e3pipe.__logging__ import logger


class E3RunDbInterface:

    """ Basic interface to the run database.
    """

    def __init__(self, host, user, passwd, dbname):
        """ Constructor.
        """
        logger.info('Connecting to %s on %s (as %s)' % (dbname, host, user))
        self.__Database = MySQLdb.connect(host, user, passwd, dbname)
        logger.info('Done, setting up cursor...')
        self.__Cursor = self.__Database.cursor()
        logger.info('Interface to the run database ready.')

    def execute(self, query):
        """ Execute a query.
        """
        logger.info('About to execute "%s"...' % query)
        self.__Cursor.execute(query)
        



if __name__ == '__main__':
    db = E3RunDbInterface('131.154.96.193', 'eee', 'eee-monitoring',
                          'eee_rundb2')
    db.execute('SELECT * FROM telescope_id_table')
