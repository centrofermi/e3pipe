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


""" Basic event selection cuts.
"""
MAX_GOOD_CHISQUARE = 10.
CUT_GOOD_EVENT = 'StatusCode == 0'
CUT_GOOD_TRACK = '%s && ChiSquare < %.3f' % (CUT_GOOD_EVENT, MAX_GOOD_CHISQUARE)

""" Maximum run duration (in s), in the sense of the difference between the
largest and the smallest timestamp in the run.

Mind that this is really to give up on runs when the timestamps are so scrambled
that the apparent run duration is insanely long, see e.g.
http://eee.centrofermi.it/dqm/CATA-02/2014-10-22/CATA-02-2014-10-22-00022/

One day should be plenty :-)
"""
MAX_RUN_DURATION = 86400.0



if __name__ == '__main__':
    print 'MAX_GOOD_CHISQUARE = %s' % MAX_GOOD_CHISQUARE
    print 'CUT_NO_GPS = %s' % CUT_NO_GPS
    print 'CUT_GOOD_TRACK = %s' % CUT_GOOD_TRACK
