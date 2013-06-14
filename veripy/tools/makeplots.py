# makeplots.py
#
# Copyright (c) 2009 James R. Holliday, jrholliday@ucdavis.edu
# See 'license.txt' for licensing and usage restrictions.
#
###############################################################################

"""Standardized forecast plotting routines.

This module exports methods for plotting the output results from
Probabilistic and Continuous forecast verification.  These methods are
works in progress.  As they become more stable, they will be moved out
of this 'makeplots' container into a 'plots' subpackage.  As such, the
current source code should probably be used as a template in your own
projects and not trusted for longevity.
"""

###############################################################################

from __future__ import division

import numpy
import matplotlib.pyplot as plt

###############################################################################

def plot_error(forecast=(), label=None, filename=None,
               symbols='os^os^', colors='brgcm'):
    """Create Error Plot."""
    plt.figure()

    plt.plot((0,1),(1,0), '--k', lw=1)
    for n in xrange(len(forecast)):
        if numpy.core.fromnumeric.sum(forecast[n][2:4]) == 0:
            try:
                plt.plot(forecast[n][0],forecast[n][1],
                         ('%c%c' % (symbols[n] , colors[n])),
                         label=label[n])
            except:
                plt.plot(forecast[0],forecast[1],
                         ('%c%c' % (symbols[0] , colors[0])))
        else:
            try:
                x0,y0,dx,dy = forecast[n]
            except:
                x0,y0,dx,dy = forecast
                
            X1 = []
            Y1 = []
            X2 = []
            Y2 = []

            for i in xrange(len(x0)):
                X1.append(max(x0[i]-dx[i][0],0))
                Y1.append(max(y0[i]-dy[i][0],0))
            for i in xrange(len(x0)-2,0,-1):
                X2.append(min(x0[i]+dx[i][1],1))
                Y2.append(min(y0[i]+dy[i][1],1))

            for i in xrange(1,len(X1)):
                X1[i] = min(X1[i],X1[i-1])
                Y1[i] = max(Y1[i],Y1[i-1])
            for i in xrange(1,len(X2)):
                X2[i] = max(X2[i],X2[i-1])
                Y2[i] = min(Y2[i],Y2[i-1])

            X = X1+X2
            Y = Y1+Y2

            plt.fill(X,Y,colors[n],alpha=.2)

            try:
                plt.plot(x0,y0,
                         ('%c%c' % (symbols[n] , colors[n])),
                         label=label[n])
            except:
                plt.plot(x0,y0,
                         ('%c%c' % (symbols[n] , colors[n])))

    plt.xlabel('Fraction of Alarm Time')
    plt.ylabel('Failure To Predict Rate')
    plt.axis((0,1,0,1))

    if len(forecast) !=4 or label is not None:
        plt.legend(loc=0, numpoints=1)

    if filename is not None:
        plt.savefig(filename)
    else:
        plt.show()

    # End plot_error(...)
    return None

#-----------------------------------------------------------------------------#

def plot_roc(forecast=(), label=None, filename=None,
               symbols='os^os^', colors='brgcm'):
    """Create ROC plot."""
    plt.figure()

    plt.plot((0,1),(0,1), '--k', lw=1)
    for n in xrange(len(forecast)):
        if numpy.core.fromnumeric.sum(forecast[n][2:4]) == 0:
            try:
                plt.plot(forecast[n][0],forecast[n][1],
                         ('%c%c' % (symbols[n] , colors[n])),
                         label=label[n])
            except:
                plt.plot(forecast[0],forecast[1],
                         ('%c%c' % (symbols[0] , colors[0])))
        else:
            try:
                x0,y0,dx,dy = forecast[n]
            except:
                x0,y0,dx,dy = forecast
                
            X1 = []
            Y1 = []
            X2 = []
            Y2 = []

            for i in xrange(len(x0)):
                X1.append(max(x0[i]-dx[i][0],0))
                Y1.append(min(y0[i]+dy[i][1],1))
            for i in xrange(len(x0)-2,0,-1):
                X2.append(min(x0[i]+dx[i][1],1))
                Y2.append(max(y0[i]-dy[i][0],0))

            for i in xrange(1,len(X1)):
                X1[i] = min(X1[i],X1[i-1])
                Y1[i] = min(Y1[i],Y1[i-1])
            for i in xrange(1,len(X2)):
                X2[i] = max(X2[i],X2[i-1])
                Y2[i] = max(Y2[i],Y2[i-1])

            X = X1+X2
            Y = Y1+Y2

            plt.fill(X,Y,colors[n],alpha=.2)

            try:
                plt.plot(x0,y0,
                         ('%c%c' % (symbols[n] , colors[n])),
                         label=label[n])
            except:
                plt.plot(x0,y0,
                         ('%c%c' % (symbols[n] , colors[n])))

    plt.xlabel('False Alarm Rate')
    plt.ylabel('Hit Rate')
    plt.axis((0,1,0,1))
    
    if len(forecast) !=4 or label is not None:
        plt.legend(loc=0, numpoints=1)

    if filename is not None:
        plt.savefig(filename)
    else:
        plt.show()

    # End plot_roc(...)
    return None

#-----------------------------------------------------------------------------#

