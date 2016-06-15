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
G = np.zeros((4,2,2048),dtype=complex)
mag_ratio = np.zeros((2,2048))
phase_dif = np.zeros((2,2048))

# This function is the heart of the program and governs what happens during a mesaurement.
def measurement(reading, channels, fpga, probe, g0, g1, g2, g3, generator, bw, LO, RF_power, fsteps):

    print("LO frequency must be "+str(LO)+"[GHz] (manual set)")
    print( "Current RF power is set to: "+ str(RF_power) + "dBm")
    generator.write("power "+repr(RF_power)+"dbm\r\n")
    generator.write("Output on\r\n")
    bw = 600.0

    for channel_number in range(0,channels,fsteps):
        print("##########################################################")
        print("               Current channel = "+str(channel_number)+"               ")
        print("##########################################################")
        # A calculation to see what the current frequency should be (in MHz) and setting the signal generator to the middle of a spectral channel
        freq = (bw/channels)*(channel_number)
        freq = max(0.01, freq + LO*1000)     # LO addition
        print( "Current frequency is set to: "+ str(freq) + "MHz")
        generator.write("freq "+str(freq)+"mhz\r\n")
        #time.sleep(0.05)

        # Read the data from the ROACH
        spectrum_z1_a, spectrum_z1_c, spectrum_z0_a, spectrum_z0_c = calibrate_inputs.get_data(fpga, channels)

        # Constructing the voltage vectors V. We are only interested in the channel where the tone is, the rest can be discarded.
        V = np.array([spectrum_z1_a[channel_number], spectrum_z1_c[channel_number], spectrum_z0_a[channel_number], spectrum_z0_c[channel_number]])

        # Computing the power of the spectra for plotting
        power_spec_z1_a, power_spec_z1_c, power_spec_z0_a, power_spec_z0_c = calibrate_functions.channel_power(spectrum_z1_a, spectrum_z1_c, spectrum_z0_a, spectrum_z0_c)

        print("\nVoltage vector V = "+str(V)+"\n")

        ### Computing the coefficients of G: ###
        # Computing the magnitudes of G: a_ix,y
        magnitude = calibrate_functions.compute_mag(V)
        print('\nMagnitude is equal to: '+str(magnitude)+'\n')

        # Computing the phase of G: theta_ix,y
        rel_phase = calibrate_functions.compute_relative_phase(V)
        print('Relative phase is equal to:\n')
        print rel_phase

        amp_ratio = calibrate_functions.compute_mag_ratio(magnitude,probe)
        phase_diff = calibrate_functions.compute_phase_diff(rel_phase,probe)

        if phase_diff<0:
            phase_diff=360+phase_diff

        ####only for plotting
        mag_ratio[reading][channel_number] = amp_ratio
        phase_dif[reading][channel_number] = phase_diff
        ####
        # Plot the spectra
        calibrate_plot.plot_calibration(bw, power_spec_z1_a, power_spec_z1_c, power_spec_z0_a, power_spec_z0_c,magnitude,rel_phase,mag_ratio, phase_dif,g0,g1,g2,g3)

        # Saving the coefficients:
        for i in range(0,4):
            G[i,reading,channel_number] = magnitude[i]*cos(rel_phase[i])+1j*magnitude[i]*sin(rel_phase[i])

    # Saving the relevant plots
    g2.hardcopy('normalized_magnitude.ps', enhanced =1, color=1)
    g3.hardcopy('normalized_phase.ps', enhanced =1, color=1)
    raw_input('press enter to continue')
    return G    
