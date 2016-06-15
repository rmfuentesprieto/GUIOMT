from cmath import phase, pi

import time

import adc5g
import Gnuplot


def calibrate_gliches(fpga,snap_a,snapc, adc, current_channel):
    if current_channel == 0:
        adc5g.sync_adc(fpga)
        opt1, glitches1 = adc5g.calibrate_mmcm_phase(fpga, adc, [snap_a, snapc, ])


def calibrate_adc(fpga, save_data, current_channel, fifo_delay_0, spec_0, fifo_delay1, spec_1):
    '''autor Rafael Rodriguez'''
    if current_channel == 0:
        save_data['cont'] = 1
        save_data['ready'] = 0
        save_data['angle'] = []
        a0 = spec_0[0][current_channel]
        a1 = spec_1[0][current_channel]
        save_data['angle'].append(phase(a0*a1.conjugate()))

        g3 = Gnuplot.Gnuplot(debug=0)
        g3.clear()
        g3.title('Phase (degree)')
        g3.xlabel('Channel #')
        g3.ylabel('Degrees')
        g3('set style data points')
        # g3('set terminal wxt size 500,300')
        g3('set yrange [-360:360]')
        g3('set xrange [0:1027]')
        g3('set ytics 10')
        g3('set xtics 256')
        g3('set grid y')
        g3('set grid x')

        save_data['plot'] = g3.plot

        return

    a0 = spec_0[0][current_channel]
    a1 = spec_1[0][current_channel]

    angle_=phase(a0*a1.conjugate())* 180 /pi
    #if angle_ < 0:
    #    angle_ = 360 + angle_

    save_data['angle'].append(angle_)
    save_data['cont'] += 1

    save_data['plot'](save_data['angle'])

    if current_channel < 10:
        return

    if save_data['cont'] >= 5 and save_data['ready'] < 4:

        save_data['cont'] = 0


        index = len(save_data['angle']) - 1
        an_m2 = save_data['angle'][index - 4]
        an_m1 = save_data['angle'][index - 3]
        an_p1 = save_data['angle'][index - 1]
        an_p2 = save_data['angle'][index]
        steigung = (-an_p2 + 8* an_p1 - 8*an_m1 + an_m2)/12.0

        if steigung > 0.08:
            print 'lol+'
            save_data['ready'] = 0
            delay = fpga.read_int(fifo_delay_0)
            fpga.write_int(fifo_delay_0, delay + 1)
        elif steigung < -0.08:
            print 'lol-'
            save_data['ready'] = 0
            delay = fpga.read_int(fifo_delay1)
            fpga.write_int(fifo_delay1, delay + 1)

        else:
            save_data['ready'] += 1

    time.sleep(1)