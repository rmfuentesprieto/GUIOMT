##
## Cal_phase_R2_and_cal_Data.py 192.168.1.12 -b new_cal_v7.bof -g 0xf0000000 --adc0 0 --adc1 0 --fsteps 1

#Import all the necessary libraries
import corr,time,struct,sys,logging,pylab,matplotlib,Gnuplot,Gnuplot.funcutils,telnetlib
#import katcp_wrapper,log_handlers,time,struct,sys,logging,pylab,matplotlib,Gnuplot,Gnuplot.funcutils,telnetlib
import numpy as np
import matplotlib.pyplot as plt
from math import *
import adc5g


##
from time import gmtime, strftime, localtime ##para colocar timestamp
import os# para trabaja con carpetas
katcp_port=7147
#time_stamp=strftime("%Y-%m-%d=%H-%M-%S", localtime())
time_stamp=strftime("%Y-%m-%d", localtime())
##

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
print("         Digital Sideband Separating Program              ")
print("##########################################################")
# This part of the program is the setup of all the variables and settings needed to succesfully start the program.

# Define boffile and katcp port
bitstream = "new_cal_v7.bof"
katcp_port = 7147
# Number of channels
global channels
channels = 2048
# LO frequency [GHz]
#LO = 0
# RF power [dBm]
#RF_power = 1


def get_data(fpga,channels):
    # Read the data from the outputs of the program
    # We will have to send a signal to the ROACH to signal that we are ready to collect a sample
    #fpga.write_int('data_ctrl_lec_done',0)
    #fpga.write_int('data_ctrl_sel_we',1)
    #time.sleep(1)
    # Read the software registers
    length1 = 512
    bytewidth = 8
    data_type='q'
    # Channel 1 (z1 a)
    v_z1_a0_r = struct.unpack('>' + str(length1) + data_type, fpga.read('dout0_0', length1 * bytewidth, 0))
    v_z1_a0_i = struct.unpack('>' + str(length1) + data_type, fpga.read('dout0_1', length1 * bytewidth, 0))

    v_z1_a2_r = struct.unpack('>' + str(length1) + data_type, fpga.read('dout0_2', length1 * bytewidth, 0))
    v_z1_a2_i = struct.unpack('>' + str(length1) + data_type, fpga.read('dout0_3', length1 * bytewidth, 0))

    v_z1_a4_r = struct.unpack('>' + str(length1) + data_type, fpga.read('dout0_4', length1 * bytewidth, 0))
    v_z1_a4_i = struct.unpack('>' + str(length1) + data_type, fpga.read('dout0_5', length1 * bytewidth, 0))

    v_z1_a6_r = struct.unpack('>' + str(length1) + data_type, fpga.read('dout0_6', length1 * bytewidth, 0))
    v_z1_a6_i = struct.unpack('>' + str(length1) + data_type, fpga.read('dout0_7', length1 * bytewidth, 0))

    # Channel 3 (z0 a)
    v_z0_a0_r = struct.unpack('>' + str(length1) + data_type, fpga.read('dout0_16', length1 * bytewidth, 0))
    v_z0_a0_i = struct.unpack('>' + str(length1) + data_type, fpga.read('dout0_17', length1 * bytewidth, 0))

    v_z0_a2_r = struct.unpack('>' + str(length1) + data_type, fpga.read('dout0_24', length1 * bytewidth, 0))
    v_z0_a2_i = struct.unpack('>' + str(length1) + data_type, fpga.read('dout0_25', length1 * bytewidth, 0))

    v_z0_a4_r = struct.unpack('>' + str(length1) + data_type, fpga.read('dout0_26', length1 * bytewidth, 0))
    v_z0_a4_i = struct.unpack('>' + str(length1) + data_type, fpga.read('dout0_27', length1 * bytewidth, 0))

    v_z0_a6_r = struct.unpack('>' + str(length1) + data_type, fpga.read('dout0_28', length1 * bytewidth, 0))
    v_z0_a6_i = struct.unpack('>' + str(length1) + data_type, fpga.read('dout0_29', length1 * bytewidth, 0))

    #fpga.write_int('data_ctrl_lec_done',1)
    #fpga.write_int('data_ctrl_sel_we',0)
    # Construct the spectra
    spectrum_z1_a = np.zeros(channels,dtype=complex)
    #spectrum_z1_c = np.zeros(channels,dtype=complex)
    spectrum_z0_a = np.zeros(channels,dtype=complex)
    #spectrum_z0_c = np.zeros(channels,dtype=complex)

    # The inverse gain is a bitshift to the right to counteract the effect of the quantizer.
    # Remember the quantizer makes sure the numbers are integers for easier reading.
    inverse_gain = 2**15

    spectrum_z1_a[0::4] = np.array(v_z1_a0_r) / (inverse_gain) + 1j * np.array(v_z1_a0_i) / (inverse_gain)
    spectrum_z1_a[1::4] = np.array(v_z1_a2_r) / (inverse_gain) + 1j * np.array(v_z1_a2_i) / (inverse_gain)
    spectrum_z1_a[2::4] = np.array(v_z1_a4_r) / (inverse_gain) + 1j * np.array(v_z1_a4_i) / (inverse_gain)
    spectrum_z1_a[3::4] = np.array(v_z1_a6_r) / (inverse_gain) + 1j * np.array(v_z1_a6_i) / (inverse_gain)

    spectrum_z0_a[0::4] = np.array(v_z0_a0_r) / (inverse_gain) + 1j * np.array(v_z0_a0_i) / (inverse_gain)
    spectrum_z0_a[1::4] = np.array(v_z0_a2_r) / (inverse_gain) + 1j * np.array(v_z0_a2_i) / (inverse_gain)
    spectrum_z0_a[2::4] = np.array(v_z0_a4_r) / (inverse_gain) + 1j * np.array(v_z0_a4_i) / (inverse_gain)
    spectrum_z0_a[3::4] = np.array(v_z0_a6_r) / (inverse_gain) + 1j * np.array(v_z0_a6_i) / (inverse_gain)

    return spectrum_z1_a, spectrum_z0_a

