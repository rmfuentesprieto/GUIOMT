import Gnuplot


def disp_max(save_me, spec, channel):
    m_spec = spec[0]
    if not save_me:
        g2 = Gnuplot.Gnuplot(debug=0)
        g2.clear()
        
        save_me['plot'] = g2.plot

        value = abs(m_spec[channel] * m_spec[channel].conjugate())

        save_me['plot']((value,))
    value = abs(m_spec[channel] * m_spec[channel].conjugate())

    save_me['plot']((value,))