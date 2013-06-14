#!/usr/bin/env python

from distutils.core import setup

DESCRIPTION="""\
There are many different types of forecasts, and each type requires its
own methods of testing and verification. Similarly, for a given forecast
there are many different types of tests which can be performed, and the
forecast may perform differently on different tests. Care must be taken
to chose an appropriate test and to interpret the results correctly.
This package attempts to create a standard set of tools for use in
general verifications of generic forecast data sets. 
"""

setup(name='VeriPy',
      version='0.8',
      description='Forecast Verification Utilities',
      long_description=DESCRIPTION,
      platforms=('All',),
      author='James R Holliday',
      author_email='jrholliday@gmail.com',
      url='https://github.com/jrholliday/VeriPy',
      license='MAME',
      packages=['veripy', 'veripy.tools'],
      package_data={'veripy': ['license.txt']},
      )

