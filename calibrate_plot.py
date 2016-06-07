'''
This script governs all the plots for the calibration
'''

###################################################################
####################  Plotting the calibration ####################
###################################################################

import corr,time,struct,sys,logging,Gnuplot,Gnuplot.funcutils
import numpy as np
from math import *

# Function to set up the plots
def plot_setup():
# g0 = power spectra of all four channels
# g1 = calibration vectors
# g2 = final gains of the G matrix
# g3 = final phase of the G matrix
    g0 = Gnuplot.Gnuplot(debug=0)
    g1 = Gnuplot.Gnuplot(debug=0)
    g2 = Gnuplot.Gnuplot(debug=0)
    g3 = Gnuplot.Gnuplot(debug=0)
    return g0,g1,g2,g3
    
# Function to plot the spectra of the channels during the measurements
def plot_calibration(bw,power_channel1,power_channel2,power_channel3,power_channel4,magnitude,phase, amp_ratio, phase_diff,g0,g1,g2,g3):
    # Figure 1: Plot the powers of the channels.
    g0('set multiplot layout 2,2 title "Instantaneous Frequency Spectrum"')
    g0('set title "Instantaneous power channel 0"')
    g0.xlabel('Channel #')
    g0.ylabel('Power (dB)')
    g0('set style data linespoints')
    g0('set xrange [0:2048]')
    g0('set ytics 5')
    g0('set xtics 256')
    g0('set grid y')
    g0('set grid x')
    g0.plot(power_channel1)
    g0('unset key')
    g0('set title "Instantaneous power channel 1"')
    g0.xlabel('Channel #')
    g0.ylabel('Power (dB)')
    g0('set style data linespoints')
    g0('set xrange [0:2048]')
    g0('set ytics 5')
    g0('set xtics 256')
    g0('set grid y')
    g0('set grid x')
    g0.plot(power_channel2)
    g0('unset key')
    g0('set title "Instantaneous power channel 2"')
    g0.xlabel('Channel #')
    g0.ylabel('Power (dB)')
    g0('set style data linespoints')
    g0('set xrange [0:2048]')
    g0('set ytics 5')
    g0('set xtics 256')
    g0('set grid y')
    g0('set grid x')
    g0.plot(power_channel3)
    g0('unset key')
    g0('set title "Instantaneous power channel 3"')
    g0.xlabel('Channel #')
    g0.ylabel('Power (dB)')
    g0('set style data linespoints')
    g0('set xrange [0:2048]')
    g0('set ytics 5')
    g0('set xtics 256')
    g0('set grid y')
    g0('set grid x')
    g0.plot(power_channel4)
    g0('unset key')
    g0('unset multiplot')

    # Figure 2: Plot the calibration vectors
    data = np.zeros((4,4))
    for i in range(4):
        data[i, 2] = magnitude[i]*cos(phase[i])
        data[i, 3] = magnitude[i]*sin(phase[i])
    d1 = Gnuplot.PlotItems.Data(data, with_='vectors')
    g1('set title "Vectors representation of the instantaneous reading"')
    g1('set xrange[-1.5:1.5]')
    g1('set yrange[-1.5:1.5]')
    g1('set grid y')
    g1('set grid x')
    g1.plot(d1)

    # Figure 4: Plot the magnitude of each channel non normalized
    g2.clear()
    g2('set multiplot layout 1,2 title "Magnitude Ratio Max frequency = ' + str(bw) + ' MHz" ')
    g2('set title "Magnitude Ratio p1/p3"')
    g2.xlabel('Channel #')
    g2.ylabel('Power AU (dB)')
    g2('set style data linespoints')
    g2('set yrange [0:2]')
    g2('set xrange [-5:2048]')
    g2('set ytics 0.1')
    g2('set xtics 256')
    g2('set grid y')
    g2('set grid x')
    g2('set key box')
    d1 = Gnuplot.Data(amp_ratio[0],title='Magnitude Ratio p1/p3')
    g2.plot(d1)
    g2('unset key')
    g2('set title "Magnitude Ratio p2/p4"')
    g2.xlabel('Channel #')
    g2.ylabel('Power AU (dB)')
    g2('set style data linespoints')
    g2('set yrange [0:2]')
    g2('set xrange [-5:2048]')
    g2('set ytics 0.1')
    g2('set xtics 256')
    g2('set grid y')
    g2('set grid x')
    g2('set key box')
    d2 = Gnuplot.Data(amp_ratio[1],title='Magnitude Ratio p2/p4')
    g2.plot(d2)
    g2('unset key')
    g2('unset multiplot')

    # Figure 5: Plot the phase of each channel non normalized
    g3.clear()
    g3('set multiplot layout 1,2 title "Probe phase" ')
    g3('set title "Phase Difference |p1-p3|"')
    g3.xlabel('Channel #')
    g3.ylabel('Degrees')
    g3('set style data points')
    g3('set yrange [-10:10]')
    g3('set xrange [0:2048]')
    g3('set ytics 1')
    g3('set xtics 256')
    g3('set grid y')
    g3('set grid x')
    g3('set key box')
    d1 = Gnuplot.Data(phase_diff[0],title='Phase Difference |p1-p3|')
    g3.plot(d1)
    g3('unset key')
    g3('set title "Phase Difference |p1-p3|"')
    g3.xlabel('Channel #')
    g3.ylabel('Degrees')
    g3('set style data points')
    g3('set yrange [-10:10]')
    g3('set xrange [0:2048]')
    g3('set ytics 1')
    g3('set xtics 256')
    g3('set grid y')
    g3('set grid x')
    g3('set key box')
    d2 = Gnuplot.Data(phase_diff[1],title='Phase Difference |p2-p4|')
    g3.plot(d2)
    g3('unset key')
    g3('unset multiplot')
