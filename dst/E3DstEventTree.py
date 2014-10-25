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


from e3pipe.root.E3Tree import E3Tree
from e3pipe.root.E3BranchDescriptor import E3BranchDescriptor
from e3pipe.dst.E3DstTrendingTree import E3DstTrendingTree
from e3pipe.config.__dst__ import MAX_GOOD_CHISQUARE, CUT_HIT_EVENT,\
    CUT_GOOD_TRACK, TRENDING_LIST
from e3pipe.root.E3H1D import E3H1D
from e3pipe.root.__ROOT__ import setupTimeDisplay



class E3DstEventTree(E3Tree):
    
    """ Class describing the ROOT tree containing all the event-by-event
    information.
    """

    NAME = 'Events'
    BRANCHES = [E3BranchDescriptor('RunNumber', 'i'),
                E3BranchDescriptor('EventNumber', 'i'),
                E3BranchDescriptor('StatusCode', 'i'),
                E3BranchDescriptor('Seconds', 'i'),
                E3BranchDescriptor('Nanoseconds', 'l'),
                E3BranchDescriptor('XDir', 'F'),
                E3BranchDescriptor('YDir', 'F'),
                E3BranchDescriptor('ZDir', 'F'),
                E3BranchDescriptor('ChiSquare', 'F'),
                E3BranchDescriptor('TimeOfFlight', 'F'),
                E3BranchDescriptor('TrackLength', 'F'),
                E3BranchDescriptor('DeltaTime', 'D')
            ]
    ALIAS_DICT = {'Timestamp': 'Seconds + 1.e-9*Nanoseconds',
                  'Theta'    : '57.29577951308232*acos(ZDir)',
                  'Phi'      : '57.29577951308232*atan2(YDir, XDir)'}

    def __init__(self):
        """ Constructor.
        """
        E3Tree.__init__(self, 'Event tree')

    def timestamp(self, entry = None):
        """ Retrurn the timestamp for a given entry.
        """
        if entry is not None:
            self.GetEntry(entry)
        return self.value('Seconds') + 1.e-9*self.value('Nanoseconds')

    def runStart(self):
        """ Return the timestamp of the first event.

        Mind that we have to make sure that the first event is not a GPS event,
        otherwise we're screwed.

        TODO: and this might change again if we eventually get the timestamp
        information for the GPS events. 
        """
        entry = 0
        while 1:
            t = self.timestamp(entry)
            if t > 0:
                return t
            entry += 1

    def runStop(self):
        """ Return the timestamp of the last event.

        Mind that we have to make sure that the first event is not a GPS event,
        otherwise we're screwed.

        TODO: and this might change again if we eventually get the timestamp
        information for the GPS events. 
        """
        entry = self.GetEntries() - 1
        while 1:
            t = self.timestamp(entry)
            if t > 0:
                return t
            entry -= 1

    def runDuration(self):
        """ Return the run duration.
        """
        return self.runStop() - self.runStart()

    def trendingHist(self, name, title = None, cut = '', timeDelta = 60,
                     xmin = None, xmax = None, **kwargs):
        """ Create a trending histogram.
        """
        xmin = xmin or self.runStart()
        xmin -= 1.e-3
        xmax = xmax or self.runStop()
        xmax += 1.e-3
        xbins = max(1, int(self.runDuration()/float(timeDelta) + 0.5))
        hist = self.hist1d('Timestamp', cut, name, title, xmin, xmax, xbins,
                           **kwargs)
        hist.Sumw2()
        hist.Scale(1./hist.GetBinWidth(1))
        hist.SetXTitle('')
        return hist

    def doMonitoring(self):
        """ Create the standard set of monitoring plots.

        TODO: this should properly configured via a configuration file.
        """
        self.hist1d('Theta', cut = CUT_GOOD_TRACK,
                    xmin = 0., xmax = 70., xbins = 50,
                    XTitle = '#theta [#circ]')
        self.hist1d('Phi', cut = CUT_GOOD_TRACK,
                    xmin = -180., xmax = 180., xbins = 50,
                    XTitle = '#phi [#circ]', Minimum = 0.)
        # Mind we do skip the first event, here, for which the delta
        # event time is not defined.
        self.hist1d('DeltaTime', cut = 'EventNumber > 0 && %s' % CUT_HIT_EVENT,
                    xmin = 0, xmax = 0.5, xbins = 100,
                    XTitle = 'Time difference [s]')
        self.hist1d('ChiSquare', cut = CUT_HIT_EVENT,
                    xmin = 0, xmax = 50, xbins = 100,
                    XTitle = '#chi^{2}')
        self.hist1d('TimeOfFlight', cut = CUT_GOOD_TRACK,
                    xmin = -10, xmax = 20, xbins = 100,
                    XTitle = 'Time of flight [ns]')
        self.hist1d('TrackLength', cut = CUT_GOOD_TRACK,
                    xmin = 0, xmax = 300., xbins = 100,
                    XTitle = 'Track length [cm]')

    def doTrending(self, timeDelta = 60, xmin = None, xmax = None,
                   weatherRecord = None):
        """ Create the trending plots/tree.

        TODO: this is only partially configured from config.__dst__.py

        Note that you do have to call the TH1::SetTimeDisplay() method
        after the call to TH1::Divide(), otherwise the number of bins
        in the histograms is doubles. ROOT is weird.
        """
        for (name, title, cut, kwargs) in TRENDING_LIST:
            self.trendingHist(name, title, cut, timeDelta, xmin, xmax,
                              YTitle = '%s [Hz]' % title)
        hHit = self.plot('RateHitEvents')
        hTkr = self.plot('RateTrackEvents')
        hFra = hHit.Clone('FractionTrackEvents')
        hFra.SetYTitle('Fraction of events with #chi^{2} < %.1f' %\
                       MAX_GOOD_CHISQUARE)
        hFra.Divide(hTkr, hHit, 1., 1., 'B')
        self.store(hFra)
        for h in [hHit, hTkr, hFra]:
            setupTimeDisplay(h)
        tree = E3DstTrendingTree()
        tree.setUniqueRunId(self.UniqueRunId)
        if weatherRecord is not None:
            tree.setValue('IndoorTemperature',
                          weatherRecord.indoorTemperature())
            tree.setValue('OutdoorTemperature', 
                          weatherRecord.outdoorTemperature())
            tree.setValue('Pressure', weatherRecord.pressure())
        for i in range(1, hHit.GetNbinsX() + 1):
            tree.setValue('BinStart', hHit.GetBinLowEdge(i))
            tree.setValue('BinEnd', hHit.GetBinLowEdge(i) + hHit.GetBinWidth(i))
            tree.setValue('RateHitEvents', hHit.GetBinContent(i))
            tree.setValue('RateHitEventsErr', hHit.GetBinError(i))
            tree.setValue('RateTrackEvents', hTkr.GetBinContent(i))
            tree.setValue('RateTrackEventsErr', hTkr.GetBinError(i))
            tree.setValue('FractionTrackEvents', hFra.GetBinContent(i))
            tree.setValue('FractionTrackEventsErr', hFra.GetBinError(i))
            tree.Fill()
        return tree


def test():
    """
    """
    tree = E3DstEventTree()



if __name__ == '__main__':
    test()
