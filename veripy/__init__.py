# __init.py__
#
# Copyright (c) James R. Holliday, jrholliday@gmail.com
# See 'license.txt' for licensing and usage restrictions.
#
###############################################################################

"""VeriPy --- A forecast verification package for Python"""

###############################################################################

def license():
    """Display license and copyright notice for the VeriPy package."""

    import pydoc

    # Read in the license text
    file = open( __path__[0] + '/license.txt' )
    text = file.read()
    file.close()

    # Use python pager to display the license text
    pydoc.pager(text)

    # End license()
    return None

#-----------------------------------------------------------------------------#

__all__ = []

for subpackage in ['ContingencyTable',
                   'MultiContingencyTable',
                   'Probabilistic',
                   'Continuous',
                   'tools']:

    exec 'from ' + subpackage + ' import *'
    __all__.append( subpackage )

###############################################################################
