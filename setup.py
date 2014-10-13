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


from distutils.core import setup
import glob

from __version__ import TAG


_NAME = 'e3pipe'

_DESCRIPTION = 'Offline analysis pipeline for the EEE experiment'

_AUTHOR = 'Luca Baldini'

_AUTHOR_EMAIL = 'luca.baldini@pi.infn.it'

_LICENSE = 'GNU General Public License v3 or later'

_URL = 'https://bitbucket.org/lbaldini/e3pipe'

_PACKAGES = [
    'e3pipe', 'e3pipe.apps', 'e3pipe.doc', 'e3pipe.dqm', 'e3pipe.dst',
    'e3pipe.misc', 'e3pipe.root', 'e3pipe.tasks', 'e3pipe.test'
    ]

_PACKAGE_DIR = {
    'e3pipe': '.'
    }

_PACKAGE_DATA = {
    'e3pipe'      : ['LICENSE', 'README'],
    'e3pipe.apps' : [],
    'e3pipe.doc'  : [],
    'e3pipe.dqm'  : [],
    'e3pipe.dst'  : [],
    'e3pipe.misc' : [],
    'e3pipe.root' : [],
    'e3pipe.tasks': [],
    'e3pipe.test' : []
    }

_SCRIPTS = glob.glob('apps/*.py')

_CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'Environment :: Console',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: '
    'GNU General Public License v3 or later (GPLv3+)',
    'Programming Language :: Python',
    'Topic :: Scientific/Engineering :: Physics'
    ]


if __name__ == '__main__':

    setup(name = _NAME,
          description = _DESCRIPTION,
          version = TAG,
          author = _AUTHOR,
          author_email = _AUTHOR_EMAIL,
          license = _LICENSE,
          url = _URL,
          packages = _PACKAGES,
          package_dir = _PACKAGE_DIR,
          package_data = _PACKAGE_DATA,
          scripts = _SCRIPTS,
          classifiers = _CLASSIFIERS)