def channel_power(spectrum_z1_a, spectrum_z0_a):
    power_spectrum_z1_a = 10*np.log10(abs(spectrum_z1_a)**2+1)
    power_spectrum_z0_a = 10*np.log10(abs(spectrum_z0_a)**2+1)

    index1 = np.argmax(power_spectrum_z1_a, axis = 0)
    index3 = np.argmax(power_spectrum_z0_a, axis = 0)

    #print("The maximum of the spectrum are at channel: "+ str(index1) + ', ' + str(index3))
    return power_spectrum_z1_a, power_spectrum_z0_a

def c_angle(re,im):#complex angle / evaluates atan(Im/Re) for the 4 cuadrants
# initializing
    out=0
    if re==0:
        re=10**-20
    if im==0:
        im=10**-20
# Angle calculation
    if im>=0.0 and re>=0.0:
        out=atan(im/re)
    if im>=0.0 and re<=0.0:
        out=pi/2+atan(abs(re)/im)
    if im<=0.0 and re<=0.0:
        out=pi+atan(abs(im)/abs(re))
    if im<=0.0 and re>=0.0:
        out=(3*pi/2)+atan(re/abs(im))
    return out # the output is in radians

def trunca(f, n):
    '''Truncates/pads a float f to n decimal places without rounding'''
    slen = len('%.*f' % (n, f))
    return str(f)[:slen]
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
    p.add_option('-z', '--adc0', dest='delay_0',type='int', default=0,help='Set ADC0 delay')
    p.add_option('-o', '--adc1', dest='delay_1',type='int', default=0,help='Set ADC1 delay')
    p.add_option('-f', '--fsteps', dest='fsteps',type='int', default=1,help='Set the step of frequencies to sweep')
    opts, args = p.parse_args(sys.argv[1:])


    roach_a = '192.168.1.12'
    if opts.boffile != '':
        bitstream = opts.boffile

try:
    loggers = []
    lh=corr.log_handlers.DebugLogHandler()
    #lh = log_handlers.DebugLogHandler()
    logger_a = logging.getLogger(roach_a)
    logger_a.addHandler(lh)
    logger_a.setLevel(10)

    # Configuring and prepping the FPGA's
    print('Connecting to server %s on port %i... '%(roach_a,katcp_port)),
    fpga = corr.katcp_wrapper.FpgaClient(roach_a, katcp_port,timeout=10,logger=logger_a)
    #fpga = katcp_wrapper.FpgaClient(roach_a, katcp_port, timeout=10, logger=logger_a)
    time.sleep(1)
    if fpga.is_connected():
        print "ok"
    else:
        print "ERROR connecting to server %s on port %i.\n"%(roach_a,katcp_port)
        exit_fail()

    print "----------------------"
    print "Programming FPGA's with %s..." %bitstream,
    if not opts.skip:
        #fpga.progdev(bitstream)
        print("\nROACH 2 is programmed")
    else:
        print "Skipped"
    time.sleep(1)

###################################################################
###################  Start of the measurement #####################
###################################################################

    print "----------------------"
    # Get the clock speed of the FPGA. Useful information for in the plots.
    bw = trunc(fpga.est_brd_clk()) * 8
    # Note that since the ADC boards are in dual channel mode the actual bandwidth at the output is half the clock frequency
    print("ADC speed = " + str(bw))
    bw = bw / 2
    print("Bandwidth = " + str(bw))

    print "----------------------"
    # Connecting to the signal generator (RF)
    RF_source = telnetlib.Telnet("192.168.1.34", 5025)
    RF_source.write("power -18 dbm\r\n")
    RF_source.write("Freq "+str(bw/2)+" MHz \r\n")
    RF_source.write("OUTP:STAT ON\r\n")
    print ('RF generator ON!!')
    RF_source.write("*idn?\r\n")
    idn_rf_source=RF_source.read_until('\n', 1)
    print("Connected to the signal generator "+ ' ' + idn_rf_source)

    #### Connecting to the signal generator (LO)
    LO = 0#3000.0
    LO_source = telnetlib.Telnet("192.168.1.33", 5025)
    LO_source.write("power +18 dbm\r\n")
    LO_source.write("Freq " + str(LO) + " MHz \r\n")
    LO_source.write("OUTP:STAT ON\r\n")
    print ('LO generator ON!!')
    LO_source.write("*idn?\r\n")
    idn_lo_source = LO_source.read_until('\n', 1)
    print("Connected to the signal generator " + ' ' + idn_lo_source)

    #### Connecting to the signal generator (LO1)
    LO2 = 0.0
    #LO2 = 3000.0
    #LO2_source = telnetlib.Telnet("192.168.1.33", 5025)
    #LO2_source.write("power +18 dbm\r\n")
    #LO2_source.write("Freq " + str(LO2) + " MHz \r\n")
    #LO2_source.write("OUTP:STAT ON\r\n")
    #print ('LO2 generator ON!!')
    #LO2_source.write("*idn?\r\n")
    #idn_lo2_source = LO2_source.read_until('\n', 1)
    #print("Connected to the signal generator " + ' ' + idn_lo2_source)
    ##########
    #### Other variables (constants)
    factorM1 = 1
    factorM2 = 1
    wait = 0.1
    test = 0
    #################
    print '\nSetting digital gain of all channels to %i...\n' % opts.gain,
    if not opts.skip:
        #fpga.write_int('gain', opts.gain)  # write the same gain for all inputs, all channels
        print 'done'
    else:
        print 'Skipped.'

