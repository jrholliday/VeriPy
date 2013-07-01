# Forecast.py
#
# Copyright (c) James R. Holliday, jrholliday@gmail.com
# See 'license.txt' for licensing and usage restrictions.
#
###############################################################################

"""Base class for Continuous and Probabilistic forecast types.

This module exports only one object: the Forecast base class.  The
Continuous class and the Probabilisitic class both inherit from
Forecast.  The Forecast type should not be used by itself.
"""

###############################################################################

from __future__ import division

import numpy

###############################################################################

class Forecast(object):
    """Base class for Continuous and Probabilistic forecast types.

    The Continuous class and the Probabilisitic class both inherit
    from this base class.  This class should not be called or used by
    itself.
    """

    #-------------------------------------------------------------------------#

    def __init__(self):
        """Initialize Forecast object."""

        # Storage for data array
        self._data = []

        # Storage for calculated statistics
        self._stats = {}

         # Storage for histogram thresholds
        self._hist = {}

    #-------------------------------------------------------------------------#

    def __str__(self):
        """Return string representation of data array."""

        # End __str__(self)
        return str(self._data)

    #-------------------------------------------------------------------------#

    def add_data(self, datum):
        """Add data to forecast object."""

        # End add_data(self, ...)
        return None

    #-------------------------------------------------------------------------#

    def _calc_stats(self):
        """Calculate statistics on forecasted and observed data sets.

        This is an internal function and should not be called directly.
        """

        # End _calc_stats(self)
        return None

    #-------------------------------------------------------------------------#

    def stats(self, Test=None):
        """Return a copy of the calculated forecast statistics.

        Keyword arguments:
        Test -- the specific test result to return. (default None)

        If Test does not exist, or is None, return a dictionary of all
        test results.

        Return value:
        either calculated value of Test or dictionary of test results
        indexed by test.
        """

        # Check that _calc_stats(self) has been run first
        if self._stats == {}:
            self._calc_stats()

        # Check if Test is one of our calculated statistics.
        if Test in self._stats.keys():
            results = self._stats[Test]
        else:
            results = self._stats

        # End stats(self, ...)
        return results

    #-------------------------------------------------------------------------#

    def print_stats(self, Test=None):
        """Print the calculated statistics to screen.

        Keyword arguments:
        Test -- the specific test result to return. (default None)

        Print out a formatted report of test results.  If Test does
        not exist, or is None, report on all test results.

        Return value:
        None
        """

        # Check that _calc_stats(self) has been run first
        if self._stats == {}:
            self._calc_stats()

        # Get list of all tests.
        tests = self._stats.keys()

        # Check if Test is one of our calculated statistics.
        if Test in tests:
                print "%s\t% .6f" % ( Test , self._stats[Test] )
        else:
            for test in tests:
                print "%s\t%s" % ( test , self._stats[test] )

        # End print_stats(self, ...)
        return None

    #-------------------------------------------------------------------------#

    def histogram(self, bins, unit=None):
        """Return the summed observations in forecasted categories.

        Keyword arguments:
        bins -- number or description of bins to populate.
        unit -- construct bins uniformly over the total range? (default None)

        The bins keyword can either be an integer, N, of bins to
        populate or a list of upper edges.  If a set number is passed
        in, the unit keyword dictates whether the N bins are
        constructed with uniform width over the forecast range
        (unit=True), with uniform "width" over the forecast
        distribution (unit=False), or "balanced" such that each bin
        gets roughly the same number of "events" (unit=None, default).

        Return value:
        dictionary of observations and sample sizes indexed by upper
        bin threshold.
        """

        hist = {}

        # Separate the Forecast from the observations
        F,O = [ numpy.array(col) for col in map(None, *self._data) ]

        # If number of bins is given, create the bins array
        if type(bins) is int:
            N = bins
            bins = []


            if unit is None:
                thresh = []
                for f,o in self._data:
                    if o >= 1:
                        if f not in thresh:
                            thresh.append(f)
                    
                thresh.sort()
                Nobs = len(thresh)

                groups = [int(Nobs/N)+1 if i<Nobs%N
                          else int(Nobs/N)
                          for i in range(N)]

                bins.append( F.min() )
                indx = 0
                for i in xrange(N-1):
                    indx += groups[i]
                    try:
                        bins.append(.5*(thresh[indx]+thresh[indx+1]))
                    except:
                        pass
                bins.append( F.max() )

            elif unit is True:
                L = F.min()
                U = F.max()

                dx = ( U - L ) / N

                for i in xrange(0 , N+1):
                    bins.append(L + i*dx)

            else:
                tmp = sorted(F)
                NN = len(tmp)-1

                for i in xrange(0 , N+1):
                    bins.append(tmp[int(NN*i/N)])

        # Inititialize the histogram object
        hist['under'] = [0,0]
        hist['over']  = [0,0]

        for i in xrange(1,len(bins)):
            hist[.5*(bins[i-1]+bins[i])] = [0,0]

        # Loop over forecasts and cumulate the observations
        for f,o in self._data:

            # Check for underflow
            if f < bins[0]:
                hist['under'][0] += o
                hist['under'][1] += 1

            # Check for overflow
            elif f > bins[-1]:
                hist['over'][0] += o
                hist['over'][1] += 1

            # Increment the proper bin
            else:
                for i in xrange(1,len(bins)):
                    if f <= bins[i]:
                        hist[.5*(bins[i-1]+bins[i])][0] += o
                        hist[.5*(bins[i-1]+bins[i])][1] += 1
                        break

        # End histogram(self, ...)
        return hist
    
###############################################################################
