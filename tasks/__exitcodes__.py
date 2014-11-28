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



""" Small utility module to try and keep track of the many, many different
ways things can go wrong.
"""
E3PIPE_EXIT_CODE_ANALYZER_SEGFAULT = 139
E3PIPE_EXIT_CODE_ANALYZER_KILLED = 137
E3PIPE_EXIT_CODE_NO_HITS_EVENTS = 100
E3PIPE_EXIT_CODE_RUN_TOO_LONG = 101
E3PIPE_EXIT_CODE_UNKNOWN = 17


E3PIPE_EXIT_CODE_INTENT_DICT = {
    E3PIPE_EXIT_CODE_ANALYZER_SEGFAULT:
    'the EEE analyzer exited with a segmentation fault',
    E3PIPE_EXIT_CODE_ANALYZER_KILLED:
    'the EEE analyzer was killed',
    E3PIPE_EXIT_CODE_NO_HITS_EVENTS:
    'no events with hits in the file',
    E3PIPE_EXIT_CODE_RUN_TOO_LONG:
    'difference between the largest and smallest timestamp too large',
    E3PIPE_EXIT_CODE_UNKNOWN:
    'unknown error'
}


def exitCodeIntent(code):
    """ Return the intent for a given exit code.
    """
    try:
        return E3PIPE_EXIT_CODE_INTENT_DICT[code]
    except KeyError:
        return 'n/a'

def lockFileMessage(code, logFilePath = None):
    """ Return a message for the lock file.
    """
    msg = 'Exit code %d (%s).' %\
          (code, exitCodeIntent(code))
    if logFilePath is not None:
        msg += '\nLog file at %s' % logFilePath
    msg += '\n'
    return msg



if __name__ == '__main__':
    print E3PIPE_EXIT_CODE_ANALYZER_SEGFAULT,\
        exitCodeIntent(E3PIPE_EXIT_CODE_ANALYZER_SEGFAULT)
    print lockFileMessage(E3PIPE_EXIT_CODE_ANALYZER_SEGFAULT)
    print lockFileMessage(E3PIPE_EXIT_CODE_ANALYZER_SEGFAULT, 'run.log')
    print lockFileMessage(46)
