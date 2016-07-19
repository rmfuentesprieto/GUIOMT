def ideal_calibration(current_channel, channel_offset, number_of_channels):
	if current_channel > 0:
		return

	FILE = open('ideal_omt.txt','w')

	for cont in range(number_of_channels):
		FILE.write('channel: {}\n'.format(cont))
		FILE.write('{} {}\n'.format( 0,  1))
		FILE.write('{} {}\n'.format( 0, -1))
		FILE.write('{} {}\n'.format( 1,  0))
		FILE.write('{} {}\n'.format(-1,  0))

	FILE.close()


def x_caliration(current_channel, channel_offset, number_of_channels, save_me, adc_0a, adc_0c, adc_1a, adc_1c):
	pass

def y_caliration(current_channel, channel_offset, number_of_channels, save_me, adc_0a, adc_0c, adc_1a, adc_1c):
	pass

def a45_calibration(current_channel, channel_offset, number_of_channels, save_me, adc_0a, adc_0c, adc_1a, adc_1c):
	pass

def __to_bin_cat__(type_, array):
    bin_to_return = ''

    N = len(array)

    for cont in range(N):
        bin_to_return += struct.pack(type_, array[cont])

    return bin_to_return


def load_constant_roachII(fpga, current_channel, file_name, number_of_channels):

	FILE = open(file_name,'r')

	bram_name_xfft1 = [['BRAM_hx1a_real','BRAM_hx1a_imag'],['BRAM_hx1b_real','BRAM_hx1b_imag'],['BRAM_hx1c_real','BRAM_hx1c_imag'],['BRAM_hx1d_real','BRAM_hx1d_imag']]
	bram_name_xfft2 = [['BRAM_hx2a_real','BRAM_hx2a_imag'],['BRAM_hx2b_real','BRAM_hx2b_imag'],['BRAM_hx2c_real','BRAM_hx2c_imag'],['BRAM_hx2d_real','BRAM_hx2d_imag']]
	bram_name_xfft3 = [['BRAM_hx3a_real','BRAM_hx3a_imag'],['BRAM_hx3b_real','BRAM_hx3b_imag'],['BRAM_hx3c_real','BRAM_hx3c_imag'],['BRAM_hx3d_real','BRAM_hx3d_imag']]
	bram_name_xfft4 = [['BRAM_hx4a_real','BRAM_hx4a_imag'],['BRAM_hx4b_real','BRAM_hx4b_imag'],['BRAM_hx4c_real','BRAM_hx4c_imag'],['BRAM_hx4d_real','BRAM_hx4d_imag']]

	bram_name_yfft1 = [['BRAM_hy1a_real','BRAM_hy1a_imag'],['BRAM_hy1b_real','BRAM_hy1b_imag'],['BRAM_hy1c_real','BRAM_hy1c_imag'],['BRAM_hy1d_real','BRAM_hy1d_imag']]
	bram_name_yfft2 = [['BRAM_hy2a_real','BRAM_hy2a_imag'],['BRAM_hy2b_real','BRAM_hy2b_imag'],['BRAM_hy2c_real','BRAM_hy2c_imag'],['BRAM_hy2d_real','BRAM_hy2d_imag']]
	bram_name_yfft3 = [['BRAM_hy3a_real','BRAM_hy3a_imag'],['BRAM_hy3b_real','BRAM_hy3b_imag'],['BRAM_hy3c_real','BRAM_hy3c_imag'],['BRAM_hy3d_real','BRAM_hy3d_imag']]
	bram_name_yfft4 = [['BRAM_hy4a_real','BRAM_hy4a_imag'],['BRAM_hy4b_real','BRAM_hy4b_imag'],['BRAM_hy4c_real','BRAM_hy4c_imag'],['BRAM_hy4d_real','BRAM_hy4d_imag']]

	bram = [[bram_name_xfft1, bram_name_yfft1], [bram_name_xfft2, bram_name_yfft2], [bram_name_xfft3, bram_name_yfft3], [bram_name_xfft4, bram_name_yfft4]]

	parallel_stream = 4

	data_dic = []

	for cont in range(number_of_channels/parallel_stream):
		for cont1 in range(parallel_stream):
			FILE.readline()

			# to read the matrix rows
			for cont2 in range(4):
				x_i_complex,y_i_complex = FILE.readline().split(" ",1)

				x_i_complex = float(x_i_complex) * 2**24
				y_i_complex = float(y_i_complex) * 2**24

				if not bram[cont2][0][cont1][0] in data_dic:
					data_dic[bram[cont2][0][cont1][0]] = []

				if not bram[cont2][0][cont1][1] in data_dic:
					data_dic[bram[cont2][0][cont1][1]] = []

				if not bram[cont2][1][cont1][0] in data_dic:
					data_dic[bram[cont2][1][cont1][0]] = []

				if not bram[cont2][1][cont1][1] in data_dic:
					data_dic[bram[cont2][1][cont1][1]] = []

				data_dic[bram[cont2][0][cont1][0]].append(int(x_i_complex.real))
				data_dic[bram[cont2][0][cont1][1]].append(int(x_i_complex.imag))

				data_dic[bram[cont2][1][cont1][0]].append(int(y_i_complex.real))
				data_dic[bram[cont2][1][cont1][1]].append(int(x_i_complex.imag))

	for key in data_dic:
		fpga.write(key,__to_bin_cat__('>1l',data_dic[key]),0)




