#!/usr/bin/env python

import sys
sys.path.append('../')

import veripy as v

# Data was snagged from
# http://www.bom.gov.au/bmrc/wefor/staff/eee/verif/POP3/POP3.html

forecast24 = v.Probabilistic()
forecast48 = v.Probabilistic()

# Open the data file
file = open('POP_3cat_2003.txt')

# Gobble the header line
file.readline()

# Parse the data
for line in file.readlines():
    a,b,c,d,e,f,g,h,i,j = line.split()
    try:    forecast24.add_data( float(f)+float(g) , int(float(d)>0) )
    except: pass
    try:    forecast48.add_data( float(i)+float(j) , int(float(d)>0) )
    except: pass
# Close the data file

file.close()

# Make some plots
labels = ( '24-hour Forecasts' , '48-hour Forecasts' )

v.tools.plot_roc( (forecast24.roc(10) , forecast48.roc(10)) , labels )
v.tools.plot_reliability( (forecast24.reliability() ,
                           forecast48.reliability()
                           ) , labels )
