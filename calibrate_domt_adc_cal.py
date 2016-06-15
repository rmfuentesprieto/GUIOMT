#!/usr/bin/env python

'''
This script is used to calibrate all the coefficients of the four channel digital polarization isolator.
This works together with a couple of different files: calibrate_measurement.py, calibrate_functions.py, calibrate_inputs.py, calibrate_plot.py
Author: T.F.G. Geelen
email: t.f.g.geelen@gmail.com

to run this script:

python calibrate_domt.py 192.168.1.12 -b new_cal_2016_Jan_21_1802.bof -g 0xf0000000 --adc0 0 --adc1 0 --fsteps 1
'''

# Import all the necessary libraries
import corr,time,struct,sys,logging,pylab,matplotlib,Gnuplot,Gnuplot.funcutils,telnetlib
import numpy as np
import matplotlib.pyplot as plt
from math import *
import adc5g

# Import any extra files
import calibrate_measurement
import calibrate_measurement_45
import calibrate_plot

def exit_fail():
    print 'FAILURE DETECTED. Log entries:\n',lh.printMessages()
    try:
        fpga.stop()
    except: pass
    raise
    exit()

def exit_clean():
    try:
        fpga.stop()
    except: pass
    exit()

print("##########################################################")
print("             Digital OMT Calibration program              ")
print("##########################################################")
# This part of the program is the setup of all the variables and settings needed to succesfully start the program.

# Define boffile and katcp port
bitstream = "new_cal_v7.bof"
katcp_port = 7147
# Number of channels
global channels
channels = 2048
# LO frequency [GHz]
LO = 0
# RF power [dBm]
RF_power = -3


###################################################################
##########  Opening logging files  ################################
###################################################################

# Make the logging file for the output data
logfile = open('calibration_data.txt','w')

###################################################################
##########  Start of the main program  ############################
###################################################################

if __name__ == "__main__":
    from optparse import OptionParser
    p = OptionParser()
    p.set_usage("domt_calibrate.py <ROACH_HOSTNAME_or_IP> [options]")
    p.set_description(__doc__)
    p.add_option('-g', '--gain', dest='gain', type='int',default=0xf0000000,help='Set the digital gain (6bit quantisation scalar). Default is 0xf0000000, good for wideband noise. Set lower for CW tones.')
    p.add_option('-s', '--skip', dest='skip', action='store_true',help='Skip reprogramming the FPGA and configuring EQ.')
    p.add_option('-b', '--bof', dest='boffile',type='str', default='',help='Specify the bof file to load')
    p.add_option('-z', '--adc0', dest='sel_delay0',type='int', default=0,help='Set ADC0 delay')
    p.add_option('-o', '--adc1', dest='sel_delay1',type='int', default=0,help='Set ADC1 delay')
    p.add_option('-f', '--fsteps', dest='fsteps',type='int', default=1,help='Set the step of frequencies to sweep')
    opts, args = p.parse_args(sys.argv[1:])
	
    if args==[]:
        print 'Please specify a ROACH board. Run with the -h flag to see all options.\nExiting.'
        exit()
    else:
        roach_a = args[0]
    if opts.boffile != '':
        bitstream = opts.boffile
	
try:
    loggers = []
    lh=corr.log_handlers.DebugLogHandler()
    logger_a = logging.getLogger(roach_a)
    logger_a.addHandler(lh)
    logger_a.setLevel(10)  
	
    # Configuring and prepping the FPGA's
    print('Connecting to server %s on port %i... '%(roach_a,katcp_port)), 
    fpga = corr.katcp_wrapper.FpgaClient(roach_a, katcp_port,timeout=10,logger=logger_a)
    time.sleep(1)
    if fpga.is_connected():
        print "ok"
    else:
        print "ERROR connecting to server %s on port %i.\n"%(roach_a,katcp_port)
        exit_fail()
    
    print "----------------------"
    print "Programming FPGA's with %s..." %bitstream,
    if not opts.skip:
        fpga.progdev(bitstream)
        print("\nROACH 2 is programmed")
    else:
        print "Skipped"
    time.sleep(1)

