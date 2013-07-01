# Probabilistic.py
#
# Copyright (c) James R. Holliday, jrholliday@gmail.com
# See 'license.txt' for licensing and usage restrictions.
#
###############################################################################

"""Probabilistic forecast type.

This module exports only one object: the Probabilistic forecast class
definition.  This class inherits from the Forecasts base class.
"""

###############################################################################

from __future__ import division

from Forecast import Forecast
from tools.GenericCDF import GenericCDF
from tools.ConfidenceIntervals import CI

import numpy
import scipy.special

###############################################################################

class Probabilistic(Forecast):
    """Class definition for Probabilistic forecast object.

    A probabilistic forecast gives a probability of an event
    occurring, with a value between 0 and 1 (or 0 and 100%).  Event
    occurrence is binary: it either occurs or it does not occur.
    """

    #-------------------------------------------------------------------------#

    def __init__(self):
        """Initialize Probabilistic object."""

        # Storage for data vectors ( forecast , observed )
        self._data = []

        # Storage for bootstrap "observations"
        self._boot = None

        # Storage for calculated statistics
        self._stats = {}

    #-------------------------------------------------------------------------#

    def add_data(self, forecast, observed):
        """Add forecast/observed data pair.

        Keyword arguments:
        forecast -- probability of event occurring.
        observed -- number of observed events.

        Since forecast indicates the probability of the event
        occuring, it must be a value between 0 and 1, inclusive.
        Since obsevered is the number of observed event occurrences,
        it must be a positive integer (including 0).

        Return value:
        None
        """

        # Check forecast is between 0 and 1
        if not 0 <= forecast <= 1:
            raise ValueError("Forecast must be between 0 and 1 (%s)."
                             % forecast)

        # Check observation is binary (either 0 or 1)
        if observed < 0 or observed != int(observed):
            raise ValueError("Observation must be a positive integer (%s)."
                             % observed)
            
        # Add data to the table list
        self._data.append( (forecast , int(observed)) )

        # Reset the bootstrap object
        self._boot = None

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

        # Calculate the climatology value
        C = O.mean()

        # Calculate the "Brier Score"
        BS =  ((F-O)**2).sum() / N
        self._stats['BS'] = BS

        # Calculate the "Brier Skill Score"
        BSC = ((F-C)**2).sum() / N
        BSS = 1 - BS/BSC
        self._stats['BSS'] = BSS

        # Calculate the "Ranked Probability Score"
        pass

        # Calculate the "Ranked Probability Score"
        pass

        # End _calc_stats(self)
        return None

    #-------------------------------------------------------------------------#

    def reliability(self, bins=10, unit=None):
        """Calculate and return reliability data and climatology background.

        Keyword arguments:
        bins -- number or description of bins to populate. (default 10)
        unit -- construct bins uniformly over the total range? (default True)

        The bins keyword can either be an integer, N, of bins to
        populate or a list of upper edges.  If a set number is passed
        in, the unit keyword dictates whether the N bins are
        constructed with uniform width over the forecast range
        (unit=True), with uniform "width" over the forecast
        distribution (unit=False), or "balanced" such that each bin
        gets roughly the same number of "events" (unit=None, default).

        Returned values:
        tuple of x values,
        tuple of y values,
        tuple of sample sizes in each bin,
        climatology measure.
        """

        # Histogram the data
        hist = self.histogram(bins,unit)
        x,y,z = [],[],[]

        # Calculate the observed relative frequency for each probability bin
        for key in sorted(hist.keys()):
            if type(key) is not str:
                try: res = hist[key][0]/hist[key][1]
                except ZeroDivisionError: res = 0

                x.append(key)
                y.append(res)
                z.append(hist[key][1])

        # Determine the climatology background
        climatology = sum(map(None,*self._data)[1]) / len(self._data)

        # End reliability(self, ...)
        return tuple(x), tuple(y), tuple(z), climatology

    #-------------------------------------------------------------------------#

    def roc(self, threshold=None, unit=True, sigma=1.96):
        """Calculate and return relative operating characteristic (ROC) data.

        Keyword arguments:
        threshold -- probability values for calculating hit rates and false
                     alarm rates. (default None)
        unit  -- construct bins uniformly over the total range? (default True)
        sigma -- sigma level for confidence bands. (default 1.96)

        The threshold keyword can either be an integer, N, of
        probability thresholds to use or a list of specific
        probabilities.  If a set number is passed in, the unit keyword
        dictates whether the N probabilities are sampled uniformly
        over the forecast range (unit=True) or uniformly over the
        forecast distribution (unit=False).  Confidence bands are
        estimated using the binomial distribution if the bootstrap
        function has not been previously called.

        Return values:
        tuple of x values,
        tuple of y values,
        tuple of (lower,upper) x-axis confidence bands,
        tuple of (lower,upper) y-axis confidence bands.
        """
        return self._calc_curve('ROC', threshold, unit, sigma)

    #-------------------------------------------------------------------------#

    def error(self, threshold=None, unit=True, sigma=1.96):
        """Calculate and return error diagram data.

        Keyword arguments:
        threshold -- probability values for calculating miss rates and
                     fraction of alarm space. (default None)
        unit  -- construct bins uniformly over the total range? (default True)
        sigma -- sigma level for confidence bands. (default 1.96)

        The threshold keyword can either be an integer, N, of
        probability thresholds to use or a list of specific
        probabilities.  If a set number is passed in, the unit keyword
        dictates whether the N probabilities are sampled uniformly
        over the forecast range (unit=True) or uniformly over the
        forecast distribution (unit=False).  Confidence bands are
        estimated using the binomial distribution if the bootstrap
        function has not been previously called.

        Return values:
        tuple of x values,
        tuple of y values,
        tuple of (lower,upper) x-axis confidence bands,
        tuple of (lower,upper) y-axis confidence bands.
        """
        return self._calc_curve('ERROR', threshold, unit, sigma)

    #-------------------------------------------------------------------------#

    def _calc_curve(self, curve, threshold, unit, sigma):
        """Calculate and return assorted (ROC, error, etc) diagram data.

        This is an internal function and should not be called directly.
        Instead, call the appropriate wrapper function.

        Keyword arguments:
        curve     -- flag indicating which diagram measures to calculate.
                     Supported values are 'ROC' and 'ERROR'.
        threshold -- probability values for calculating x-axis and y-axis
                     measures. (default None)
        unit  -- construct bins uniformly over the total range? (default True)
        sigma -- sigma level for confidence bands. (default 1.96)

        The threshold keyword can either be an integer, N, of
        probability thresholds to use or a list of specific
        probabilities.  If a set number is passed in, the unit keyword
        dictates whether the N probabilities are sampled uniformly
        over the forecast range (unit=True) or uniformly over the
        forecast distribution (unit=False).  Confidence bands are
        estimated using the binomial distribution if the bootstrap
        function has not been previously called.

        Return values:
        tuple of x values,
        tuple of y values,
        tuple of (lower,upper) x-axis confidence bands,
        tuple of (lower,upper) y-axis confidence bands.
        """
        if self._boot is None:  self.bootstrap(0)

        # Copy the forecasted and oberved (plus bootstrapped) data
        forecast,obs = [ numpy.array(col) for col in map(None, *self._data) ]
        observed = numpy.vstack((obs,self._boot))

        Nobs = obs.sum()

        thresh = []
        for obs in observed:
            # if threshold is None, find the exact "jump" points.  These will
            # be the places where the observed value is > 0.
            if threshold is None:
                thresh.append([])

                for f,o in zip(forecast,obs):
                    if o >= 1:
                        thresh[-1].append(f)
                    
                thresh[-1].sort()

            # If number of thresholds is given, create the thresholds array
            elif type(threshold) is int:
                tmp = sorted( forecast )

                if unit is True:
                    L = tmp[0]
                    U = tmp[-1]

                    dx = ( U - L ) / (threshold+1)

                    thresh.append( [L + i*dx
                                    for i in xrange(threshold+1)] )

                else:
                    NN = len(tmp)-1

                    thresh.append( [tmp[int(NN*i/threshold)]
                                    for i in xrange(threshold+1)] )

            else:
                # Make sure '0' and '1' are in threshold array
                tmp = [float(i) for i in threshold]
                if 0.0 not in tmp: tmp.append(0.0)
                if 1.0 not in tmp: tmp.append(1.0)
                thresh.append(sorted(tmp))

        if curve == 'ERROR':
            x = [1.0,]
            y = [0.0,]
        else:
            x = [1.0,]
            y = [1.0,]

        pairs = []

        for j in xrange(len(observed)):
            for val in thresh[j]:
                a = 0
                b = 0
                c = 0
                d = 0

                for i in xrange(len(forecast)):
                    if forecast[i] >= val and observed[j][i] >= 1: a += 1
                    if forecast[i] >= val and observed[j][i] == 0: b += 1
                    if forecast[i] <  val and observed[j][i] >= 1: c += 1
                    if forecast[i] <  val and observed[j][i] == 0: d += 1

                # Calculate statistics
                try:
                    if curve == 'ERROR':
                        X = (a + b) / (a + b + c + d) # Tau (alarm space)
                        Y = c / (a + c)               # Nu (miss rate)
                    else:
                        X = b / (b + d)               # F (false alarm rate)
                        Y = a / (a + c)               # H (hit rate)

                    if j == 0:
                        x.append( X )
                        y.append( Y )
                    else:
                        pairs.append( (X,Y) )

                except ZeroDivisionError:
                    pass

        if curve == 'ERROR':
            x.append( 0.0 )
            y.append( 1.0 )
        else:
            x.append( 0.0 )
            y.append( 0.0 )

        dx = [ (0.0,0.0), ]
        dy = [ (0.0,0.0), ]

        siglevel = scipy.special.erf(sigma/numpy.sqrt(2))

        for i in xrange(len(thresh[0])):
            tmp = sorted([X for (X,Y) in pairs
                          if X <= x[i+1] and abs(Y-y[i+1]) <= .01],
                         reverse=True)
            try:
                dxl = x[i+1] - tmp[int(siglevel*len(tmp))]
            except:
                dxl = x[i+1] - CI(x[i+1], len(forecast)-Nobs, siglevel)[0]

            tmp = sorted([X for (X,Y) in pairs
                          if X >= x[i+1] and abs(Y-y[i+1]) <= .01],
                         reverse=False)
            try:
                dxu = tmp[int(siglevel*len(tmp))] - x[i+1]
            except:
                dxu = CI(x[i+1], len(forecast)-Nobs, siglevel)[1] - x[i+1]
            ##
            tmp = sorted([Y for (X,Y) in pairs
                          if Y <= y[i+1] and abs(X-x[i+1]) <= .01],
                         reverse=True)
            try:
                dyl = y[i+1] - tmp[int(siglevel*len(tmp))]
            except:
                dyl = y[i+1] - CI(y[i+1], Nobs, siglevel)[0]
            
            tmp = sorted([Y for (X,Y) in pairs
                          if Y >= y[i+1] and abs(X-x[i+1]) <= .01],
                         reverse=False)
            try:
                dyu = tmp[int(siglevel*len(tmp))] - y[i+1]
            except:
                dyu = CI(y[i+1], Nobs, siglevel)[1] - y[i+1]
            ###
                         
            dx.append( (dxl,dxu) )
            dy.append( (dyl,dyu) )

        dx.append( (0.0,0.0) )
        dy.append( (0.0,0.0) )

        # End _calc_curve(self, ...)
        return tuple(x), tuple(y), tuple(dx), tuple(dy)

    #-------------------------------------------------------------------------#

    def roc_area(self, x=None, y=None, dx=None, dy=None, model=None,
                 threshold=None, unit=True, sigma=1.96):
        """Calculate and return roc diagram area scores.

        Keyword arguments:
        x     -- Array of x-axis values.
        y     -- Array of y-axis values.
        dx    -- Array of x-axis confidence bands.
        dy    -- Array of y-axis confidence bands.
        model -- Reference forecast for skill score. (default None)

        threshold -- probability values for calculating miss rates and
                     fraction of alarm space. (default None)
        unit  -- construct bins uniformly over the total range? (default True)
        sigma -- sigma level for confidence bands. (default 1.96)

        If no values area passed in for x,y,dx,dy the values for
        threshold,unit,sigma will be used to generate new curve
        values.  ROC diagrams are measured by their area below the
        curve.  Error diagrams are measured by their area above the
        curve.  To calculate an area skill score, a reference model
        can be indicated.  Setting model equal to 'None' uses the
        pessimist's forecast (perfect failure) as a reference.
        Setting model equal to '0' uses the random-guessing model as a
        reference.  Otherwise, model should be an array of y-axis
        values calculated at each specified x-axis value.

        Return values:
        tuple of x values,
        tuple of area values,
        tuple of area skill score vales.
        tuple of (lower,upper) area confidence bands,
        tuple of (lower,upper) area skill score confidence bands.
        """
        if ( x == None or y == None ):
            x,y,dx,dy = self.roc(threshold, unit, sigma)

        return self._calc_curve_area('ROC', x, y, dx, dy, model)

    #-------------------------------------------------------------------------#

    def error_area(self, x=None, y=None, dx=None, dy=None, model=None,
                   threshold=None, unit=True, sigma=1.96):
        """Calculate and return error diagram area scores.

        Keyword arguments:
        x     -- Array of x-axis values. (default None)
        y     -- Array of y-axis values. (default None)
        dx    -- Array of x-axis confidence bands. (default None)
        dy    -- Array of y-axis confidence bands. (default None)
        model -- Reference forecast for skill score. (default None)

        threshold -- probability values for calculating miss rates and
                     fraction of alarm space. (default None)
        unit  -- construct bins uniformly over the total range? (default True)
        sigma -- sigma level for confidence bands. (default 1.96)

        If no values area passed in for x,y,dx,dy the values for
        threshold,unit,sigma will be used to generate new curve
        values.  ROC diagrams are measured by their area below the
        curve.  Error diagrams are measured by their area above the
        curve.  To calculate an area skill score, a reference model
        can be indicated.  Setting model equal to 'None' uses the
        pessimist's forecast (perfect failure) as a reference.
        Setting model equal to '0' uses the random-guessing model as a
        reference.  Otherwise, model should be an array of y-axis
        values calculated at each specified x-axis value.

        Return values:
        tuple of x values,
        tuple of area values,
        tuple of area skill score vales.
        tuple of (lower,upper) area confidence bands,
        tuple of (lower,upper) area skill score confidence bands.
        """
        if ( x == None or y == None ):
            x,y,dx,dy = self.error(threshold, unit, sigma)

        return self._calc_curve_area('ERROR', x, y, dx, dy, model)

    #-------------------------------------------------------------------------#

    def _calc_curve_area(self, curve, x, y, dx, dy, model):
        """Calculate and return assorted (ROC, error, etc) diagram area data.

        This is an internal function and should not be called directly.
        Instead, call the appropriate wrapper function.

        Keyword arguments:
        curve -- flag indicating which diagram measures to calculate.
                 Supported values are 'ROC' and 'ERROR'.
        x     -- Array of x-axis values.
        y     -- Array of y-axis values.
        dx    -- Array of x-axis confidence bands.
        dy    -- Array of y-axis confidence bands.
        model -- Reference forecast for skill score. (default None)

        ROC diagrams are measured by their area below the curve.
        Error diagrams are measured by their area above the curve.  To
        calculate an area skill score, a reference model can be
        indicated.  Setting model equal to 'None' uses the pessimist's
        forecast (perfect failure) as a reference.  Setting model
        equal to '0' uses the random-guessing model as a reference.
        Otherwise, model should be an array of y-axis values
        calculated at each specified x-axis value.

        Return values:
        tuple of x values,
        tuple of area values,
        tuple of area skill score vales.
        tuple of (lower,upper) area confidence bands,
        tuple of (lower,upper) area skill score confidence bands.
        """
        area = [0.0,]
        da   = [(0.0,0.0),]

        skill = [0.0,]
        ds    = [(0.0,0.0),]
        
        # Sort the arrays into increasing x direction
        X,Y,DX,DY = map(None,*sorted(zip(x,y,dx,dy)))

        # Initialize storage for curve integration
        sum = 0.0
        ref = 0.0

        suml = 0.0
        sumu = 0.0
        
        # Iterate through the x-array
        for i in xrange(1,len(X)):
            # Integrate the curve using simple trapezoids.  According
            # to Jolliffe and Stephenson, this underestimates the area
            # found by tracing the full ROC (and overestimates the
            # area found by tracing the full error diagram) due to the
            # "well-established fact that empirical ROCs on
            # probability axes are generally convex".  Trapezoids,
            # however, are less sensitive to sampling errors (due to
            # limited numbers of observations) than simple step
            # functions connecting the points.
            sum  += 0.5*(X[i] - X[i-1])*(Y[i]+Y[i-1])
            suml += 0.5*(X[i] - X[i-1])*(Y[i]-DY[i][0]+Y[i-1]-DY[i-1][0])
            sumu += 0.5*(X[i] - X[i-1])*(Y[i]+DY[i][1]+Y[i-1]+DY[i-1][1])

            # Update the area integration
            if curve == 'ROC':
                area.append(sum)
                da.append((sum-suml,sumu-sum))
            else:
                area.append(X[i]-sum)
                da.append((sumu-sum,sum-suml))

            # Calculate the reference model area
            if model == None:
                # Perfect failure reference model
                ref = 0.0

            elif model == 0:
                # Random-guessing reference model
                if curve == 'ROC':
                    ref = 0.5*X[i]**2
                else:
                    ref = X[i] - 0.5*X[i]**2

            else:
                # Use given reference model
                ref = model[i]

            # Update the skill score
            try:
                skill.append((area[-1]-ref)/(X[i]-ref))
                ds.append((da[-1][0]/(X[i]-ref),da[-1][1]/(X[i]-ref)))
            except:
                skill.append(0.0)
                ds.append((0.0,0.0))

        # End _calc_curve_area(self, ...)
        return tuple(X), tuple(area), tuple(skill), tuple(da), tuple(ds)

    #-------------------------------------------------------------------------#

    def bootstrap(self, N, observed=True, model=None, seed=None):
        """Create synthetic observed datasets based on a given distribution.

        Keyword arguments:
        N        -- Number of synthetic datasets to create.
        observed -- Draw synthetic observations from distribution of actual
                    observations? (default True)
        model    -- Distribution model to draw from if not drawing from
                    actual obersvations. (default None)
        seed     -- Seed value for random number generator. (default None)

        If no seed value is set, use the current time to initialize
        the random number generator.

        Return values:
        None
        """

        # Separate the Forecast from the observations
        F,O = [ numpy.array(col) for col in map(None, *self._data) ]

        if observed is True:
            # Create a CDF based on Observed distribution
            myCDF = GenericCDF(O, seed=seed)
        else:
            # Create a CDF based on Model distribution
            if model is None:
                myCDF = GenericCDF(F)
            else:
                myCDF = GenericCDF(model)

        # Count the number of target observations
        NN = O.sum()

        # Create the _boot object
        self._boot = numpy.zeros( (N , len(F)) , dtype=int )

        # Fill the _boot object
        for i in xrange(N):
            for n in xrange(NN):
                indx = myCDF.draw()
                self._boot[i][indx] += 1

        # End bootstrap(self, ...)
        return None

###############################################################################

#    for indices in [myCDF.draw(NN) for x in xrange(N)]:
#        [indices.count(i) for i in xrange(events)]
