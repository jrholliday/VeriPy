# ContingencyTable.py
#
# Copyright (c) James R. Holliday, jrholliday@gmail.com
# See 'license.txt' for licensing and usage restrictions.
#
###############################################################################

"""Dichotomous (yes/no) contingency table.

This module exports only one object: the ContingencyTable class
definition.  This class inherits from MultiContingencyTable.
"""

###############################################################################

from __future__ import division

from MultiContingencyTable import MultiContingencyTable

import numpy
import scipy.special

###############################################################################

class ContingencyTable(MultiContingencyTable):
    """Class definition for ContingencyTable object.

    A dichotomous forecast says, 'yes, an event will happen', or 'no,
    the event will not happen'. Rain and fog prediction are common
    examples of yes/no forecasts.  Outcomes of these forecasts can be
    categorized by contingency tables.

    Data is organized and entered by listing:
        n(F=yes, O=yes), n(F=yes, O=no), n(F=no, O=yes), n(F=no, O=no)
    """

    #-------------------------------------------------------------------------#

    def set_data(self, data):
        """Enter contingency table data.  Replace old data if it exists.

        Keyword arguments:
        data -- arrary of table data.

        Data should be entered as a 4-element list:
        n(F=yes, O=yes), n(F=yes, O=no), n(F=no, O=yes), n(F=no, O=no)
        
        Return value:
        None
        """

        N = len(data)

        # Make sure a 2x2 matrix is entered.
        if N is not 4:
            raise Exception("Table data not 2x2 matrix (N=%d)" % N)
        else:
            MultiContingencyTable.set_data(self,data)

        # Set the category labels to (Y,N)
        self.set_labels(("Yes","No"))

        # End set_data(self, ...)
        return None

    #-------------------------------------------------------------------------#

    def _calc_stats(self):
        """Calculate statistics on table data.

        This is an internal function and should not be called directly.
        """

        A = int(self._data[0,0])
        B = int(self._data[0,1])
        C = int(self._data[1,0])
        D = int(self._data[1,1])

        # Calculate the "Base Rate"
        BR = ( A + C ) / ( A + B + C + D )
        self._stats['BR'] = BR

        # Calculate the "Probability of a Forcast of Occurence"
        PFO = ( A + B ) / ( A + B + C + D )
        self._stats['PFO'] = PFO

        # Calculate the "Percent Correct" ("accuracy")
        PC = ( A + D ) / ( A + B + C + D )
        self._stats['PC'] = PC

        # Calculate the "Bias Score" ("frequency bias")
        try:
            BIAS = ( A + B ) / ( A + C )
        except:
            BIAS = 0
        self._stats['BIAS'] = BIAS

        # Calculate the "Probability of Detection" ("hit rate")
        try:
            POD = A / ( A + C )
        except:
            POD = 0
        self._stats['POD'] = POD

        # Calculate the "False Alarm Ratio"
        try:
            FAR = B / ( A + B )
        except:
            FAR = 0
        self._stats['FAR'] = FAR

        # Calculate the "Probability of False Detection"
        # ("false alarm rate")
        try:
            POFD = B / ( B + D )
        except:
            POFD = 0
        self._stats['POFD'] = POFD

        # Calculate the "Threat Score" ("critical success index")
        try:
            TS = A / ( A + B + C )
        except:
            TS = 0
        self._stats['TS'] = TS

        # Calculate the "Equitable Threat Score" ("Gilbert
        # skill score")
        try:
            HR  = ( A + C ) * ( A + B ) / ( A + B + C + D )
            ETS = ( A - HR ) / (A + B + C - HR )
        except:
            ETS = 0
        self._stats['ETS'] = ETS

        # Calculate the "Peirces's Skill Score" ("Hanssen and
        # Kuipers dicriminant" or "true skill statistic")
        PSS = POD - POFD
        self._stats['PSS'] = PSS

        # Calculate the "Heidke Skill Score"
        try:
            ECR = ((A+C)*(A+B) + (C+D)*(B+D)) / (A+B+C+D)
            HSS = ((A+D)-ECR) / (A+B+C+D-ECR)
        except:
            HSS = 0
        self._stats['HSS'] = HSS

        # Calculate the "Odds Ratio"
        try:
            OR = ( POD / ( 1 - POD ) ) / ( POFD / ( 1 - POFD ) )
        except:
            OR = 0
        self._stats['OR'] = OR

        # Calculate the "Odds Ratio Skill Score" (Yule's "Q")
        try:
            ORSS = (A*D - C*B) / (A*D + C*B)
        except:
            ORSS = 0
        self._stats['ORSS'] = ORSS

        # Calculate the "Extreme Dependency Score"
        try:
            EDS = ( 2 * numpy.log(BR) / numpy.log(BR * POD) ) - 1.0
        except:
            EDS = 0
        self._stats['EDS'] = EDS

        # Calculate the "Discrimination Distance"
        D = numpy.sqrt(2) * (scipy.special.erfinv(1-2*POFD) -
                             scipy.special.erfinv(1-2*POD))
        self._stats['D'] = D

        # Calculate the "Area Under the Modelled ROC"
        Az = 0.5 + 0.5*scipy.special.erf(0.5*D)
        self._stats['Az'] = Az

        # End _calc_stats(self)
        return None

###############################################################################
