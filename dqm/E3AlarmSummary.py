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


from e3pipe.__logging__ import logger, abort
from e3pipe.dqm.E3Alarm import E3Alarm


class E3AlarmSummary(dict):

    """ Small utility class summarizing the alarm statistics for the DQM.
    """
    
    def __init__(self):
        """ Constructor.
        """
        dict.__init__(self)
        self[E3Alarm.STATUS_UNSET] = 0
        self[E3Alarm.STATUS_CLEAN] = 0
        self[E3Alarm.STATUS_WARNING] = 0
        self[E3Alarm.STATUS_ERROR] = 0
    
    def fill(self, alarm):
        """
        """
        self[alarm.status()] += 1

    def status(self):
        """
        """
        for status in [E3Alarm.STATUS_ERROR, E3Alarm.STATUS_WARNING,
                       E3Alarm.STATUS_CLEAN, E3Alarm.STATUS_UNSET]:
            if self[status]:
                return status

    def write(self, filePath):
        """
        """
        logger.info('Writing alarm summary to %s...' % filePath)
        outputFile = open(filePath, 'w')
        outputFile.write('Status: %s\n' % self.status())
        for status in [E3Alarm.STATUS_ERROR, E3Alarm.STATUS_WARNING,
                       E3Alarm.STATUS_CLEAN, E3Alarm.STATUS_UNSET]:
            outputFile.write('%s alarms: %s\n' % (status, self[status]))
        outputFile.close()
        logger.info('Done.')


    
def test():
    """ Test program.
    """
    summary = E3AlarmSummary()
    print summary
    



if __name__ == '__main__':
    test()
