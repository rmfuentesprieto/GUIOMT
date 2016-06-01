#!/usr/bin/env python
'''
para correr la calibracion:

./calibracion_r2.py 192.168.1.12 -g 4294967296 -b cal_r2_2016_Jan_22_1745.bof


\nAuthor: Andres Alvear, January 2016.
'''


import corr,time,numpy,struct,sys,logging,pylab,matplotlib,math,Gnuplot, Gnuplot.funcutils,array, telnetlib, valon_synth
from math import *
import adc5g

bitstream = 'No_bof_file_error'
katcp_port=7147

def creartxt():
    archi=open('datos.dat','w')
    archi.close()

def creartxt():
    archi_teo=open('datos_teo.dat','w')
    archi_teo.close()

archi=open('datos.dat','a')
archi_teo=open('datos_teo.dat','a')    

creartxt()

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
'''
def get_data():
    #get the data...    

    fpga.write_int('data_ctrl_lec_done',0)
    fpga.write_int('data_ctrl_sel_we',1)   

    re_0i=struct.unpack('>512q',fpga.read('dout0_0',512*8,0))
    im_0i=struct.unpack('>512q',fpga.read('dout0_1',512*8,0))
    re_1i=struct.unpack('>512q',fpga.read('dout0_2',512*8,0))
    im_1i=struct.unpack('>512q',fpga.read('dout0_3',512*8,0))
    re_2i=struct.unpack('>512q',fpga.read('dout0_4',512*8,0))
    im_2i=struct.unpack('>512q',fpga.read('dout0_5',512*8,0))
    re_3i=struct.unpack('>512q',fpga.read('dout0_6',512*8,0))
    im_3i=struct.unpack('>512q',fpga.read('dout0_7',512*8,0))
#
    re_4q=struct.unpack('>512q',fpga.read('dout0_8',512*8,0))
    im_4q=struct.unpack('>512q',fpga.read('dout0_9',512*8,0))
    re_5q=struct.unpack('>512q',fpga.read('dout0_10',512*8,0))
    im_5q=struct.unpack('>512q',fpga.read('dout0_11',512*8,0))
    re_6q=struct.unpack('>512q',fpga.read('dout0_12',512*8,0))
    im_6q=struct.unpack('>512q',fpga.read('dout0_13',512*8,0))
    re_7q=struct.unpack('>512q',fpga.read('dout0_14',512*8,0))
    im_7q=struct.unpack('>512q',fpga.read('dout0_15',512*8,0))

    fpga.write_int('data_ctrl_lec_done',1)
    fpga.write_int('data_ctrl_sel_we',0)

    spec_i=[]
    spec_q=[]
    power_spec_i=[]
    power_spec_q=[]
    amp_dif=[]
    phase_dif=[]
    e=10**-10
#    
    for i in range(512):
        spec_i.append(float(re_0i[i])/(2**18))
        spec_i.append(float(im_0i[i])/(2**18))
        spec_i.append(float(re_1i[i])/(2**18))
        spec_i.append(float(im_1i[i])/(2**18))
        spec_i.append(float(re_2i[i])/(2**18))
        spec_i.append(float(im_2i[i])/(2**18))
        spec_i.append(float(re_3i[i])/(2**18))
        spec_i.append(float(im_3i[i])/(2**18))

        spec_q.append(float(re_4q[i])/(2**18))
        spec_q.append(float(im_4q[i])/(2**18))
        spec_q.append(float(re_5q[i])/(2**18))
        spec_q.append(float(im_5q[i])/(2**18))
        spec_q.append(float(re_6q[i])/(2**18))
        spec_q.append(float(im_6q[i])/(2**18))
        spec_q.append(float(re_7q[i])/(2**18))
        spec_q.append(float(im_7q[i])/(2**18))

    
    return spec_i, spec_q
'''
def get_data():
    #get the data...    

    fpga.write_int('data_ctrl_lec_done',0)
    fpga.write_int('data_ctrl_sel_we',1)   

    re_0i=struct.unpack('>512q',fpga.read('dout0_0',512*8,0))
    im_0i=struct.unpack('>512q',fpga.read('dout0_1',512*8,0))
    re_2i=struct.unpack('>512q',fpga.read('dout0_2',512*8,0))
    im_2i=struct.unpack('>512q',fpga.read('dout0_3',512*8,0))
