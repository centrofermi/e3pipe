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


E3_STATION_DICT = {
    'ALTA-01': 1,
    'ANCO-01': 2,
    'AREZ-01': 3,
    'BARI-01': 4,
    'BOLO-01': 5,
    'BOLO-02': 6,
    'BOLO-03': 7,
    'BOLO-04': 8,
    'CAGL-01': 9,
    'CAGL-02': 10,
    'CAGL-03': 11,
    'CATA-01': 12,
    'CATA-02': 13,
    'CATZ-01': 14,
    'CERN-01': 15,
    'CERN-02': 16,
    'COSE-01': 17,
    'FRAS-01': 18,
    'FRAS-02': 19,
    'GROS-01': 20,
    'GROT-01': 21,
    'LAQU-01': 22,
    'LAQU-02': 23,
    'LECC-01': 24,
    'LECC-02': 25,
    'LECC-03': 26,
    'LODI-01': 27,
    'PISA-01': 28,
    'PARM-01': 29,
    'PATE-01': 30,
    'REGG-01': 31,
    'ROMA-01': 32,
    'ROMA-02': 33,
    'SALE-01': 34,
    'SAVO-01': 35,
    'SAVO-02': 36,
    'SAVO-03': 37,
    'TERA-01': 38,
    'TORI-01': 39,
    'TORI-02': 40,
    'TORI-03': 41,
    'TORI-04': 42,
    'TRAP-01': 43,
    'TREV-01': 44, 
    'TRIN-01': 45,
    'VIAR-01': 46,
    'VIAR-02': 47
}


E3_ACTIVE_STATIONS = [
    'ALTA-01',
    'BARI-01',
    'BOLO-03',
    'CAGL-01',
    'CAGL-02',
    'CATA-02',
    'CATZ-01',
    'FRAS-02',
    'GROS-01',
    'LECC-01',
    'LECC-02',
    'LODI-01',
    #'PISA-01',
    'SAVO-01',
    'SAVO-02',
    'TORI-04',
    'TRAP-01',
    'TRIN-01',
    'VIAR-01',
    'VIAR-02'
]


if __name__ == '__main__':
    print E3_STATION_DICT
    print E3_ACTIVE_STATIONS
    print len(E3_STATION_DICT)
    print len(E3_ACTIVE_STATIONS)
