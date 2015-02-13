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


""" Unique ID assigned to each station.
"""
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
    'VIAR-02': 47,
    'FRAS-03': 48
}


""" And now we invert the dict.
"""
E3_STATION_ID_DICT = {}
for key, value in E3_STATION_DICT.items():
    E3_STATION_ID_DICT[value] = key


E3_ACTIVE_STATIONS = [
    'ALTA-01',
    'BARI-01',
    'BOLO-03',
    'CAGL-01',
    'CAGL-02',
    'CAGL-03',
    'CATA-02',
    'CATZ-01',
    'FRAS-02',
    'GROS-01',
    'LAQU-01',
    'LAQU-02',
    'LECC-01',
    'LECC-02',
    'LODI-01',
    'PISA-01',
    'SAVO-01',
    'SAVO-02',
    'TORI-04',
    'TRAP-01',
    'TRIN-01',
    'VIAR-01',
    'VIAR-02'
]


E3_LOCATION_DICT = {
    'ALTA-01': {'lat': 40.823383333333, 'lon': 16.553683333333, 'alt': 541.0},
    #'ANCO-01': {'lat': , 'lon': , 'alt': },
    #'AREZ-01': {'lat': , 'lon': , 'alt': },
    'BARI-01': {'lat': 41.119150000000, 'lon': 16.871800000000, 'alt':  37.0},
    #'BOLO-01': {'lat': , 'lon': , 'alt': },
    #'BOLO-02': {'lat': , 'lon': , 'alt': },
    'BOLO-03': {'lat': 44.488650000000, 'lon': 11.347933333333, 'alt': 119.0},
    #'BOLO-04': {'lat': , 'lon': , 'alt': },
    'CAGL-01': {'lat': 39.229466666667, 'lon':  9.118066666667, 'alt':  49.0},
    'CAGL-02': {'lat': 39.230900000000, 'lon':  9.123916666667, 'alt':  34.0},
    'CAGL-03': {'lat': 39.208433333333, 'lon':  9.120583333333, 'alt':  83.0},
    #'CATA-01': {'lat': , 'lon': , 'alt': },
    'CATA-02': {'lat': 37.498750000000, 'lon': 15.061750000000, 'alt': 101.0},
    'CATZ-01': {'lat': 38.830666666667, 'lon': 16.637233333333, 'alt':  21.0},
    #'CERN-01': {'lat': , 'lon': , 'alt': },
    #'CERN-02': {'lat': , 'lon': , 'alt': },
    #'COSE-01': {'lat': , 'lon': , 'alt': },
    #'FRAS-01': {'lat': , 'lon': , 'alt': },
    'FRAS-02': {'lat': 41.812600000000, 'lon': 12.677933333333, 'alt': 416.0},
    'GROS-01': {'lat': 42.753583333333, 'lon': 11.117600000000, 'alt':  20.0},
    #'GROT-01': {'lat': , 'lon': , 'alt': },
    #'LAQU-01': {'lat': , 'lon': , 'alt': },
    'LAQU-02': {'lat': 42.354933333333, 'lon': 13.413416666667, 'alt': 795.0},
    'LECC-01': {'lat': 40.360900000000, 'lon': 18.192400000000, 'alt': 115.0},
    #'LECC-02': {'lat': , 'lon': , 'alt': },
    #'LECC-03': {'lat': , 'lon': , 'alt': },
    #'LODI-01': {'lat': , 'lon': , 'alt': },
    #'PISA-01': {'lat': , 'lon': , 'alt': },
    #'PARM-01': {'lat': , 'lon': , 'alt': },
    #'PATE-01': {'lat': , 'lon': , 'alt': },
    #'REGG-01': {'lat': , 'lon': , 'alt': },
    #'ROMA-01': {'lat': , 'lon': , 'alt': },
    #'ROMA-02': {'lat': , 'lon': , 'alt': },
    #'SALE-01': {'lat': , 'lon': , 'alt': },
    'SAVO-01': {'lat': 44.306100000000, 'lon':  8.482883333333, 'alt': 32.0},
    'SAVO-02': {'lat': 44.316150000000, 'lon':  8.478166666667, 'alt': 33.0},
    #'SAVO-03': {'lat': , 'lon': , 'alt': },
    #'TERA-01': {'lat': , 'lon': , 'alt': },
    #'TORI-01': {'lat': , 'lon': , 'alt': },
    #'TORI-02': {'lat': , 'lon': , 'alt': },
    #'TORI-03': {'lat': , 'lon': , 'alt': },
    'TORI-04': {'lat': 45.064566666667, 'lon':  7.676100000000, 'alt': 252.0},
    'TRAP-01': {'lat': 38.0179825,      'lon': 12.51271667    , 'alt':  23.0},
    #'TREV-01': {'lat': , 'lon': , 'alt': }, 
    'TRIN-01': {'lat': 41.352783333333, 'lon': 16.096216666667, 'alt':  25.0},
    'VIAR-01': {'lat': 43.871033333333, 'lon': 10.244166666667, 'alt':  11.0},
    'VIAR-02': {'lat': 43.858933333333, 'lon': 10.244783333333, 'alt':  16.0}
}


