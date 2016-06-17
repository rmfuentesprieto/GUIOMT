import numpy

import calibrate_inputs


def measurement(channels, fpga,g0, g1, g2, g3, generator, LO, RF_power, fsteps, gain_matrix_g, s0):

    print("LO frequency must be "+str(LO)+"[GHz] (manual set)")
    print( "Current RF power is set to: "+ str(RF_power) + "dBm")
    generator.write("power "+repr(RF_power)+"dbm\r\n")
    generator.write("Output on\r\n")
    bw = 600.0

    s0_2 = s0*s0

    for channel_number in range(0, channels, fsteps):
        print("##########################################################")
        print("               Current channel = "+str(channel_number))
        print("##########################################################")
        # A calculation to see what the current frequency should be (in MHz) and setting the signal generator to the middle of a spectral channel
        freq = (bw/channels)*(channel_number)
        freq = max(0.01, freq + LO*1000)     # LO addition
        print( "Current frequency is set to: "+ str(freq) + "MHz")
        generator.write("freq "+str(freq)+"mhz\r\n")
        #time.sleep(0.05)

        spectrum_z1_a, spectrum_z1_c, spectrum_z0_a, spectrum_z0_c = calibrate_inputs.get_data(fpga, channels)

        # Constructing the voltage vectors V. We are only interested in the channel where the tone is, the rest can be discarded.
        V = numpy.array([spectrum_z1_a[channel_number], spectrum_z1_c[channel_number], spectrum_z0_a[channel_number], spectrum_z0_c[channel_number]])

        gain_matrix_h = numpy.linalg.pinv( gain_matrix_g[:][:][channel_number])

        # obtain the estimated values of given the partialy
        # calibrated matrix
        s_prima = gain_matrix_h*V

        # convert from linear polarization to circular
        to_circular_matrix = numpy.matrix('1 -1j; 1 1j')
        s_circular = to_circular_matrix*s_prima

        # get the square module of each polarization component
        s_left_abs_2 = s_circular[0]*s_circular[0].conjugate()
        s_rigth_abs_2 = s_circular[1]*s_circular[1].conjugate()

        # get the value of eps given equation 22a of the paper
        # compact orthomode transducers using digital polarizatio synthesis
        sin_eps = (s_left_abs_2 + s_rigth_abs_2)/(2*s0_2) - 1.0
        eps = numpy.arcsin(sin_eps)

        # values that are needed for leater
        cos_eps = numpy.cos(eps)
        sin_2_eps = 2*sin_eps*cos_eps

        # calculate phi given equation 22b
        sin_phi = (s_left_abs_2 - s_rigth_abs_2)/(s0_2*(sin_2_eps + 2*cos_eps))
        s_cross_product = s_circular[0]*s_circular[1]
        cos_phi = 2*(numpy.imag(s_cross_product))/(s0_2*(sin_2_eps + 2*cos_eps))

        # the rotations matrix given equaton 24
        rotation_matrix_eps = numpy.matrix('1 %f;0 %f'.format(sin_eps,cos_eps))
        rotation_matrix_phi = numpy.matrix('1 0;0 {:.2f}'.format(cos_phi + 1j*sin_phi))

        gain_matrix_g[:][:][channel_number] = gain_matrix_g[:][:][channel_number] * rotation_matrix_phi * rotation_matrix_eps

    return gain_matrix_g