###################################################################
###################  Start of the measurement #####################
###################################################################

    print "----------------------"
    # Get the clock speed of the FPGA. Useful information for in the plots.
    bw = trunc(fpga.est_brd_clk())*8
    # Note that since the ADC boards are in dual channel mode the actual bandwidth at the output is half the clock frequency
    print("ADC speed = "+str(bw))
    bw = bw/2
    print("Bandwidth = "+str(bw))

    print "----------------------"
    # Connecting to the signal generator
    generator = telnetlib.Telnet("192.168.1.34",5025)
    print("Connected to the signal generator")

    print 'Setting digital gain of all channels to %i...'%opts.gain,
    if not opts.skip:
        fpga.write_int('gain',opts.gain) # write the same gain for all inputs, all channels
        print 'done'
    else:
        print 'Skipped.'

    # Calibrating ADCs
    print 'Calibrating the time delay at the adc interface...'
    adc5g.sync_adc(fpga)
    opt1, glitches1 = adc5g.calibrate_mmcm_phase(fpga, 1,['snapshot_z1_c','snapshot_z1_a',])
    opt2, glitches2 = adc5g.calibrate_mmcm_phase(fpga, 0,['snapshot_z0_c','snapshot_z0_a',])
    time.sleep(0.5)

    # set delays on the ADC boards
    fpga.write_int('sel_delay0',opts.sel_delay0)
    fpga.write_int('sel_delay1',opts.sel_delay1)

    # Setup the plots
    g0,g1,g2,g3 = calibrate_plot.plot_setup()
    
    time.sleep(0.5)

    #first measurement
    # probe = raw_input('Enter the probe number to calibrate to: (0/1/2/3): ')
    while 1:
        probe = raw_input('Enter the probe number to calibrate to: (0/1/2/3): ')
        try:
            probe = int(probe)
            if probe in (0,1,2,3):

                break
        except:
            pass
    calibrate_measurement.measurement(0,channels,fpga,probe,g0,g1,g2,g3,generator,bw,LO,RF_power,opts.fsteps)
    raw_input('\nIt is OK?, Press enter to continue...\n')

###################################################################
#############  Begin calibration reading 0 degrees ################
###################################################################

    print("##########################################################")
    print("           Begin calibration reading 0 degrees            ")
    print("##########################################################")

    # If this setting is set to 'yes' you can define the probe to calibrate to yourself
    # probe = raw_input('Enter the probe number to calibrate to: (0/1/2/3): ')
    while 1:
        probe = raw_input('Enter the probe number to calibrate to: (0/1/2/3): ')
        try:
            probe = int(probe)
            if probe in (0,1,2,3):
                break
        except:
            pass

    # First measurement
    G = calibrate_measurement.measurement(0,channels,fpga,probe,g0,g1,g2,g3,generator,bw,LO,RF_power,opts.fsteps)

###################################################################
############  Begin calibration reading 90 degrees ################
###################################################################

    print("##########################################################")
    print("           Begin calibration reading 90 degrees           ")
    print("##########################################################")

    # If this setting is set to 'yes' you can define the probe to calibrate to yourself
    # probe = raw_input('Enter the probe number to calibrate to: (0/1/2/3)....')
    while 1:
        probe = raw_input('Enter the probe number to calibrate to: (0/1/2/3): ')
        try:
            probe = int(probe)
            if probe in (0,1,2,3):
                break
        except:
            pass

    # Second measurement
    raw_input('Press enter when ready to start the 90 degrees measurement')
    G = calibrate_measurement.measurement(1,channels,fpga,probe,g0,g1,g2,g3,generator,bw,LO,RF_power,opts.fsteps)

###################################################################
############  Begin calibration reading 45 degrees ################
###################################################################

    print("##########################################################")
    print("           Begin calibration reading 45 degrees           ")
    print("##########################################################")

    # If this setting is set to 'yes' you can define the probe to calibrate to yourself
    # probe = raw_input('Enter the probe number to calibrate to: (0/1/2/3)....')

    # Second measurement
    raw_input('Press enter when ready to start the 45 degrees measurement')
    G = calibrate_measurement_45.measurement(channels,fpga,g0,g1,g2,g3,generator,LO,RF_power,opts.fsteps, G,1)

###################################################################
### Saving the Gain matrix and displaying it in a readable sense ##
###################################################################

    print("##########################################################")
    print("                   Saving the Gain matrix                 ")
    print("##########################################################")

    raw_input('Press enter to continue...')
    for k in range(0,channels):
        logfile.write('Gain matrix for channel: '+str(k)+'\n')
        logfile.write(str(G[0,0,k]).rjust(34)+' '+str(G[0,1,k]).rjust(34)+'\n'+str(G[1,0,k]).rjust(34)+' '+str(G[1,1,k]).rjust(34)+'\n'+str(G[2,0,k]).rjust(34)+' '+str(G[2,1,k]).rjust(34)+'\n'+str(G[3,0,k]).rjust(34)+' '+str(G[3,1,k]).rjust(34)+'\n')

    print("##########################################################")
    print("                    Done calibrating                      ")
    print("##########################################################")

# Extra stuff
except KeyboardInterrupt:
    exit_clean()
except:
    exit_fail()

exit_clean()
