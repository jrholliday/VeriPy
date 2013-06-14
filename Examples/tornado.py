#!/usr/bin/env python

import sys
sys.path.append('../')

import veripy as v

data = v.ContingencyTable( (28,72,23,2680) )

# Display the table
print "Finley's Tornado Data -",
print "(Percent Correct: %.1f%%)\n" % (100*data.stats('PC'))
print data,"\n"

# Display the statistics
results = data.stats()

for test in sorted(results.keys()):
    print "% 5s: %9.5f" % (test, results[test])

# Optimist's hypothesis: never forecast a tornado
data.set_data( (0,0,51,2752) )

print "\n\nOptimist's Forecast -",
print "(Percent Correct: %.1f%%)\n" % (100*data.stats('PC'))
print data,"\n"

results = data.stats()
for test in sorted(results.keys()):
    print "% 5s: %9.5f" % (test, results[test])

