'''
This script governs the the reading of the BRAM modules in the model
'''

###################################################################
###########  Reading the registers and processing them ############
###################################################################

# Any necessary library imports
import corr,time,struct,sys,logging
import numpy as np
from math import *

# This function reads the ROACH
def get_data(fpga,channels):
    # Read the data from the outputs of the program
    # We will have to send a signal to the ROACH to signal that we are ready to collect a sample
    fpga.write_int('data_ctrl_lec_done',0)
    fpga.write_int('data_ctrl_sel_we',1)
    # Read the software registers
    # Read the software registers
    length1 = 512
    bytewidth = 8
    # Channel 1 (z1 a)
    v_z1_a0_r = struct.unpack('>512q',fpga.read('doutv_z1_a0_r',length1*bytewidth,0))
    v_z1_a0_i = struct.unpack('>512q',fpga.read('doutv_z1_a0_i',length1*bytewidth,0))
    v_z1_a1_r = struct.unpack('>512q',fpga.read('doutv_z1_a1_r',length1*bytewidth,0))
    v_z1_a1_i = struct.unpack('>512q',fpga.read('doutv_z1_a1_i',length1*bytewidth,0))
    v_z1_a2_r = struct.unpack('>512q',fpga.read('doutv_z1_a2_r',length1*bytewidth,0))
    v_z1_a2_i = struct.unpack('>512q',fpga.read('doutv_z1_a2_i',length1*bytewidth,0))
    v_z1_a3_r = struct.unpack('>512q',fpga.read('doutv_z1_a3_r',length1*bytewidth,0))
    v_z1_a3_i = struct.unpack('>512q',fpga.read('doutv_z1_a3_i',length1*bytewidth,0))
    # Channel 2 (z1 c)
    v_z1_c0_r = struct.unpack('>512q',fpga.read('doutv_z1_c0_r',length1*bytewidth,0))
    v_z1_c0_i = struct.unpack('>512q',fpga.read('doutv_z1_c0_i',length1*bytewidth,0))
    v_z1_c1_r = struct.unpack('>512q',fpga.read('doutv_z1_c1_r',length1*bytewidth,0))
    v_z1_c1_i = struct.unpack('>512q',fpga.read('doutv_z1_c1_i',length1*bytewidth,0))
    v_z1_c2_r = struct.unpack('>512q',fpga.read('doutv_z1_c2_r',length1*bytewidth,0))
    v_z1_c2_i = struct.unpack('>512q',fpga.read('doutv_z1_c2_i',length1*bytewidth,0))
    v_z1_c3_r = struct.unpack('>512q',fpga.read('doutv_z1_c3_r',length1*bytewidth,0))
    v_z1_c3_i = struct.unpack('>512q',fpga.read('doutv_z1_c3_i',length1*bytewidth,0))
    # Channel 3 (z0 a)
    v_z0_a0_r = struct.unpack('>512q',fpga.read('doutv_z0_a0_r',length1*bytewidth,0))
    v_z0_a0_i = struct.unpack('>512q',fpga.read('doutv_z0_a0_i',length1*bytewidth,0))
    v_z0_a1_r = struct.unpack('>512q',fpga.read('doutv_z0_a1_r',length1*bytewidth,0))
    v_z0_a1_i = struct.unpack('>512q',fpga.read('doutv_z0_a1_i',length1*bytewidth,0))
    v_z0_a2_r = struct.unpack('>512q',fpga.read('doutv_z0_a2_r',length1*bytewidth,0))
    v_z0_a2_i = struct.unpack('>512q',fpga.read('doutv_z0_a2_i',length1*bytewidth,0))
    v_z0_a3_r = struct.unpack('>512q',fpga.read('doutv_z0_a3_r',length1*bytewidth,0))
    v_z0_a3_i = struct.unpack('>512q',fpga.read('doutv_z0_a3_i',length1*bytewidth,0))
    # Channel 4 (z0 c)
    v_z0_c0_r = struct.unpack('>512q',fpga.read('doutv_z0_c0_r',length1*bytewidth,0))
    v_z0_c0_i = struct.unpack('>512q',fpga.read('doutv_z0_c0_i',length1*bytewidth,0))
    v_z0_c1_r = struct.unpack('>512q',fpga.read('doutv_z0_c1_r',length1*bytewidth,0))
    v_z0_c1_i = struct.unpack('>512q',fpga.read('doutv_z0_c1_i',length1*bytewidth,0))
    v_z0_c2_r = struct.unpack('>512q',fpga.read('doutv_z0_c2_r',length1*bytewidth,0))
    v_z0_c2_i = struct.unpack('>512q',fpga.read('doutv_z0_c2_i',length1*bytewidth,0))
    v_z0_c3_r = struct.unpack('>512q',fpga.read('doutv_z0_c3_r',length1*bytewidth,0))
    v_z0_c3_i = struct.unpack('>512q',fpga.read('doutv_z0_c3_i',length1*bytewidth,0))
    # Send a signal that we are done sampling the data from the registers
    fpga.write_int('data_ctrl_lec_done',1)
    fpga.write_int('data_ctrl_sel_we',0)

    # Construct the spectra
    spectrum_z1_a = np.zeros(channels,dtype=complex)
    spectrum_z1_c = np.zeros(channels,dtype=complex)
    spectrum_z0_a = np.zeros(channels,dtype=complex)
    spectrum_z0_c = np.zeros(channels,dtype=complex)

    # The inverse gain is a bitshift to the right to counteract the effect of the quantizer.
    # Remember the quantizer makes sure the numbers are integers for easier reading.
    inverse_gain = 15

    spectrum_z1_a[0::4] = np.array(v_z1_a0_r)/(2**inverse_gain-1) + 1j*np.array(v_z1_a0_i)/(2**inverse_gain-1)
    spectrum_z1_a[1::4] = np.array(v_z1_a1_r)/(2**inverse_gain-1) + 1j*np.array(v_z1_a1_i)/(2**inverse_gain-1)
    spectrum_z1_a[2::4] = np.array(v_z1_a2_r)/(2**inverse_gain-1) + 1j*np.array(v_z1_a2_i)/(2**inverse_gain-1)
    spectrum_z1_a[3::4] = np.array(v_z1_a3_r)/(2**inverse_gain-1) + 1j*np.array(v_z1_a3_i)/(2**inverse_gain-1)

    spectrum_z1_c[0::4] = np.array(v_z1_c0_r)/(2**inverse_gain-1) + 1j*np.array(v_z1_c0_i)/(2**inverse_gain-1)
    spectrum_z1_c[1::4] = np.array(v_z1_c1_r)/(2**inverse_gain-1) + 1j*np.array(v_z1_c1_i)/(2**inverse_gain-1)
    spectrum_z1_c[2::4] = np.array(v_z1_c2_r)/(2**inverse_gain-1) + 1j*np.array(v_z1_c2_i)/(2**inverse_gain-1)
    spectrum_z1_c[3::4] = np.array(v_z1_c3_r)/(2**inverse_gain-1) + 1j*np.array(v_z1_c3_i)/(2**inverse_gain-1)

    spectrum_z0_a[0::4] = np.array(v_z0_a0_r)/(2**inverse_gain-1) + 1j*np.array(v_z0_a0_i)/(2**inverse_gain-1)
    spectrum_z0_a[1::4] = np.array(v_z0_a1_r)/(2**inverse_gain-1) + 1j*np.array(v_z0_a1_i)/(2**inverse_gain-1)
    spectrum_z0_a[2::4] = np.array(v_z0_a2_r)/(2**inverse_gain-1) + 1j*np.array(v_z0_a2_i)/(2**inverse_gain-1)
    spectrum_z0_a[3::4] = np.array(v_z0_a3_r)/(2**inverse_gain-1) + 1j*np.array(v_z0_a3_i)/(2**inverse_gain-1)

    spectrum_z0_c[0::4] = np.array(v_z0_c0_r)/(2**inverse_gain-1) + 1j*np.array(v_z0_c0_i)/(2**inverse_gain-1)
    spectrum_z0_c[1::4] = np.array(v_z0_c1_r)/(2**inverse_gain-1) + 1j*np.array(v_z0_c1_i)/(2**inverse_gain-1)
    spectrum_z0_c[2::4] = np.array(v_z0_c2_r)/(2**inverse_gain-1) + 1j*np.array(v_z0_c2_i)/(2**inverse_gain-1)
    spectrum_z0_c[3::4] = np.array(v_z0_c3_r)/(2**inverse_gain-1) + 1j*np.array(v_z0_c3_i)/(2**inverse_gain-1)

    return spectrum_z1_a, spectrum_z1_c, spectrum_z0_a, spectrum_z0_c

    # # Construct the spectra
    # power_spec_z1_a = []
    # power_spec_z1_c = []
    # power_spec_z0_a = []
    # power_spec_z0_c = []
    #
    # # Construct the spectra
    # spectrum_z1_a = np.zeros(channels,dtype=complex)
    # spectrum_z1_c = np.zeros(channels,dtype=complex)
    # spectrum_z0_a = np.zeros(channels,dtype=complex)
    # spectrum_z0_c = np.zeros(channels,dtype=complex)
    #
    # # The inverse gain is a bitshift to the right to counteract the effect of the quantizer.
    # # Remember the quantizer makes sure the numbers are integers for easier reading.
    # inverse_gain = 32
    #
    # spectrum_z1_a[0::4] = np.array(v_z1_a0_r)/(2**inverse_gain-1) + 1j*np.array(v_z1_a0_i)/(2**inverse_gain-1)
    # spectrum_z1_a[1::4] = np.array(v_z1_a1_r)/(2**inverse_gain-1) + 1j*np.array(v_z1_a1_i)/(2**inverse_gain-1)
    # spectrum_z1_a[2::4] = np.array(v_z1_a2_r)/(2**inverse_gain-1) + 1j*np.array(v_z1_a2_i)/(2**inverse_gain-1)
    # spectrum_z1_a[3::4] = np.array(v_z1_a3_r)/(2**inverse_gain-1) + 1j*np.array(v_z1_a3_i)/(2**inverse_gain-1)
    #
    # spectrum_z1_c[0::4] = np.array(v_z1_c0_r)/(2**inverse_gain-1) + 1j*np.array(v_z1_c0_i)/(2**inverse_gain-1)
    # spectrum_z1_c[1::4] = np.array(v_z1_c1_r)/(2**inverse_gain-1) + 1j*np.array(v_z1_c1_i)/(2**inverse_gain-1)
    # spectrum_z1_c[2::4] = np.array(v_z1_c2_r)/(2**inverse_gain-1) + 1j*np.array(v_z1_c2_i)/(2**inverse_gain-1)
    # spectrum_z1_c[3::4] = np.array(v_z1_c3_r)/(2**inverse_gain-1) + 1j*np.array(v_z1_c3_i)/(2**inverse_gain-1)
    #
    # spectrum_z0_a[0::4] = np.array(v_z0_a0_r)/(2**inverse_gain-1) + 1j*np.array(v_z0_a0_i)/(2**inverse_gain-1)
    # spectrum_z0_a[1::4] = np.array(v_z0_a1_r)/(2**inverse_gain-1) + 1j*np.array(v_z0_a1_i)/(2**inverse_gain-1)
    # spectrum_z0_a[2::4] = np.array(v_z0_a2_r)/(2**inverse_gain-1) + 1j*np.array(v_z0_a2_i)/(2**inverse_gain-1)
    # spectrum_z0_a[3::4] = np.array(v_z0_a3_r)/(2**inverse_gain-1) + 1j*np.array(v_z0_a3_i)/(2**inverse_gain-1)
    #
    # spectrum_z0_c[0::4] = np.array(v_z0_c0_r)/(2**inverse_gain-1) + 1j*np.array(v_z0_c0_i)/(2**inverse_gain-1)
    # spectrum_z0_c[1::4] = np.array(v_z0_c1_r)/(2**inverse_gain-1) + 1j*np.array(v_z0_c1_i)/(2**inverse_gain-1)
    # spectrum_z0_c[2::4] = np.array(v_z0_c2_r)/(2**inverse_gain-1) + 1j*np.array(v_z0_c2_i)/(2**inverse_gain-1)
    # spectrum_z0_c[3::4] = np.array(v_z0_c3_r)/(2**inverse_gain-1) + 1j*np.array(v_z0_c3_i)/(2**inverse_gain-1)
    #
    # for i in range(0,4*512,1):
    #     power_spec_z1_a.append(10*log10(1+(abs(spectrum_z1_a[i]))**2))
    #     power_spec_z1_c.append(10*log10(1+(abs(spectrum_z1_c[i]))**2))
    #     power_spec_z0_a.append(10*log10(1+(abs(spectrum_z0_a[i]))**2))
    #     power_spec_z0_c.append(10*log10(1+(abs(spectrum_z0_c[i]))**2))
    #
    # return spectrum_z1_a, spectrum_z1_c, spectrum_z0_a, spectrum_z0_c, power_spec_z1_a, power_spec_z1_c, power_spec_z0_a, power_spec_z0_c