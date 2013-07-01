# GenericCDF.py
#
# Copyright (c) James R. Holliday, jrholliday@gmail.com
# See 'license.txt' for licensing and usage restrictions.
#
###############################################################################

"""Generic CDF construction and sampling.

This module exports only one object: the GenericCDF class definition.
"""

###############################################################################

import random

###############################################################################

class GenericCDF:
    """
    This class takes in an arbitrary array and creates a normalized
    CDF.  The user can then draw array indicies from the distribition.

    Sample usage:
        myCDF = GenericCDF(array, Normalized=False)
        myCDF.draw()
    """

    #-------------------------------------------------------------------------#

    def __init__(self, array, Normalized=False, seed=None):
        """Initialize GenericCDF object.

        Keyword arguments:
        array      -- distribution array to sample from.
        Normalized -- does the input distribution sum to 1? (default False)
        seed       -- seed value for random number generator (default None)

        Class initialization requires an input array.  If the array is
        already normalized (sum of all values is 1.0), the second
        argument can be set to True.  Default behavior is to go ahead
        and (re)normalize the array.  If no value is intered for the
        random number generator seed, the current time will be used.
        """
        self._cdf = []

        # Seed the RNG
        random.seed(seed)

        # Calculate normalization factor
        norm = 0.0
        if Normalized:
            norm=1.0
        else:
            for value in array:
                norm += value

        # Integrate the array and create the CDF
        sum = 0.0
        for value in array:
            sum += value
            self._cdf.append(sum/norm)

    #-------------------------------------------------------------------------#

    def draw(self, N=1):
        """Draw an array index from the inpyt distribution array."""
        indices = []

        for i in xrange(N):
            indx = 0

            # Draw a uniform random number (0,1] and find where it
            # falls in our CDF.
            rng = random.random()
            while ( (self._cdf[indx] < rng) and (indx < len(self._cdf) - 1) ):
                indx += 1

            indices.append(indx)

        # Return the array indices.
        return (indices[0] if N==1 else indices)

###############################################################################
