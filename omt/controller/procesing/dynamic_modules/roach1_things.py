from cmath import phase

import Gnuplot


def cal_phase_ampl(save_me, ab_spec, b_square, current_channel):

    spec_ab = ab_spec[0]
    spec_bb = b_square[0]

    if current_channel == 0:
        save_me['fft_ang'] = []
        save_me['fft_amplt'] = []

        if spec_bb[current_channel+4] == 0:
            amp = 0
        else:
            amp = abs(spec_ab[current_channel+4] / spec_bb[current_channel+4])
        phase_ = phase(spec_ab[current_channel+4])

        save_me['fft_ang'].append(phase_)
        save_me['fft_amplt'].append(amp)

        g2 = Gnuplot.Gnuplot(debug=0)
        g2.clear()
        g2.title('Phase (degree)')
        g2.xlabel('Channel #')
        g2.ylabel('Degrees')
        g2('set style data points')
        #2g3('set terminal wxt size 500,300')
        g2('set yrange [0:2]')
        g2('set xrange [0:256]')
        g2('set ytics 0.1')
        g2('set xtics 16')
        g2('set grid y')
        g2('set grid x')

        save_me['plot_p'] = g2.plot

        g3 = Gnuplot.Gnuplot(debug=0)
        g3.clear()
        g3.title('amplitud')
        g3.xlabel('Channel #')
        g3.ylabel('Degrees')
        g3('set style data points')
        # g3('set terminal wxt size 500,300')
        g3('set yrange [-6:6]')
        g3('set xrange [0:256]')
        g3('set ytics 0.35')
        g3('set xtics 16')
        g3('set grid y')
        g3('set grid x')

        save_me['plot_a'] = g3.plot

        return


    if spec_bb[current_channel+4] == 0:
        amp = 0
    else:
        amp = abs(spec_ab[current_channel+4] / spec_bb[current_channel+4])
    phase_ = phase(spec_ab[current_channel+4])

    save_me['fft_ang'].append(phase_)
    save_me['fft_amplt'].append(amp)	

    save_me['plot_a'](save_me['fft_ang'])
    save_me['plot_p'](save_me['fft_amplt'])