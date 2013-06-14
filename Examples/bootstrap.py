#!/usr/bin/env python

import sys
sys.path.append('../')

import veripy as v

NSHM = v.Probabilistic()

# Load in National Seismic Hazard Map data
file = open('NSHM-21.dat')
for line in file.readlines():
    f,o = line.split()[2:4]
    NSHM.add_data(float(f),int(o))
file.close()

NSHM.bootstrap(100)

rocData = ( NSHM.roc(sigma=3) , NSHM.roc(sigma=1) )
labels  = ( '3-sigma confidence band' , '1-sigma confidence band' )

v.tools.plot_roc(rocData,labels)

