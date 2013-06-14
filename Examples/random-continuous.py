#!/usr/bin/env python

import sys
sys.path.append('../')

import veripy as v
import random as rand

data = v.Continuous()

for i in xrange(100):
    x = .1 + .8*rand.random()
    y = x + .2*rand.random() - .1
    data.add_data( x , y )

data.print_stats()
print ""

# Make scatter plots
v.tools.plot_scatter( (data.scatter(),) , label=('Random Noise',) )

v.tools.plot_scatter( data.scatter(1) , plot=1)
v.tools.plot_scatter( data.scatter(2) , plot=2)
