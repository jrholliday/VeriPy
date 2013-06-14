# MultiContingencyTable.py
#
# Copyright (c) 2009 James R. Holliday, jrholliday@ucdavis.edu
# See 'license.txt' for licensing and usage restrictions.
#
###############################################################################

"""Multi-category contingency table.

This module exports only one object: the MultiContingencyTable class
definition.  This class also acts as a base class for ContingencyTable.
"""

###############################################################################

from __future__ import division

import numpy

###############################################################################

class MultiContingencyTable(object):
    """Class definition for MultiContingencyTable object.

    A multi-category contingency table is a generalized contingency
    table for classifying multi-category forecasts.  Data is organized
    and entered by listing:
        n(F1,O1), n(F1,02), n(F1,03), ... n(F1,Ok), n(F2,O1), ... n(Fk,Ok)
    """

    #-------------------------------------------------------------------------#

    def __init__(self, data=None):
        """Initialize MultiContingencyTable object.

        Keyword arguments:
        data -- array of table data. (default None)

        If an array of data is passed in at constuction, use it to
        populate the table.  Otherwise wait for explicit call to
        set_data(data).
        """

        # Storage for data matrix
        self._data = numpy.array([], dtype=int)
        self._data.shape = (0,0)

        # Number of categrories
        self._nCat  = 0

        # Storage for label array
        self._label = ()

        # Storage for calculated statistics
        self._stats = {}
  
        # Was a data array passed in?
        if data is not None:
            self.set_data(data)

    #-------------------------------------------------------------------------#

    def __str__(self):
        """Return string representation of table data."""

        # Calculate table totals
        N = self._data.sum()
        F = self._data.sum(axis=1)
        O = self._data.sum(axis=0)

        # Get the max "cell size"
        padding = len(str(self._data.max()))

        # Build the string representation
        rep = ""
        for i in xrange(self._nCat):
            for j in xrange(self._nCat):
                rep += "%5d" % self._data[i,j]
            rep += " |%5d\n" % F[i]
        rep += (self._nCat+1)*"-----" + "--\n"
        for i in xrange(self._nCat):
            rep += "%5d" % O[i]
        rep += " |%5d" % N

        # End __str__(self)
        return str(rep)

    #-------------------------------------------------------------------------#

    def set_data(self, data):
        """Enter contingency table data.  Replace old data if it exists.

        Keyword arguments:
        data -- arrary of table data.

        Data should be entered for the k categories as a k*k length list:
        n(F1,O1), n(F1,02), n(F1,03), ... n(F1,Ok), n(F2,O1), ... n(Fk,Ok)
        
        Return value:
        None
        """

        N = len(data)

        # Make sure a square matrix is entered.
        rootN = numpy.sqrt(N)
        
        if rootN != int(rootN):
            raise Exception("Table data not square matrix (N=%d)" % N)
        else:
            self._nCat = int(rootN)
            self._data = numpy.array(data, dtype=int)
            self._data.shape = (self._nCat,self._nCat)

        # Create default labels, if needed
        if len(self._label) != self._nCat:
            tmp = []
            for i in xrange(self._nCat):
                tmp.append("Category %d" % (i+1))
            self._label = tuple(tmp)

        # Calculate various statistics
        self._calc_stats()

        # End set_data(self, ...)
        return None

    #-------------------------------------------------------------------------#

    def set_labels(self, labels):
        """Set labels for each category."""

        if len(labels) != self._nCat:
            raise Exception(
                "Number of labels not equal to number of categories (%d!=%d)"
                % (len(labels),self._nCat))
        else:
            self._label = tuple(labels)

        # End set_labels(self, ...)
        return None

    #-------------------------------------------------------------------------#

    def _calc_stats(self):
        """Calculate statistics on table data.

        This is an internal function and should not be called directly.
        """

        # Calculate table totals
        N = self._data.sum()
        F = self._data.sum(axis=1)
        O = self._data.sum(axis=0)
        
        # Calculate the "Percent Correct" ("accuracy")
        PC = 0
        for i in xrange(self._nCat):
            PC += (self._data[i,i] / N)
        self._stats['PC'] = PC

        # Calculate the "Peirces's Skill Score" ("Hanssen and
        # Kuipers dicriminant" or "true skill statistic")
        num1, num2, denom = 0,0,0
        for i in xrange(self._nCat):
            num1  += (self._data[i,i] / N)
            num2  += (F[i] * O[i] / N / N )
            denom += (O[i] * O[i] / N / N )
        try:
            PSS = (num1 - num2)/(1-denom)
        except:
            PSS = 0
        self._stats['PSS'] = PSS

        # Calculate the "Heidke Skill Score"
        num1, num2, denom = 0,0,0
        for i in xrange(self._nCat):
            num1  += (self._data[i,i] / N)
            num2  += (F[i] * O[i] / N / N )
            denom += (F[i] * O[i] / N / N )
        try:
            HSS = (num1 - num2)/(1-denom)
        except:
            HSS = 0
        self._stats['HSS'] = HSS

        # End _calc_stats(self)
        return None

    #-------------------------------------------------------------------------#

    def stats(self, Test=None):
        """Return a copy of the calculated table statistics.

        Keyword arguments:
        Test -- the specific test result to return. (default None)

        If Test does not exist, or is None, return a dictionary of all
        test results.

        Return value:
        either calculated value of Test or dictionary of test results
        indexed by test.
        """

        # Check if Test is one of our calculated statistics.
        if Test is None:
            results = self._stats
        elif Test.upper() in self._stats.keys():
            results = self._stats[Test]
        else:
            raise Exception("'%s' is not a valid statistic." % Test)

        # End stats(self, ...)
        return results

    #-------------------------------------------------------------------------#

    def histogram(self):
        """Calculate relative frequencies of forecast and observed categories.

        Return value:
        dictionary of (forecast,observed) frequencies indexed by
        category label.
        """

        # Calculate table totals
        N = self._data.sum()
        F = 100.0 * self._data.sum(axis=1) / N
        O = 100.0 * self._data.sum(axis=0) / N

        # End histogram(self)
        return dict(zip(self._label, zip(F,O)))

###############################################################################
