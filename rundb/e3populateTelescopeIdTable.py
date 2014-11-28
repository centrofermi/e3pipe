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


db = E3RunDbInterface('131.154.96.193', 'eee', 'eee-monitoring', 'eee_rundb2')
for stationName, stationId in E3_STATION_DICT.items():
    query = 'INSERT INTO telescope_id_table (id, name) VALUES(%d, "%s")' %\
            (stationId, stationName)
    db.execute(query)

