# Continuous.py
#
# Copyright (c) 2009 James R. Holliday, jrholliday@ucdavis.edu
# See 'license.txt' for licensing and usage restrictions.
#
###############################################################################

"""Continuous forecast type.

This module exports only one object: the Continuous forecast class
definition.  This class inherits from the Forecasts base class.
"""

###############################################################################

from __future__ import division

from Forecast import Forecast

import numpy

###############################################################################

class Continuous(Forecast):
    """Class definition for Continuous forecast object.

    A continuous forecast gives a list of values for some measurable
    process and allows for comparison against the actual observations.
    """

    #-------------------------------------------------------------------------#

    def __init__(self):
        """Initialize Continuous object."""

        # Storage for data vectors ( forecast , observed )
        self._data = []

        # Storage for calculated statistics
        self._stats = {}
  
    #-------------------------------------------------------------------------#

    def add_data(self, forecast, observed):
        """Add forecast/observed data pair.

        Keyword arguments:
        forecast -- forecasted value.
        observed -- actual observed value.

        Return value:
        None
        """

        # Add data to the table list
        self._data.append( (forecast , observed) )

        # Reset the statistics object
        self._stats = {}

        # End add_data(self, ...)
        return None

    #-------------------------------------------------------------------------#

    def _calc_stats(self):
        """Calculate statistics on forecasted and observed data sets.

        This is an internal function and should not be called directly.
        """
        N = len(self._data)

        # Separate the Forecast from the observations
        F,O = [ numpy.array(col) for col in map(None, *self._data) ]

        # Calculate array totals
        sumF = F.sum()
        sumO = O.sum()

        # Calculate array means
        meanF = F.mean()
        meanO = O.mean()

        # Calculate the "Mean Error"
        ME = (F-O).sum() / N
        self._stats['ME'] = ME

        # Calculate the (multiplicative) "Bias"
        BIAS = sumF / sumO
        self._stats['BIAS'] = BIAS

        # Calculate the "Mean Absolute Error"
        MAE = abs(F-O).sum() / N
        self._stats['MAE'] = MAE

        # Calculate the "Mean Square Error"
        MSE = ((F-O)**2).sum() / N
        self._stats['MSE'] = MSE

        # Calculate the "Root Mean Square Error"
        self._stats['RMSE'] = numpy.sqrt(MSE)

        # Calculate the "Linear Error in Probability Space" (LEPS)
        pass

        # Calculate the "Correlation Coefficient" (R)
        R = ((F-meanF)*(O-meanO)).sum() / (N * F.std() * O.std())
        self._stats['R'] = R

        # Calculate the "Anomaly Correlation"
        pass

        # Calculate the "S1" score
        pass

        # Calculate the "Skill" score
        pass

        # End _calc_stats(self)
        return None

    #-------------------------------------------------------------------------#

    def scatter(self, type=0):
        """Calculate relationships between observed and forecasted values.

        Keyword arguments:
        type -- flag indicating which relationship to calculate. (Default 0)

        If type is set to 0, return the Forecast vs Observed values.
        If type is set to 1, return (Forecast-Observed) vs Observed values.
        If type is set to 2, return (Forecast-Observed) vs Forecast values.

        Returned values:
        tuple of x values,
        tuple of y values.
        """

        # Separate the Forecast from the observations
        F,O = [ numpy.array(col) for col in map(None, *self._data) ]

        try:
            X,Y = { # Type = 0 : X=Observed, Y=Forecast
                    0 : (O, F),

                    # Type = 1 : X=Observed, Y=Forecast-Observed
                    1 : (O, F-O),

                    # Type = 1 : X=Forecast, Y=Forecast-Observed
                    2 : (F, F-O)
                  }[type]

        # No other choices
        except KeyError:
            raise Exception("Scatter type must be 0, 1, or 2 [%s]." % type)

        # End scatter(self, ...)
        return tuple(X), tuple(Y)

###############################################################################
