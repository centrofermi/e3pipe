#!/usr/bin/env python
# *********************************************************************
# * Copyright (C) 2014 Luca Baldini (luca.baldini@pi.infn.it)         *
# *                                                                   *
# * For the license terms see the file LICENCE, distributed           *
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


import e3pipe.__utils__ as __utils__

from e3pipe.__logging__ import logger
from e3pipe.__package__ import E3PIPE_VERSION_FILE_PATH, versionInfo,\
    E3PIPE_RELEASE_NOTES_PATH


TAG_MODES = ['major', 'minor', 'patch']



def updateVersionInfo(mode, dryRun = False):
    """ Update the __tag__.py module with the new tag and build date.
    """
    prevTag, prevBuildDate = versionInfo()
    logger.info('Previous tag was %s...' % prevTag)
    version, release, patch = [int(item) for item in prevTag.split('.')]
    if mode == 'major':
        version += 1
        release = 0
        patch = 0
    elif mode == 'minor':
        release += 1
        patch = 0
    elif mode == 'patch':
        patch += 1
    else:
        abort('Unknown release mode %s.' % mode)
    nextTag = '%s.%s.%s' % (version, release, patch)
    logger.info('Writing new tag (%s) to %s...' %\
                (nextTag, E3PIPE_VERSION_FILE_PATH))
    if not dryRun:
        outputFile = open(E3PIPE_VERSION_FILE_PATH, 'w')
        outputFile.writelines('TAG = \'%s\'\n' % nextTag)
        outputFile.writelines('BUILD_DATE = \'%s\'\n' % BUILD_DATE)
        outputFile.close()
    logger.info('Done.')
    return nextTag

def updateReleaseNotes(tag, dryRun = False):
    """ Write the new tag and build date on top of the release notes
    (which must be kept up to date during the release process).
    """
    hline = '-'*79
    logger.info('Reading in %s...' % E3PIPE_RELEASE_NOTES_PATH)
    notes = open(E3PIPE_RELEASE_NOTES_PATH).read().strip('\n')
    logger.info('Writing out %s...' % E3PIPE_RELEASE_NOTES_PATH)
    if not dryRun:
        outputFile = open(E3PIPE_RELEASE_NOTES_PATH, 'w')
        outputFile.writelines('\n%s\ne3pipe (%s) - %s\n%s\n' %\
                                  (hline, tag, BUILD_DATE, hline))
        outputFile.writelines(notes)
        outputFile.close()
    logger.info('Done.')

def tagPackage(mode, dryRun = False):
    """ Tag the package.

    This means:
    (*) hg pull/update to make sure we're not missing remote modification;
    (*) figure out the target tag and update the release.notes;
    (*) commit the modifications, tag and push.
    """
    __utils__.cmd('hg pull', verbose = True, dryRun = dryRun)
    __utils__.cmd('hg update', verbose = True, dryRun = dryRun)
    __utils__.cmd('hg status', verbose = True, dryRun = dryRun)
    tag = updateVersionInfo(mode, dryRun)
    updateReleaseNotes(tag, dryRun)
    msg = 'Prepare for tag %s.' % tag
    __utils__.cmd('hg commit -m "%s"' % msg, verbose = True, dryRun = dryRun)
    __utils__.cmd('hg push', verbose = True, dryRun = dryRun)
    __utils__.cmd('hg tag %s' % tag, verbose = True, dryRun = dryRun)
    __utils__.cmd('hg push', verbose = True, dryRun = dryRun)
    __utils__.cmd('hg status', verbose = True, dryRun = dryRun)



if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option('-t', dest = 'tagmode', type = str, default = None,
                      help = 'The release tag mode %s.' % TAG_MODES)
    parser.add_option('-n', action = 'store_true', dest = 'dryrun',
                      help = 'Dry run (i.e. do not actually do anything).')
    parser.add_option('-s', action = 'store_true', dest = 'src',
                      help = 'Create a source distribution.')
    (opts, args) = parser.parse_args()
    if not opts.tagmode and not (opts.src or opts.rpm):
        parser.print_help()
        parser.error('Please specify at least one valid option.')        
    tag = None
    if opts.tagmode is not None:
        if opts.tagmode not in TAG_MODES:
            parser.error('Invalid tag mode %s (allowed: %s)' %\
                             (opts.tagmode, TAG_MODES))
        tagPackage(opts.tagmode, opts.dryrun)
    if opts.src and not opts.dryrun:
        distsrc()