def location(station):
    """ Return the location of a given station, indexed either by name or
    unique (integer) ID.
    """
    if isinstance(station, int):
        station = E3_STATION_ID_DICT[station]
    lat = E3_LOCATION_DICT[station]['lat']
    lon = E3_LOCATION_DICT[station]['lon']
    alt = E3_LOCATION_DICT[station]['alt']
    return (lat, lon, alt)



E3_GEOMETRY_DICT = {
    'ALTA-01': {'phi_north':  55.0, 'd12':  60.0, 'd23':  60.0},
    #'ANCO-01': {'phi_north': , 'd12': , 'd23': },
    #'AREZ-01': {'phi_north': , 'd12': , 'd23': },
    'BARI-01': {'phi_north': 222.0, 'd12':  67.0, 'd23':  67.0},
    #'BOLO-01': {'phi_north': , 'd12': , 'd23': },
    #'BOLO-02': {'phi_north': , 'd12': , 'd23': },
    'BOLO-03': {'phi_north': 145.0, 'd12':  55.0, 'd23':  55.0},
    #'BOLO-04': {'phi_north': , 'd12': , 'd23': },
    'CAGL-01': {'phi_north': 236.0, 'd12':  70.0, 'd23':  70.0},
    'CAGL-02': {'phi_north': 100.0, 'd12':  70.0, 'd23':  70.0},
    'CAGL-03': {'phi_north': 115.0, 'd12':  50.0, 'd23':  50.0},
    #'CATA-01': {'phi_north': , 'd12': , 'd23': },
    'CATA-02': {'phi_north': 300.0, 'd12':  80.0, 'd23':  80.0},
    'CATZ-01': {'phi_north': 294.0, 'd12':  80.0, 'd23':  80.0},
    #'CERN-01': {'phi_north': , 'd12': , 'd23': },
    #'CERN-02': {'phi_north': , 'd12': , 'd23': },
    #'COSE-01': {'phi_north': , 'd12': , 'd23': },
    #'FRAS-01': {'phi_north': , 'd12': , 'd23': },
    'FRAS-02': {'phi_north': 178.0, 'd12':  40.0, 'd23':  40.0},
    'GROS-01': {'phi_north': 212.0, 'd12':  49.0, 'd23':  49.0},
    #'GROT-01': {'phi_north': , 'd12': , 'd23': },
    'LAQU-01': {'phi_north': 264.4, 'd12':  50.0, 'd23':  50.0},
    'LAQU-02': {'phi_north':  43.4, 'd12':  50.0, 'd23':  50.0},
    'LECC-01': {'phi_north':   5.2, 'd12': 100.0, 'd23': 100.0},
    #'LECC-02': {'phi_north': , 'd12': , 'd23': },
    #'LECC-03': {'phi_north': , 'd12': , 'd23': },
    #'LODI-01': {'phi_north': , 'd12': , 'd23': },
    'PISA-01': {'phi_north':   0.0, 'd12':  53.0, 'd23':  53.0},
    #'PARM-01': {'phi_north': , 'd12': , 'd23': },
    #'PATE-01': {'phi_north': , 'd12': , 'd23': },
    #'REGG-01': {'phi_north': , 'd12': , 'd23': },
    #'ROMA-01': {'phi_north': , 'd12': , 'd23': },
    #'ROMA-02': {'phi_north': , 'd12': , 'd23': },
    #'SALE-01': {'phi_north': , 'd12': , 'd23': },
    'SAVO-01': {'phi_north':  56.0, 'd12':  46.0, 'd23':  46.0},
    'SAVO-02': {'phi_north': 170.0, 'd12':  44.0, 'd23':  43.0},
    #'SAVO-03': {'phi_north': , 'd12': , 'd23': },
    #'TERA-01': {'phi_north': , 'd12': , 'd23': },
    #'TORI-01': {'phi_north': , 'd12': , 'd23': },
    #'TORI-02': {'phi_north': , 'd12': , 'd23': },
    #'TORI-03': {'phi_north': , 'd12': , 'd23': },
    'TORI-04': {'phi_north': 297.0, 'd12':  50.0, 'd23':  50.0},
    'TRAP-01': {'phi_north': 137.0, 'd12':  55.0, 'd23':  55.0},
    #'TREV-01': {'phi_north': , 'd12': , 'd23': }, 
    'TRIN-01': {'phi_north':  20.0, 'd12':  58.0, 'd23':  59.0},
    'VIAR-01': {'phi_north': 105.0, 'd12':  55.0, 'd23':  55.0},
    'VIAR-02': {'phi_north': 205.0, 'd12':  60.0, 'd23':  59.0}
}




if __name__ == '__main__':
    print E3_STATION_DICT
    print E3_ACTIVE_STATIONS
    print len(E3_STATION_DICT)
    print len(E3_ACTIVE_STATIONS)
