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


from e3pipe.rundb.E3RunDbInterface import E3RunDbInterface
from e3pipe.config.__stations__ import E3_STATION_DICT
from e3pipe.__logging__ import logger


def e3populateTelescopeIdTable():
    """
    """
    db = E3RunDbInterface()
    table = 'telescope_id_table'
    logger.info('Truncating table %s...' % table)
    query = 'TRUNCATE TABLE %s' % table
    db.execute(query, commit = True)
    logger.info('Populating %s...' % table)
    for stationName, stationId in E3_STATION_DICT.items():
        query = 'INSERT INTO %s (id, name) VALUES(%d, "%s");' %\
                (table, stationId, stationName)
        db.execute(query, commit = True)
    logger.info('Done.')
    query = 'SELECT * from %s;' % table
    db.execute(query)
    for row in db.fetchall():
        print row
    db.close()



if __name__ == '__main__':
    e3populateTelescopeIdTable()