# Calibrating ADCs
    print '\nCalibrating the time delay at the adc interface...\n'
    adc5g.sync_adc(fpga)
    opt1, glitches1 = adc5g.calibrate_mmcm_phase(fpga, 1, ['adc1c', 'adc1a', ])
    opt2, glitches2 = adc5g.calibrate_mmcm_phase(fpga, 0, ['adc0c', 'adc0a', ])
    time.sleep(0.5)

    # set delays on the ADC boards
    #fpga.write_int('sel_delay0', opts.sel_delay0)
    #fpga.write_int('sel_delay1', opts.sel_delay1)
###### only for testing
    if test==1:
        spectrum_1, spectrum_2 = get_data(fpga,channels)
        power_spectrum_1,power_spectrum_2= channel_power(spectrum_1, spectrum_2)
        #print spectrum_1
        #print spectrum_2
        print power_spectrum_1[1]
        print power_spectrum_2[1]
        print "END!!!"
######

###### creating plots
    g0 = Gnuplot.Gnuplot(debug=0)
    g1 = Gnuplot.Gnuplot(debug=0)
    g2 = Gnuplot.Gnuplot(debug=0)
    g3 = Gnuplot.Gnuplot(debug=0)

    g0.clear()
    g0.title('i (Z1) Spectrum ' + bitstream + ' | Max frequency = ' + str(bw) + ' MHz')
    g0.xlabel('Channel #')
    g0.ylabel('power AU (dB)')
    g0('set style data linespoints')
    # g0('set terminal wxt size 500,300')
    g0('set yrange [0:100]')
    g0('set xrange [-50:1074]')
    g0('set xtics 256')
    g0('set grid y')
    g0('set grid x')

    g1.clear()
    g1.title('q (Z0) Spectrum' + bitstream + ' | Max frequency = ' + str(bw) + ' MHz')
    g1.xlabel('Channel #')
    g1.ylabel('power AU (dB)')
    g1('set style data linespoints')
    # g1('set terminal wxt size 500,300')
    g1('set yrange [0:100]')
    g1('set xrange [-50:1074]')
    g1('set xtics 256')
    g1('set grid y')
    g1('set grid x')
    #   End setting figures to be plotted

    g2.clear()
    g2.title('Amplitude Ratio')
    g2.xlabel('Channel #')
    g2.ylabel('Power AU (dB)')
    g2('set style data linespoints')
    # g2('set terminal wxt size 500,300')
    g2('set yrange [0.9:1.2]')
    g2('set xrange [-5:1027]')
    g2('set ytics 0.1')
    g2('set xtics 256')
    g2('set grid y')
    g2('set grid x')

    g3.clear()
    g3.title('Phase (degree)')
    g3.xlabel('Channel #')
    g3.ylabel('Degrees')
    g3('set style data points')
    # g3('set terminal wxt size 500,300')
    g3('set yrange [-180:180]')
    g3('set xrange [0:1027]')
    g3('set ytics 10')
    g3('set xtics 256')
    g3('set grid y')
    g3('set grid x')

    ##### Creacion de directorios#####
    ######### create files and folders
    directory = 'medida_0001'  ###'F:\RAFAEL RODRIGUEZ\google_drive_raig_account\B9_Prueba de conepto\[2016-04-08]'
    # tmp_name='\M-'+time_stamp
    # dir=directory+tmp_name
    ###tmp_name='\M-'+time_stamp+'_0000'
    direc = directory  ###directory+tmp_name
    if not os.path.exists(direc):
        os.makedirs(direc)
    indice = 0

