import numpy


def calibratoin(global_save, current_channel, initial, step, spec_a0, spec_c0, spec_a1, spec_c1, calibration_mode, fft_size,s0):
    '''Convention

    a1 = porbe 1
    c1 = probe 3
    a0 = probe 2
    c0 = probe 4'''

    spec_a0 = spec_a0[0]
    spec_c0 = spec_c0[0]
    spec_a1 = spec_a1[0]
    spec_c1 = spec_c1[0]

    if current_channel == 0:
        if not'g_matrix' in global_save:
            global_save['g_matrix'] = G = numpy.zeros((4,2,fft_size),dtype=complex)

    index = current_channel*step + initial

    v1 = spec_a1[index]
    v2 = spec_a0[index]
    v3 = spec_c1[index]
    v4 = spec_c0[index]

    if calibration_mode == 0:
        ref = v1/abs(v1) * s0

    if calibration_mode == 1:
        ref = v2/abs(v2) * s0

    v1 = v1 / ref
    v2 = v2 / ref
    v3 = v3 / ref
    v4 = v4 / ref

    global_save['g_matrix'][0][calibration_mode][current_channel] = v1
    global_save['g_matrix'][1][calibration_mode][current_channel] = v2
    global_save['g_matrix'][2][calibration_mode][current_channel] = v3
    global_save['g_matrix'][3][calibration_mode][current_channel] = v4

def calibratoin(global_save, current_channel, initial, step, spec_a0, spec_c0, spec_a1, spec_c1,  s0):

    s0_2 = s0*s0
    spec_a0 = spec_a0[0]
    spec_c0 = spec_c0[0]
    spec_a1 = spec_a1[0]
    spec_c1 = spec_c1[0]

    index = current_channel*step + initial

    v1 = spec_a1[index]
    v2 = spec_a0[index]
    v3 = spec_c1[index]
    v4 = spec_c0[index]

    V = numpy.matrix([v1],[v2],[v3],[v4])

    gain_matrix_h = numpy.linalg.pinv(global_save['g_matrix'][:][:][current_channel])

    s_prima = numpy.dot(gain_matrix_h,V)

    #print s_prima.shape
    # convert from linear polarization to circular
    to_circular_matrix = numpy.matrix('1 -1j; 1 1j')
    s_circular = numpy.dot(to_circular_matrix,s_prima)

    # get the square module of each polarization component
    s_left_abs_2 = numpy.dot(s_circular[0],s_circular[0].conjugate())[0,0]
    s_rigth_abs_2 = numpy.dot(s_circular[1],s_circular[1].conjugate())[0,0]

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
    rotation_matrix_eps = numpy.matrix('1 {:.2f};0 {:.2f}'.format(sin_eps.item(),cos_eps.item()))
    rotation_matrix_phi = numpy.matrix('1 0;0 {:.2f}'.format((cos_phi + 1j*sin_phi).item()))

    global_save['g_matrix'][:][:][current_channel] = \
        global_save['g_matrix'][:][:][current_channel] * rotation_matrix_phi * rotation_matrix_eps

def write_constant_to_bram(global_save, fpga, bram_name, size, step):
    pass
