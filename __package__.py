#!/usr/bin/env python
# *********************************************************************
# * Copyright (C) 2014 Luca Baldini (luca.baldini@pi.infn.it)         *
# *                                                                   *
# * For the license terms see the file LICENSE, distributed           *
# * along with this software.                                         *
# *********************************************************************
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU GengReral Public License as published by
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


import os

""" Basic folder structure of the package.
"""
E3PIPE_BASE = os.path.abspath(os.path.dirname(__file__))
E3PIPE_ANALYSIS = os.path.join(E3PIPE_BASE, 'analysis')
E3PIPE_APPS = os.path.join(E3PIPE_BASE, 'apps')
E3PIPE_CONFIG = os.path.join(E3PIPE_BASE, 'config')
E3PIPE_DIST = os.path.join(E3PIPE_BASE, 'dist')
E3PIPE_DOC = os.path.join(E3PIPE_BASE, 'doc')
E3PIPE_DQM = os.path.join(E3PIPE_BASE, 'dqm')
E3PIPE_DST = os.path.join(E3PIPE_BASE, 'dst')
E3PIPE_MC = os.path.join(E3PIPE_BASE, 'mc')
E3PIPE_MISC = os.path.join(E3PIPE_BASE, 'misc')
E3PIPE_PILOT = os.path.join(E3PIPE_BASE, 'pilot')
E3PIPE_ROOT = os.path.join(E3PIPE_BASE, 'root')
E3PIPE_RUNDB = os.path.join(E3PIPE_BASE, 'rundb')
E3PIPE_TASKS = os.path.join(E3PIPE_BASE, 'tasks')
E3PIPE_TEST = os.path.join(E3PIPE_BASE, 'test')


""" Version information.
"""
E3PIPE_VERSION_FILE_PATH = os.path.join(E3PIPE_BASE, '__version__.py')
def versionInfo():
    """ Read the tag and build date straight from the appropriate file.
    
    Use this when you don't want to import the module (i.e., at release time,
    when the file is changed), so that you don't have to bother with
    reloading stuff.
    """
    for line in open(E3PIPE_VERSION_FILE_PATH).readlines():
        exec(line.strip('\n'))
    return TAG, BUILD_DATE


""" Release notes.
"""
E3PIPE_RELEASE_NOTES_PATH = os.path.join(E3PIPE_DOC, 'release.notes')



if __name__ == '__main__':
    print('E3PIPE_ROOT: %s' % E3PIPE_ROOT)

