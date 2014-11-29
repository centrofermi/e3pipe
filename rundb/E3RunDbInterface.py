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


import MySQLdb.connections
import os
import ConfigParser

from e3pipe.__logging__ import logger, abort
from e3pipe.__package__ import E3PIPE_RUNDB


class E3RunDbInterface(MySQLdb.connections.Connection):

    """ Basic interface to the run database.
    """

    CFG_FILE_PATH = os.path.join(E3PIPE_RUNDB, 'rundb.cfg')

    def __init__(self):
        """ Constructor.
        """
        if not os.path.exists(self.CFG_FILE_PATH):
            abort('Could not find configuration file %s' % self.CFG_FILE_PATH)
        logger.info('Reading db configuration file %s...' % self.CFG_FILE_PATH)
        parser = ConfigParser.ConfigParser()
        parser.read(self.CFG_FILE_PATH)
        try:
            host = parser.get('General', 'host')
            user = parser.get('General', 'user')
            dbname = parser.get('General', 'dbname')
            pwd = parser.get('General', 'pwd')
        except ConfigParser.NoOptionError, e:
            abort(e)
        logger.info('Connecting to %s on %s (as %s)' % (dbname, host, user))
        MySQLdb.connections.Connection.__init__(self, host, user, pwd, dbname)
        logger.info('Done, setting up cursor...')
        self.__Cursor = self.cursor()
        logger.info('Interface to the run database ready.')

    def execute(self, query, commit = True):
        """ Execute a query.
        """
        logger.info('About to execute "%s"...' % query)
        if commit:
            try:
                self.__Cursor.execute(query)
                self.commit()
            except Exception, e:
                logger.error('%s, rolling back change...' % e)
                self.rollback()
        else:
            self.__Cursor.execute(query)
       
    def fetchall(self):
        """ Fetch all the values from the cursor.
        """
        return self.__Cursor.fetchall()

    def close(self):
        """ Close the connection to the database, if open.
        """
        if self.open:
            logger.info('Closing cobbection to db...')
            MySQLdb.connections.Connection.close(self)

    def __del__(self):
        self.close()



if __name__ == '__main__':
    db = E3RunDbInterface()
    numrows = db.execute('SELECT * FROM telescope_id_table')
    print numrows
    for row in db.fetchall():
        print row
    db.close()
