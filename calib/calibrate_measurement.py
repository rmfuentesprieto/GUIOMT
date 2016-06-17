
'''
This scripts governs the measurements
'''

###################################################################
####################  A calibration reading #######################
###################################################################
import corr,time,struct,sys,logging,pylab,matplotlib,Gnuplot,Gnuplot.funcutils
import numpy as np
import matplotlib.pyplot as plt
from math import *

# Import dependent files
import calibrate_functions
import calibrate_inputs
import calibrate_plot

# Some matrices for efficiency
phase = np.zeros(4)
consistent_phase = np.zeros((4,4))
G = np.zeros((4,2,2048),dtype=complex)
power_plot = np.zeros((4,2048))
phase_plot = np.zeros((6,2048))
total_magnitude = np.zeros((4,2,2048))
total_phase = np.zeros((4,2,2048))

# This function is the heart of the program and governs what happens during a mesaurement.
def measurement(reading,channels,fpga,probe,g0,g1,g2,g3,generator,bw,LO,RF_power,fsteps):

    print("LO frequency must be "+str(LO)+"[GHz] (manual set)")
    print( "Current RF power is set to: "+ str(RF_power) + "dBm")
    generator.write("power "+repr(RF_power)+"dbm\r\n")
    generator.write("Output on\r\n")
    for channel_number in range(0,channels,fsteps):
        print("##########################################################")
        print("               Current channel = "+str(channel_number)+"               ")
        print("##########################################################")
        # A calculation to see what the current frequency should be (in MHz) and setting the signal generator to the middle of a spectral channel
        freq = bw/float(channels)*(channel_number)
        freq = max(0.01,freq + LO*1000)     # LO addition
        print( "Current frequency is set to: "+ str(freq) + "MHz")
        generator.write("freq "+repr(freq)+"mhz\r\n")
        time.sleep(0.2)

        # Read the data from the ROACH
        spectrum_z1_a, spectrum_z1_c, spectrum_z0_a, spectrum_z0_c = calibrate_inputs.get_data(fpga, channels)

        # Constructing the voltage vectors V. We are only interested in the channel where the tone is, the rest can be discarded.
        V = np.array([spectrum_z1_a[channel_number], spectrum_z1_c[channel_number], spectrum_z0_a[channel_number], spectrum_z0_c[channel_number]])

        # Computing the power of the spectra for plotting
        power_spectrum_z1_a, power_spectrum_z1_c, power_spectrum_z0_a, power_spectrum_z0_c = calibrate_functions.channel_power(spectrum_z1_a, spectrum_z1_c, spectrum_z0_a, spectrum_z0_c, channels)

        print("\nVoltage vector V = "+str(V)+"\n")

        # Check if the channel with the maximum power correspond to the input frequency
        V_power = 10*np.log10((1+abs(V)**2))
        print("Powers on channel: ")
        print(V_power)
        print("")

        # Constructing the matrix M = <VV*> where V is the vector composed of the channels
        M = calibrate_functions.compute_m(V)
        print("The cross-spectrum matrix M =")
        print M

        # Computing the magnitudes of M
        magnitude = calibrate_functions.compute_mag(M)
        print('\nMagnitude is equal to: '+str(magnitude)+'\n')

        # Computing the phase of M
        rel_phase = calibrate_functions.compute_relative_phase(M)
        print('Relative phase is equal to:\n')
        print rel_phase

        # According to the probe settings the maximum is either user-defined or chosen by the maximum correlation
        index = int(probe)

        # Normalising the matrix and changing to the definite phases
        if index == 0:
            phase[0] = rel_phase[index,0]
            phase[1] = rel_phase[index,1]
            phase[2] = rel_phase[index,2]
            phase[3] = rel_phase[index,3]
        elif index == 1:
            phase[0] = rel_phase[index,0]
            phase[1] = rel_phase[index,1]
            phase[2] = rel_phase[index,2]
            phase[3] = rel_phase[index,3]
        elif index == 2:
            phase[0] = rel_phase[index,0]
            phase[1] = rel_phase[index,1]
            phase[2] = rel_phase[index,2]
            phase[3] = rel_phase[index,3]
        elif index == 3:
            phase[0] = rel_phase[index,0]
            phase[1] = rel_phase[index,1]
            phase[2] = rel_phase[index,2]
            phase[3] = rel_phase[index,3]
        else:
            print('No valid index for the phase')

#        # Normalising the matrix and changing to the definite phases
#        if index == 0:
#            phase[0] = 0
#            phase[1] = -rel_phase[index,1]
#            phase[2] = -rel_phase[index,2]
#            phase[3] = -rel_phase[index,3]
#        elif index == 1:
#            phase[0] = -rel_phase[index,0]
#            phase[1] = 0
#            phase[2] = -rel_phase[index,2]
#            phase[3] = -rel_phase[index,3]
#        elif index == 2:
#            phase[0] = -rel_phase[index,0]
#            phase[1] = -rel_phase[index,1]
#            phase[2] = 0
#            phase[3] = -rel_phase[index,3]
#        elif index == 3:
#            phase[0] = -rel_phase[index,0]
#            phase[1] = -rel_phase[index,1]
#            phase[2] = -rel_phase[index,2]
#            phase[3] = 0
#        else:
#            print('No valid index for the phase')

        # Writing the phases and magnitudes of the channels into a larger array. This is used to plot the increase of the phase and magnitude over the measurement.
        for i in range(4):
            total_magnitude[i][reading][channel_number] = magnitude[i]
            total_phase[i][reading][channel_number] = phase[i]
        print('\nNormalisation has been done, the results are: \nMagnitude: '+str(magnitude)+'\nPhase:     '+str(phase)+'\n')

        # See if the data is consistent (a.k.a. sanity check)
        calibrate_functions.consistency_magnitude(M)
        consistent_phase = calibrate_functions.consistency_phase(M)

        # Plot the spectra
        calibrate_plot.plot_calibration(channels,channel_number, power_spectrum_z1_a, power_spectrum_z1_c, power_spectrum_z0_a, power_spectrum_z0_c,magnitude,phase,total_magnitude, total_phase,g0,g1,g2,g3)

        # Saving the coefficients:
        for i in range(0,4):
            G[i,reading,channel_number] = magnitude[i]*cos(phase[i])+1j*magnitude[i]*sin(phase[i])

    # Saving the relevant plots
    #g2.hardcopy('normalized_magnitude.ps', enhanced =1, color=1)
    #g3.hardcopy('normalized_phase.ps', enhanced =1, color=1)
    raw_input('press enter to continue')
    return G    
