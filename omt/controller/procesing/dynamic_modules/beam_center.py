import Gnuplot


def disp_max(save_me, spec1,spec2, channel, name='no label'):
    m_spec1 = spec1[0]
    m_spec2 = spec2[0]

    if not save_me:
        g2 = Gnuplot.Gnuplot(debug=0)
        g2.clear()
        g2.title(name)
        g2.xlabel('Channel #')
        g2.ylabel('amplitud Ratio')
        g2('set style data points')
        #2g3('set terminal wxt size 500,300')
        g2('set yrange [0:2]')
        g2('set xrange [0:256]')
        g2('set ytics 0.1')
        g2('set xtics 16')
        g2('set grid y')
        g2('set grid x')
        save_me['plot'] = g2.plot

        value1 = abs(m_spec1[channel] * m_spec1[channel].conjugate())
        value2 = abs(m_spec2[channel] * m_spec2[channel].conjugate())
        ratio = 0 if value2 == 0 else value1/value2
        save_me['ampl'] = [ratio,]
        return
    value1 = abs(m_spec1[channel] * m_spec1[channel].conjugate())
    value2 = abs(m_spec2[channel] * m_spec2[channel].conjugate())
    ratio = 0 if value2 == 0 else value1/value2
    save_me['ampl'].append(ratio)

    save_me['plot'] (save_me['ampl'])