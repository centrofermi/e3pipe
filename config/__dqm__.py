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


DQM_BASELINE_PLOT_LIST = [
    ('Phi', dict()),
    ('Theta', dict()),
    ('TimeOfFlight', dict()),
    ('TrackLength', dict())
]


DQM_BASELINE_ALARM_LIST = [
    ('ChiSquare', 'x_average', 1, 2, 6, 10, dict(Logy = True)),
    ('DeltaTime', 'exp_fit_lambda', 5, 10, 50, 75, dict(Logy = True)),
    ('RateTrackEvents', 'y_values', 5, 10, 50, 75, dict()),
    ('HitMultTop', 'x_average', 0.5, 0.75, 2, 3, dict(Logy = True)),
    ('HitMultMid', 'x_average', 0.5, 0.75, 2, 3, dict(Logy = True)),
    ('HitMultBot', 'x_average', 0.5, 0.75, 2, 3, dict(Logy = True)),
    ('HitMultTotal', 'x_average', 1.5, 2.5, 6, 9, dict(Logy = True)),
    ('ClusterMultTop', 'x_average', 0.5, 0.75, 2, 3, dict(Logy = True)),
    ('ClusterMultMid', 'x_average', 0.5, 0.75, 2, 3, dict(Logy = True)),
    ('ClusterMultBot', 'x_average', 0.5, 0.75, 2, 3, dict(Logy = True)),
    ('ClusterMultTotal', 'x_average', 1.5, 2.5, 6, 9, dict(Logy = True)),
]



if __name__ == '__main__':
    print DQM_BASELINE_PLOT_LIST, DQM_BASELINE_ALARM_LIST
