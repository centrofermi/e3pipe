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


_usage = 'usage: %prog [options] filePath'
_synopsis = 'EEE fast simulator'

# Set up the command-line switches.
from e3pipe.misc.E3OptionParser import E3OptionParser

parser = E3OptionParser(_usage, _synopsis)
parser.add_option('-o', '--output-file', type = str, default = None,
                  dest = 'outputFile',
                  help = 'path to the output ROOT file')
parser.add_option('-n', '--numEvents', type = int, default = 100000,
                  dest = 'numEvents',
                  help = 'the number of events to generate')
parser.add_option('-s', '--station', type = str, default = None,
                  dest = 'station',
                  help = 'the actual telescope to simulate')
parser.add_option('-i', '--interactive', action = 'store_true',
                  default = False, dest = 'interactive',
                  help = 'run interactively (show the plots)')
(opts, args) = parser.parse_args()


from e3pipe.mc.E3BaseTelescope import E3BaseTelescope
from e3pipe.mc.E3Telescope import E3Telescope
from e3pipe.mc.E3McEventTree import E3McEventTree
from e3pipe.root.E3OutputRootFile import E3OutputRootFile
from e3pipe.__logging__ import logger


# Setup the telscope...
if opts.station is not None:
    telescope = E3Telescope(opts.station)
else:
    telescope = E3BaseTelescope()
logger.info('Simulating %s...' % telescope)

# Setup the output file...
outputFilePath = opts.outputFile
if outputFilePath is None:
    outputFilePath = '%s_mc.root' % telescope.name()
    logger.info('No output file specified, using %s...' % outputFilePath)
outputFile = E3OutputRootFile(outputFilePath, 'e3sim.py')
outputTree = E3McEventTree()

# Finally: get started.
logger.info('Entering the event loop...')
numGenerated = 0
numTriggered = 0
for i in xrange(opts.numEvents):
    event = telescope.shootMuon()
    event['EventNumber'] = i
    numGenerated += 1
    if event['Trigger']:
        numTriggered += 1
    outputTree.fillRow(event)
fracTriggered = float(numTriggered)/numGenerated
logger.info('Done. %d event(s) generated, %d triggered (%.2f %%).' %\
            (numGenerated, numTriggered, fracTriggered*100))
estimatedRate = 100*fracTriggered
logger.info('Estimated rate: %.1f Hz' % estimatedRate)

#Finalize.
outputTree.doMonitoring()
for plot in outputTree.plots():
    plot.Write()
outputTree.Write()
outputFile.Close()