def plot_area(forecast=(), label=None, skill=True, curve='ROC',
              filename=None, symbols='os^os^', colors='brgcm'):
    """Create Area score plot."""
    plt.figure()
    plt.plot((0,1),(0,0), '--k')

    for n in xrange(len(forecast)):
        if skill==True: indx = 2
        else: indx = 1

        try:
            plt.errorbar(forecast[n][0],forecast[n][indx],
                         map(None,*forecast[n][indx+2]),
                         marker=symbols[n], color=colors[n], label=label[n])
        except:
            plt.errorbar(forecast[0],forecast[indx],
                         map(None,*forecast[indx+2]),
                         marker=symbols[n], color=colors[n])

    if curve == 'ROC':
        plt.xlabel('False Alarm Rate')
    else:
        plt.xlabel('Fraction of Alarm Time')

    if skill == True:
        plt.ylabel('Area Skill Score')
    else:
        plt.ylabel('Area')

    if label is not None:
        plt.legend(loc=0, numpoints=1)

    if filename is not None:
        plt.savefig(filename)
    else:
        plt.show()

    # End plot_area(...)
    return None

#-----------------------------------------------------------------------------#

def plot_reliability(forecast=(), label=(), filename=None, attributes=True,
                     symbols='os^os^', colors='brgcm', limits=None):
    """Create Reliability and/or Attribute Plot."""
    
    # Can't do attribute plots for multiple forecasts
    #if len(forecast) != 4:
    #    attributes = False    
    
    plt.figure()

    if attributes is True:
        av = forecast[0][3]
        plt.fill((0,av,av,1,1,0,0),(0,0,1,1,.5*(av+1),.5*av,0),'0.8')
        plt.plot((0,1),(av,av), '--k')

    datamax = 0.0

    plt.plot((0,1),(0,1), '-k', lw=2)
    for n in xrange(len(forecast)):
        try:
            datamax = max(datamax,
                          1.1*max(max(forecast[n][0]),max(forecast[n][1])))
            if label is not None:
                plt.plot(forecast[n][0],forecast[n][1],
                         ('-%c%c' % (symbols[n] , colors[n])),
                         ms=10,lw=2,label=label[n])
            else:
                plt.plot(forecast[n][0],forecast[n][1],
                         ('-%c%c' % (symbols[n] , colors[n])),
                         ms=10,lw=2)
        except:
            datamax = max(datamax,
                          1.1*max(max(forecast[0]),max(forecast[1])))
            if label is not None:
                plt.plot(forecast[0],forecast[1],
                         ('-%c%c' % (symbols[0] , colors[0])),
                         ms=10,lw=2,label=label[n])
            else:
                plt.plot(forecast[0],forecast[1],
                         ('-%c%c' % (symbols[0] , colors[0])),
                         ms=10,lw=2)

    plt.xlabel('Forecast Probability')#, size="x-large")
    plt.ylabel('Observed Frequency')#, size="x-large")
    if limits is None:
        plt.axis((0,min(datamax,1),0,min(datamax,1)))
    else:
        plt.axis(limits)
    
    if label is not None:
        leg = plt.legend(loc=0, numpoints=1)
        #for l in leg.get_lines():
        #    l.set_linewidth(1.5)

    if attributes is True:
        a = plt.axes([0.68, 0.12, .2, .2], axisbg='w')
        plt.bar(range(len(forecast[0][2])),forecast[0][2], color='k')
        plt.setp(a, xlim=-.2, xticks=[], yticks=[])
   
    if filename is not None:
        plt.savefig(filename)
    else:
        plt.show()

    # End plot_reliability(...)
    return None

#-----------------------------------------------------------------------------#

def plot_scatter(forecast=(), label=(), filename=None, plot=0,
                 symbols='os^os^', colors='brgcm'):
    """Create Scatter Plot."""
    plt.figure()

    x_min,y_min =  99999 ,  99999
    x_max,y_max = -99999 , -99999

    for n in xrange(len(forecast)):
        try:
            x_min = min(x_min, min(forecast[n][0]))
            x_max = max(x_max, max(forecast[n][0]))

            y_min = min(y_min, min(forecast[n][1]))
            y_max = max(y_max, max(forecast[n][1]))

            plt.plot(forecast[n][0],forecast[n][1],
                     ('%c%c' % (symbols[n] , colors[n])),
                     label=label[n])
        except:
            x_min = min(x_min, min(forecast[0]))
            x_max = max(x_max, max(forecast[0]))

            y_min = min(y_min, min(forecast[1]))
            y_max = max(y_max, max(forecast[1]))
            
            plt.plot(forecast[0],forecast[1],
                     ('%c%c' % (symbols[0] , colors[0])))

    # Plot = 0 : X=Observed, Y=Forecast
    if plot is 0:
        plt.plot((min(x_min,y_min),max(x_max,y_max)),
                 (min(x_min,y_min),max(x_max,y_max)), '-k', lw=1)
        plt.xlabel('Observed')
        plt.ylabel('Forecast')

    # Plot = 1 : X=Observed, Y=Forecast-Observed
    elif plot is 1:
        plt.plot((x_min,x_max),(0,0), '-k', lw=1)
        plt.plot((x_min,x_max),(0,0), '-k', lw=1)
        plt.xlabel('Observed')
        plt.ylabel('Forecast - Observed')
        
    # Plot = 2 : X=Forecast, Y=Forecast-Observed
    elif plot is 2:
        plt.plot((x_min,x_max),(0,0), '-k', lw=1)
        plt.xlabel('Forecast')
        plt.ylabel('Forecast - Observed')
        
    # No other choices
    else:
        raise Exception("Scatter type must be 0, 1, or 2 [%s]." % plot)

    if label != ():
        plt.legend(loc=0, numpoints=1)

    if filename is not None:
        plt.savefig(filename)
    else:
        plt.show()

    # End plot_scatter(...)
    return None

###############################################################################