######################################################
#############   Calibration of the ADC  ##############
######################################################

    print("######################################################")
    print("#############   Calibration of the ADC  ##############")
    print("######################################################")

    print("Calibration Phase between ADC's")
    ti=time.time()
    ### variables###
    delay = 0################
    delay_count=0############
    count_tmp=0##############
    datos_fase = np.zeros(channels, dtype=float)  # []
    phase_mean_cal=np.zeros(200,dtype=float)####
    data_usb= []

    all_data_cal_phase_adc = open(os.path.join(direc, 'all_data_cal_phase_adc_' + 'LO1_' + str(int(LO)) + '_' + 'LO2_' + str(int(LO2)) + '.dat'), 'w')

    ###
    print "Condicion" + ' ' + "5 puntos" + ' ' + "3 puntos" + ' ' + "Delay"
    all_data_cal_phase_adc.write("Condicion" + ' ' + "5 puntos" + ' ' + "3 puntos" + ' ' + "Delay\n")
    for i in range(1*2048/channels,2047,2048/channels):#USB
        t=time.time()
        RF_source.write("FREQ "+ str((LO+LO2+(2.0*i)*bw/2048)/factorM2) +" MHz\r\n")
        time.sleep(wait)
        spec_i, spec_q= get_data(fpga,channels)
        power_spec_i, power_spec_q = channel_power(spec_i, spec_q)
        if i/20==float(i)/20:
            print(str(trunca((t-ti)/60,2))+' minutes'+' '+str(trunca(float(i)*100.0/2044,2))+' %')
        g0.plot(power_spec_i)
        g1.plot(power_spec_q)

        ###################
        angle_i = np.angle(spec_i[i], deg=True)#c_angle(spec_i[2 * i], spec_i[2 * i + 1]) * 180 / (pi)  # in degrees
        angle_q = np.angle(spec_q[i], deg=True)#c_angle(spec_q[2 * i], spec_q[2 * i + 1]) * 180 / (pi)  # in degrees
        phi = c_angle(np.real(spec_i[i])*np.real(spec_q[i]) + np.imag(spec_i[i])*np.imag(spec_q[i]),
                      np.imag(spec_i[i])*np.real(spec_q[i]) - np.real(spec_i[i])*np.imag(spec_q[i]) ) * 180 / (pi)#c_angle(spec_i[2 * i] * spec_q[2 * i] + spec_i[2 * i + 1] * spec_q[2 * i + 1],spec_q[2 * i] * spec_i[2 * i + 1] - spec_i[2 * i] * spec_q[2 * i + 1]) * 180 / (pi)  # phi_f+/-phi_LO or Phi_USB from eq_13(2008)
        #amp_ratio = amp_i / amp_q  # X from eq_9(2008)
        phase_dif = (angle_i - angle_q)  # This should be equal to phi
        ####only for plotting
        datos_fase[i]=phase_dif#diferencia_fase_usb.append([i, phase_dif])
        ####
        if phase_dif < 0:
            phase_dif = 360 + phase_dif
        data_usb.append([180 - phase_dif, LO + LO2 + (2 * i) * bw / 2048])

        ########### Only for printing on screen and on "all_data" ########
        angle_i = trunca(angle_i, 2)
        angle_q = trunca(angle_q, 2)
        phase_dif = trunca(phase_dif, 2)
        phi = trunca(phi, 2)
        ########### plotting ######################
        g3.plot(datos_fase)
        #auxx=np.unwrap(diferencia_fase_usb * pi / 180) * 180 / pi
        #g3.plot(auxx)
    ######## derivartion 5 points:

        if i>10 and np.remainder(i,20)==0:
            h=1 #ancho canal
            aux=np.unwrap(datos_fase*pi/180)*180/pi
            fps=(1.0/(12*h))*(aux[i-2*h-5]-8*aux[i-1*h-5]+8*aux[i+1*h-5]-aux[i-2*h-5])
            #fps.append(fps_temp)
            #delta_fps=fps[count_tmp]-fps[count_tmp-1]
            tps=(1.0/(2*h))*(aux[i-h-5]+aux[i+h-5])
            #print fps
            if 0.2<=fps:
                delay=delay + 1
                fpga.write_int('delay_0',delay)
                print "0.2<=fps" + ' ' + str(fps) + ' ' + str(tps) + ' ' + str(delay)
                all_data_cal_phase_adc.write(str(i)+' '+"0.2<=fps" + ' ' + str(fps) + ' ' + str(tps) + ' ' + str(delay)+"\n")
            elif fps<=-0.2:
                delay =delay + 1
                fpga.write_int('delay_1', delay)
                print "fps<=-0.2" + ' ' + str(fps)+ ' ' + str(tps) +' ' +str(delay)
                all_data_cal_phase_adc.write(str(i) + ' ' +"fps<=-0.2" + ' ' + str(fps) + ' ' + str(tps) + ' ' + str(delay) + "\n")
            else:
                delay_count=delay_count+1
                print "else" + ' ' + str(fps) + ' ' + str(tps) +' ' +str(delay)
                all_data_cal_phase_adc.write(str(i) + ' ' + "else" + ' ' + str(fps) + ' ' + str(tps) +' ' +str(delay)+"\n")
                if delay_count >4:
                    adc_delay = delay
                    print 'El desfase es : ' + str(adc_delay)
                    break;
            count_tmp=count_tmp+1
    print "The ADC are Calibrated, Delay = " + str(adc_delay)
    all_data_cal_phase_adc.close()
    #RF_source.write("OUTP:STAT OFF\r\n")


    Calibration_ON = 0
    if Calibration_ON == 1:
        ##init files
        ################################################

        #all_data=direc + 'all_data_' + 'LO1_' + str(LO) + '_' + 'LO2_' + str(LO2) + '.dat'
        all_data = open(os.path.join(direc, 'all_data_' + 'LO1_' + str(int(LO)) + '_' + 'LO2_' + str(int(LO2)) + '.dat'), 'w')
        cal_data = open(os.path.join(direc, 'cal_data_' + 'LO1_' + str(int(LO)) + '_' + 'LO2_' + str(int(LO2)) + '.dat'), 'w')
        # aux variables
        arch_spec_i_usb = direc + '\spec_i_usb_' + 'LO1_' + str(int(LO)) + '_' + 'LO2_' + str(int(LO2)) + '.dat'
        arch_spec_q_usb = direc + '\spec_q_usb_' + 'LO1_' + str(int(LO)) + '_' + 'LO2_' + str(int(LO2)) + '.dat'
        arch_power_spec_i_usb = direc + '\power_spec_i_usb_' + 'LO1_' + str(int(LO)) + '_' + 'LO2_' + str(int(LO2)) + '.dat'
        arch_power_spec_q_usb = direc + '\power_spec_q_usb_' + 'LO1_' + str(int(LO)) + '_' + 'LO2_' + str(int(LO2)) + '.dat'

        arch_spec_i_lsb = direc + '\spec_i_lsb_' + 'LO1_' + str(int(LO)) + '_' + 'LO2_' + str(int(LO2)) + '.dat'
        arch_spec_q_lsb = direc + '\spec_q_lsb_' + 'LO1_' + str(int(LO)) + '_' + 'LO2_' + str(int(LO2)) + '.dat'
        arch_power_spec_i_lsb = direc + '\power_spec_i_lsb_' + 'LO1_' + str(int(LO)) + '_' + 'LO2_' + str(
            int(LO2)) + '.dat'
        arch_power_spec_q_lsb = direc + '\power_spec_q_lsb_' + 'LO1_' + str(int(LO)) + '_' + 'LO2_' + str(
            int(LO2)) + '.dat'
        #arch_power_spec_i_lsb = open(
        #    os.path.join(dir, 'power_spec_i_lsb_' + 'LO1_' + str(LO) + '_' + 'LO2_' + str(LO2) + '.dat'), 'w')
        #arch_power_spec_q_lsb = open(
        #    os.path.join(dir, 'power_spec_q_lsb_' + 'LO1_' + str(LO) + '_' + 'LO2_' + str(LO2) + '.dat'), 'w')
        #arch_power_spec_i_usb = open(
        #    os.path.join(dir, 'power_spec_i_usb_' + 'LO1_' + str(LO) + '_' + 'LO2_' + str(LO2) + '.dat'), 'w')
        #arch_power_spec_q_usb = open(
        #    os.path.join(dir, 'power_spec_q_usb_' + 'LO1_' + str(LO) + '_' + 'LO2_' + str(LO2) + '.dat'), 'w')
        #arch_spec_i_lsb = open(os.path.join(dir, 'spec_i_lsb_' + 'LO1_' + str(LO) + '_' + 'LO2_' + str(LO2) + '.dat'),
        #                       'w')
        #arch_spec_q_lsb = open(os.path.join(dir, 'spec_q_lsb_' + 'LO1_' + str(LO) + '_' + 'LO2_' + str(LO2) + '.dat'),
        #                       'w')
        #arch_spec_i_usb = open(os.path.join(dir, 'spec_i_usb_' + 'LO1_' + str(LO) + '_' + 'LO2_' + str(LO2) + '.dat'),
        #                       'w')
        #arch_spec_q_usb = open(os.path.join(dir, 'spec_q_usb_' + 'LO1_' + str(LO) + '_' + 'LO2_' + str(LO2) + '.dat'),
        #                       'w')
        #spectrum_i_lsb = []
        #spectrum_q_lsb = []
        #spectrum_i_usb = []
        #spectrum_q_usb = []


        ###init variables
        razon_amplitud_usb = np.zeros(channels, dtype=float)  # []np.arange(2, 10, dtype=np.float)
        razon_amplitud_lsb = np.zeros(channels, dtype=float)  # []
        diferencia_fase_usb = np.zeros(channels, dtype=float)  # []
        diferencia_fase_lsb = np.zeros(channels, dtype=float)  # []
        spec_i_all = np.zeros((channels,channels), dtype=complex)  # []
        spec_q_all = np.zeros((channels,channels), dtype=complex)  # []
        power_spec_i_all=np.zeros((channels,channels), dtype=float)  # []
        power_spec_q_all=np.zeros((channels,channels), dtype=float)  # []
    ####################################################
    #############   Begin measureing USB  ##############
    ####################################################
        #wait = 0.1
        data_usb = []
        print('Measuring USB')
        print("####################################################")
        print("#############   Begin measureing USB  ##############")
        print("####################################################")
        ti = time.time()
        ###
        # LO=3000.0
        #LO2 = 0.0
        #factorM2 = 1
        ###
        print('freq   amp_i   amp_q  angle_i angle_q  amp_i/q phi   phase_dif ')
        all_data.write('upper_sideband' + ' \n')
        all_data.write('#Canal' + ' ' + 'real i'.rjust(7) + ' ' + 'imag i'.rjust(7) + ' ' + 'real q'.rjust(
            7) + ' ' + 'imag q'.rjust(7) + ' ' + 'amp_i'.rjust(7) + ' ' + 'amp_q'.rjust(7) + ' ' + 'phase_i'.rjust(
            7) + ' ' + 'phase_q'.rjust(7) + ' ' + 'amp_rat'.rjust(7) + ' ' + 'ang_dif'.rjust(7) + ' ' + 'phi'.rjust(
            7) + ' \n')
        for i in range(1 * 1024 / channels, 1023, 1024 / channels):  # USB
            t = time.time()
            RF_source.write("FREQ " + str((LO + LO2 + (2.0 * i) * bw / 2048) / factorM2) + " MHz\r\n")
            time.sleep(wait)
            spec_i, spec_q = get_data(fpga, channels)
            power_spec_i, power_spec_q = channel_power(spec_i, spec_q)
            if i / 20 == float(i) / 20:
                print(str(trunca((t - ti) / 60, 2)) + ' minutes' + ' ' + str(trunca(float(i) * 100.0 / 2044, 2)) + ' %')
            g0.plot(power_spec_i)
            g1.plot(power_spec_q)
            ###################save spectrum
            spec_i_all[i][:]=spec_i
            spec_q_all[i][:] = spec_q
            power_spec_i_all[i][:] = power_spec_i
            power_spec_q_all[i][:] = power_spec_q

            #for n_ch in range(0,len(spec_i)):
            #    arch_spec_i_usb.write(str(spec_i[n_ch])+'\t')
            #    arch_spec_q_usb.write(str(spec_q[n_ch])+'\t')
            #for n_ch in range(0,len(power_spec_i)):
            #    arch_power_spec_i_usb.write(str(power_spec_i[n_ch])+'\t')
            #    arch_power_spec_q_usb.write(str(power_spec_q[n_ch])+'\t')
            #arch_spec_i_usb.write('\n')
            #arch_spec_q_usb.write('\n')
            #arch_power_spec_i_usb.write('\n')
            #arch_power_spec_q_usb.write('\n')
            ###################
            amp_i = np.absolute(spec_i[i])  # ((spec_i[2 * i]) ** 2 + (spec_i[2 * i + 1]) ** 2) ** 0.5
            # print (str(amp_i))
            amp_q = np.absolute(spec_q[i])  # ((spec_q[2 * i]) ** 2 + (spec_q[2 * i + 1]) ** 2) ** 0.5
            # print (str(amp_q))
            angle_i = np.angle(spec_i[i], deg=True)  # c_angle(spec_i[2 * i], spec_i[2 * i + 1]) * 180 / (pi)  # in degrees
            angle_q = np.angle(spec_q[i], deg=True)  # c_angle(spec_q[2 * i], spec_q[2 * i + 1]) * 180 / (pi)  # in degrees
            phi = c_angle(np.real(spec_i[i]) * np.real(spec_q[i]) + np.imag(spec_i[i]) * np.imag(spec_q[i]),
                          np.imag(spec_i[i]) * np.real(spec_q[i]) - np.real(spec_i[i]) * np.imag(spec_q[i])) * 180 / (pi)  # c_angle(spec_i[2 * i] * spec_q[2 * i] + spec_i[2 * i + 1] * spec_q[2 * i + 1],spec_q[2 * i] * spec_i[2 * i + 1] - spec_i[2 * i] * spec_q[2 * i + 1]) * 180 / (pi)  # phi_f+/-phi_LO or Phi_USB from eq_13(2008)
            amp_ratio = amp_i / amp_q  # X from eq_9(2008)
            # print (str(amp_ratio))
            phase_dif = (angle_i - angle_q)  # This should be equal to phi
            ####only for plotting
            razon_amplitud_usb[i] = amp_ratio  # razon_amplitud_usb.append([i, amp_ratio])
            diferencia_fase_usb[i] = phase_dif  # diferencia_fase_usb.append([i, phase_dif])
            ####
            if phase_dif < 0:
                phase_dif = 360 + phase_dif
            data_usb.append([1 / (amp_ratio), LO + LO2 + (2 * i) * bw / 2048])
            data_usb.append([180 - phase_dif, LO + LO2 + (2 * i) * bw / 2048])

            ########### Only for printing on screen and on "all_data" ########
            amp_i = trunca(amp_i, 2)
            amp_q = trunca(amp_q, 2)
            angle_i = trunca(angle_i, 2)
            angle_q = trunca(angle_q, 2)
            amp_ratio = trunca(amp_ratio, 2)
            phase_dif = trunca(phase_dif, 2)
            phi = trunca(phi, 2)
            print(str(trunca(LO + LO2 + (2 * i) * bw / 2048, 0)) + ' ' + str(amp_i).rjust(7) + ' ' + str(amp_q).rjust(
            7) + ' ' + str(angle_i).rjust(7) + ' ' + str(angle_q).rjust(7) + ' ' + str(amp_ratio).rjust(7) + ' ' + str(
            phi).rjust(7) + ' ' + str(phase_dif).rjust(7))
            all_data.write(
                repr(2 * i).rjust(6) + ' ' + trunca(np.real(spec_i[i]), 2).rjust(7) + ' ' + trunca(np.imag(spec_i[i]), 2).rjust(7) + ' ' + trunca(np.real(spec_q[i]), 2).rjust(7) + ' ' + trunca(np.imag(spec_q[i]), 2).rjust(7) + ' ' + (
                amp_i).rjust(7) + ' ' + (amp_q).rjust(7) + ' ' + (angle_i).rjust(7) + ' ' + (angle_q).rjust(7) + ' ' + (
                amp_ratio).rjust(7) + ' ' + (phase_dif).rjust(7) + ' ' + phi.rjust(7) + ' \n')
            ########### plotting ######################
            # g0.plot(power_spec_i)
            # g1.plot(power_spec_q)
            g2.plot(razon_amplitud_usb)
            g3.plot(diferencia_fase_usb)

        ##############################
        #arch_spec_i_usb.close()  ###close
        #arch_spec_q_usb.close()  ###
        #arch_power_spec_i_usb.close()  ###close
        #arch_power_spec_q_usb.close()  ###
        np.savetxt(arch_spec_i_usb, spec_i_all, delimiter=',', newline='\n', fmt='%.5f')
        np.savetxt(arch_spec_q_usb, spec_q_all, delimiter=',', newline='\n', fmt='%.5f')
        np.savetxt(arch_power_spec_i_usb, power_spec_i_all, delimiter=',', newline='\n', fmt='%.5f')
        np.savetxt(arch_power_spec_q_usb, power_spec_q_all, delimiter=',', newline='\n', fmt='%.5f')
        #np.savetxt('spec_i_usb.dat', spec_i_all, delimiter=',', newline='\n',fmt='%.5f')
        #np.savetxt('spec_q_usb.dat', spec_q_all, delimiter=',', newline='\n',fmt='%.5f')
        #np.savetxt('power_spec_i_usb.dat', power_spec_i_all, delimiter=',', newline='\n',fmt='%.5f')
        #np.savetxt('power_spec_q_usb.dat', power_spec_q_all, delimiter=',', newline='\n',fmt='%.5f')
        ##############################
        #########################################################
        ###############   Begin measurement LSB  ################
        #########################################################
        print("#########################################################")
        print("###############   Begin measurement LSB  ################")
        print("#########################################################")

        all_data.write('lower_sideband' + ' \n')
        all_data.write('#Canal' + ' ' + 'real i'.rjust(7) + ' ' + 'imag i'.rjust(7) + ' ' + 'real q'.rjust(
            7) + ' ' + 'imag q'.rjust(7) + ' ' + 'amp_i'.rjust(7) + ' ' + 'amp_q'.rjust(7) + ' ' + 'phase_i'.rjust(
            7) + ' ' + 'phase_q'.rjust(7) + ' ' + 'amp_rat'.rjust(7) + ' ' + 'ang_dif'.rjust(7) + ' ' + 'phi'.rjust(
            7) + ' \n')
        data_lsb = []
        print('Measuring LSB')

        print('freq   amp_i   amp_q  angle_i angle_q  amp_i/q phi   phase_dif ')
        for i in range(1 * 1024 / (channels), 1023, 1024 / (channels)):  # LSB
            t = time.time()
            RF_source.write("freq " + str((LO - LO2 - (2.0 * i) * bw / 2048) / factorM2) + "mhz\r\n")
            time.sleep(wait)
            spec_i, spec_q=get_data(fpga,channels)
            power_spec_i, power_spec_q = channel_power(spec_i, spec_q)
            #spec_i, spec_q, power_spec_i, power_spec_q = get_data()
            if i / 20 == float(i) / 20:
                print(str(trunca((t - ti) / 60, 2)) + ' minutes' + ' ' + str(trunca(50 + float(i) * 100.0 / 2044, 2)) + ' %')
            g0.plot(power_spec_i)
            g1.plot(power_spec_q)
                ###################save spectrum
            #for index in range(0, len(spec_i)):
            #    arch_spec_i_lsb.write(str(spec_i[index]) + '\t')
            #    arch_spec_q_lsb.write(str(spec_q[index]) + '\t')
            #for index in range(0, len(power_spec_i)):
            #    arch_power_spec_i_lsb.write(str(power_spec_i[index]) + '\t')
            #    arch_power_spec_q_lsb.write(str(power_spec_q[index]) + '\t')
            #arch_spec_i_lsb.write('\n')
            #arch_spec_q_lsb.write('\n')
            #arch_power_spec_i_lsb.write('\n')
            #arch_power_spec_q_lsb.write('\n')
            #############################

            amp_i =np.absolute(spec_i[i])# ((spec_i[2 * i]) ** 2 + (spec_i[2 * i + 1]) ** 2) ** 0.5
            amp_q =np.absolute(spec_q[i])# ((spec_q[2 * i]) ** 2 + (spec_q[2 * i + 1]) ** 2) ** 0.5
            angle_i = np.angle(spec_i[i], deg=True)#c_angle(spec_i[2 * i], spec_i[2 * i + 1]) * 180 / (pi)  # en grados
            angle_q = np.angle(spec_q[i], deg=True)#c_angle(spec_q[2 * i], spec_q[2 * i + 1]) * 180 / (pi)  # en grados
            phi = c_angle(np.real(spec_i[i]) * np.real(spec_q[i]) + np.imag(spec_i[i]) * np.imag(spec_q[i]),
                          np.imag(spec_i[i]) * np.real(spec_q[i]) - np.real(spec_i[i]) * np.imag(spec_q[i])) * 180 / (pi)#c_angle(spec_i[2 * i] * spec_q[2 * i] + spec_i[2 * i + 1] * spec_q[2 * i + 1], spec_q[2 * i] * spec_i[2 * i + 1] - spec_i[2 * i] * spec_q[2 * i + 1]) * 180 / (pi)  # phi_f+/-phi_LO or Phi_USB from eq_13(2008)
            amp_ratio = amp_i / amp_q  # X from eq_9(2008)
            phase_dif = (angle_i - angle_q)  # This should be equal to phi

            ####only for plotting
            razon_amplitud_lsb[i]=amp_ratio#razon_amplitud_lsb.append([i, amp_ratio])
            diferencia_fase_lsb[i]=phase_dif#diferencia_fase_lsb.append([i, phase_dif])
            ####

            if phase_dif < 0:
                phase_dif = 360 + phase_dif
            data_lsb.append([amp_ratio, LO - LO2 - (2 * i) * bw / 2048])
            data_lsb.append([phase_dif - 180, LO - LO2 - (2 * i) * bw / 2048])

            ########### Only for printing on screen and on "all_data" ########
            amp_i = trunca(amp_i, 2)
            amp_q = trunca(amp_q, 2)
            angle_i = trunca(angle_i, 2)
            angle_q = trunca(angle_q, 2)
            amp_ratio = trunca(amp_ratio, 2)
            phase_dif = trunca(phase_dif, 2)
            phi = trunca(phi, 2)
            print(str(trunca(LO - LO2 - (2 * i) * bw / 2048, 0)) + ' ' + str(amp_i).rjust(7) + ' ' + str(amp_q).rjust(
                7) + ' ' + str(angle_i).rjust(7) + ' ' + str(angle_q).rjust(7) + ' ' + str(amp_ratio).rjust(
                7) + ' ' + str(phi).rjust(7) + ' ' + str(phase_dif).rjust(7))
            all_data.write(
                repr(2 * i).rjust(6) + ' ' + trunca(np.real(spec_i[i]), 2).rjust(7) + ' ' + trunca(np.imag(spec_i[i]),                        2).rjust(7) + ' ' + trunca(np.real(spec_q[i]), 2).rjust(7) + ' ' + trunca(np.imag(spec_q[i]), 2).rjust(
                    7) + ' ' + (amp_i).rjust(7) + ' ' + (amp_q).rjust(7) + ' ' + (angle_i).rjust(7) + ' ' + (
                angle_q).rjust(7) + ' ' + (amp_ratio).rjust(7) + ' ' + (phase_dif).rjust(7) + ' ' + phi.rjust(
                    7) + ' \n')
            ########### plotting ######################
            #g0.plot(power_spec_i)
            #g1.plot(power_spec_q)
            g2.plot(razon_amplitud_lsb)
            g3.plot(diferencia_fase_lsb)

            ###########################
        #arch_spec_i_lsb.close()  ########
        #arch_spec_q_lsb.close()  #########close
        #arch_power_spec_i_lsb.close()  ########
        #arch_power_spec_q_lsb.close()  ########

        np.savetxt(arch_spec_i_lsb, spec_i_all, delimiter=',', newline='\n', fmt='%.5f')
        np.savetxt(arch_spec_q_lsb, spec_q_all, delimiter=',', newline='\n', fmt='%.5f')
        np.savetxt(arch_power_spec_i_lsb, power_spec_i_all, delimiter=',', newline='\n', fmt='%.5f')
        np.savetxt(arch_power_spec_q_lsb, power_spec_q_all, delimiter=',', newline='\n', fmt='%.5f')
            ###########################

            ########### Writing calibration data ########
            #    cal_data.write('#lower_sideband'+' \n')
        for i in range(0, len(data_lsb), 2):
            cal_data.write(
                '0 ' + str(data_lsb[i][0]) + ' ' + str(data_lsb[i][1]) + ' \n')  # stores: amp_ratio	IF_freq
        for i in range(1, len(data_lsb), 2):
            cal_data.write(
                '0 ' + str(data_lsb[i][0]) + ' ' + str(data_lsb[i][1]) + ' \n')  # stores: phase_dif-180	IF_freq
            #    cal_data.write('#upper_sideband'+' \n')
        for i in range(0, len(data_usb), 2):
            cal_data.write(
                '0 ' + str(data_usb[i][0]) + ' ' + str(data_usb[i][1]) + ' \n')  # stores: 1/amp_ratio	IF_freq
        for i in range(1, len(data_usb), 2):
            cal_data.write(
                '0 ' + str(data_usb[i][0]) + ' ' + str(data_usb[i][1]) + ' \n')  # stores: 180-phase_dif 	IF_freq
        tf = time.time()
        print('Calibration Done!      Total time=' + repr(trunca((tf - ti) / 60, 1)) + ' minutes')


# Extra stuff
except KeyboardInterrupt:
    #RF_source.write("OUTP:STAT OFF\r\n")
    exit_clean()
except:
    #RF_source.write("OUTP:STAT OFF\r\n")
    exit_fail()

#raw_input()
exit_clean()

