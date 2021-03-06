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
parser.add_option('-s', '--station', type = str, default = 'SAVO-01',
                  dest = 'station',
                  help = 'the actual telescope to simulate')
parser.add_option('-p', '--theta-power', type = float, default = 2.0,
                  dest = 'thetaPower',
                  help = 'the power for the cos(theta) term in the muon flux')
parser.add_option('-R', '--run-number', type = int, default = 1,
                  dest = 'runNumber',
                  help = 'the run number (and random seed) for the simulation')
parser.add_option('-f', '--fitting-tool', type = str, default = '2dw',
                  dest = 'fitTool',
                  help = 'the track-fitting tool to be used')
parser.add_option('-i', '--interactive', action = 'store_true',
                  default = False, dest = 'interactive',
                  help = 'run interactively (show the plots)')
parser.add_option('-l', '--label', type = str, default = None,
                  dest = 'label',
                  help = 'a label to be attached to the default file name')
(opts, args) = parser.parse_args()


from e3pipe.mc.E3TelescopeBase import E3TelescopeBase
from e3pipe.mc.E3Telescope import E3Telescope
from e3pipe.mc.E3McEventTree import E3McEventTree
from e3pipe.root.E3OutputRootFile import E3OutputRootFile
from e3pipe.__logging__ import logger


# Initialize the random number generator.
logger.info('Setting the seed for the random generator to %d...' %\
            opts.runNumber)
import random
random.seed(opts.runNumber)

# Setup the telescope...
fitTools = E3TelescopeBase.FIT_TOOL_DICT.keys()
if not opts.fitTool in fitTools:
    parser.error('Unknown fitTool "%s", available choices are %s' %\
                 (opts.fitTool, fitTools))
telescope = E3Telescope(opts.station, fitTool = opts.fitTool)
logger.info('Simulating %s...' % telescope)
telescope.fluxService().setThetaDistParameter(0, opts.thetaPower)

# Setup the output file...
outputFilePath = opts.outputFile
if outputFilePath is None:
    outputFilePath = '%s_%d_%s_mc' %\
                     (telescope.name(), opts.runNumber, opts.fitTool)
    if opts.label is not None:
        outputFilePath += '_%s' % (opts.label)
    outputFilePath += '.root'
    logger.info('No output file specified, using %s...' % outputFilePath)
outputFile = E3OutputRootFile(outputFilePath, 'e3sim.py',
                              station = opts.station)
outputTree = E3McEventTree()

# Finally: get started.
logger.info('Entering the event loop...')
numGenerated = 0
numTriggered = 0
prevTime = 0
for i in xrange(opts.numEvents):
    event = telescope.shootMuon()
    numGenerated += 1
    if event is not None:
        elapsedTime = event['Seconds'] + 1e-9*event['Nanoseconds']
        event['RunNumber'] = opts.runNumber
        event['StatusCode'] = 0
        event['EventNumber'] = i
        event['DeltaTime'] = elapsedTime - prevTime
        numTriggered += 1
        prevTime = elapsedTime
        outputTree.fillRow(event)
if numTriggered:
    fracTriggered = float(numTriggered)/numGenerated
    triggerRate = float(numTriggered)/elapsedTime
    logger.info('%d event(s) generated, %d triggered (%.2f %%) in %.3f s.' %\
                (numGenerated, numTriggered, fracTriggered*100, elapsedTime))
    logger.info('Average trigger rate: %.3f Hz' % triggerRate)
else:
    logger.info('No events triggered the telescope.')

#Finalize.
outputTree.doMonitoring()
for plot in outputTree.plots():
    plot.Write()
outputTree.Write()
outputFile.Close()