#
    re_0q=struct.unpack('>512q',fpga.read('dout1_0',512*8,0))
    im_0q=struct.unpack('>512q',fpga.read('dout1_1',512*8,0))
    re_2q=struct.unpack('>512q',fpga.read('dout1_2',512*8,0))
    im_2q=struct.unpack('>512q',fpga.read('dout1_3',512*8,0))

    fpga.write_int('data_ctrl_lec_done',1)
    fpga.write_int('data_ctrl_sel_we',0)

    spec_i=[]
    spec_q=[]
    power_spec_i=[]
    power_spec_q=[]
    amp_dif=[]
    phase_dif=[]
    e=10**-10

    from math import log10
#   
    inverse_gain = 2**18
    for i in range(512):
        spec_i.append(log10(float(abs(re_0i[i] + 1j*im_0i[i]) + 1.0)*10))
        spec_i.append(log10(float(abs(re_2i[i] + 1j*im_2i[i]) + 1.0)*10))
        spec_q.append(log10(float(abs(re_0q[i] + 1j*im_0q[i]) + 1.0)*10))
        spec_q.append(log10(float(abs(re_2q[i] + 1j*im_2q[i]) + 1.0)*10))
        #print spec_i[2]
        #print spec_q[2]

    
    return spec_i, spec_q


def arcotan(im,re):
    tan=0
    if im>=0.0 and re>=0.0:
        if re==0:
	    re=10**-20
        tan=atan(im/re)
    if im>=0.0 and re<=0.0:
        if im==0:
	    im=10**-20        	
        tan=pi/2+atan(abs(re)/im)
    if im<=0.0 and re<=0.0:
        if re==0:
	    re=10**-20
        tan=pi+atan(abs(im)/abs(re))
    if im<=0.0 and re>=0.0:
        if im==0:
	    im=10**-20
        tan=(3*pi/2)+atan(re/abs(im))
    return tan

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


    g0 = Gnuplot.Gnuplot(debug=0)
    g1 = Gnuplot.Gnuplot(debug=0)

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

    lo=0#input('LO frequency MHZ?)')
    #lo = lo/4.0
    start=lo-bw
    stop=lo+bw

    g0.clear()    
    g0.title('Upper Side Band amplitude ratio '+bitstream+' | Max frequency = '+str(bw)+' MHz')
    g0.xlabel('Channel #')
    g0.ylabel('Power AU (dB)')
    g0('set style data linespoints')

    g0('set grid y')
    g0('set grid x')	

    g1.clear()    
    #g1.title('ADC0 spectrum using '+bitstream+' | Max frequency = '+str(bw)+' MHz')
    #g1('unset key')
    g1('set title "Probe phase Upper Side Band"')
    g1.xlabel('Channel #')
    g1.ylabel('Degrees')
    g1('set style data linespoints')

    g1('set grid y')
    g1('set grid x')
    #g1('set key box')
    #g1('unset multiplot')


    print 'Configuring FFT shift register...',
    fpga.write('shift_ctrl','\x00\x00\x0f\xff')
    print 'done'
#
    print 'Resetting counters...',
    fpga.write_int('cnt_rst',1) 
    fpga.write_int('cnt_rst',0) 
    print 'done'
#
    ti=time.time()
    #bw=trunc(fpga.est_brd_clk())*4
        #rys = telnetlib.Telnet("192.168.1.35",5025)
    #valon=valon_synth.Synthesizer('/dev/ttyUSB0')
    while 1:
    	a,b = get_data()

    	g1.plot(a)
    	g0.plot(b)


except KeyboardInterrupt:
    exit_clean()
except:
    exit_fail()

exit_clean()

