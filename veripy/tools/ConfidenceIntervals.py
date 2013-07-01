# ConfidenceIntervals.py
#
# Copyright (c) James R. Holliday, jrholliday@gmail.com
# See 'license.txt' for licensing and usage restrictions.
#
###############################################################################

"""Sampling uncertainty and confidence intervals.

This module exports functions for estimating confidence intervals on
performace measures.
"""

###############################################################################

from __future__ import division

import numpy
import scipy.special

###############################################################################

def CI(p, n, sigma=1.96):
    """Calculate confidence interval for a given probability measure.

    Keyword arguments:
    p     - Probability measure.  Should/must be between 0 and 1.
    n     - Sample size.
    sigma - Sigma level. (Default 1.96)

    This function should be used when the sample estimate is a
    probability measure.  In this special case, it can reasonably be
    expeted to have the sampling distribution of a proportion, and the
    binomial distribution can be used.  The default value of sigma
    (1.96) corresponds to a 95% confidence interval.

    Return value:
    lower confidence level.
    upper confidence level.
    """

    lower = (p + sigma**2/2/n -
             sigma*numpy.sqrt((p*(1-p) + sigma**2/4./n)/n)) / (1 + sigma**2/n)
    upper = (p + sigma**2/2/n +
             sigma*numpy.sqrt((p*(1-p) + sigma**2/4./n)/n)) / (1 + sigma**2/n)

    # End CI(...)
    return ( lower , upper )

###############################################################################
