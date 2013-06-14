#!/usr/bin/env python

import sys
sys.path.append('../')

import veripy as v
import random as rand

data1 = v.Probabilistic()
data2 = v.Probabilistic()

for i in xrange(100):
    x = rand.random()
    data1.add_data( x , int(rand.random()<.5) )
    data2.add_data( x , int(rand.random()< x) )

data1.print_stats()
print ""
data2.print_stats()
print ""

labels = ( 'Pure Noise' , 'Noisy Regression' )

# Make plots
v.tools.plot_roc( (data1.roc(10),data2.roc(10)) , labels )
v.tools.plot_error( (data1.error(10),data2.error(10)) , labels )
v.tools.plot_reliability( (data1.reliability(), data2.reliability()) , labels)

v.tools.plot_area( (data1.roc_area(threshold=10, model=0),
                    data2.roc_area(threshold=10, model=0)) ,
                   labels ,
                   skill=False,
                   curve='ROC' )

v.tools.plot_area( (data1.roc_area(threshold=10, model=0),
                    data2.roc_area(threshold=10, model=0)) ,
                   labels ,
                   skill=True,
                   curve='ROC' )
