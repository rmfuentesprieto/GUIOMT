def store_matrix_fast(data_save, matrix_size_x, matrix_size_y, spectrum, current_channel, observe_spect, file_name):

	spec = spectrum[0]
	if current_channel == 0:

		matrix_x = []
		matrix_y = []

		for cont in range(matrix_size_y):
			matrix_y.append(0)
		for cont in range(matrix_size_x):
			matrix_x.append(0)

		matrix_y[0] = spec[observe_spect]

		data_save['matrix_x'] = matrix_x
		data_save['matrix_y'] = matrix_y

	
	if current_channel >= matrix_size_y:
		index = current_channel %matrix_size_y
		data_save['matrix_x'][index] = spec[observe_spect]
	else:
		data_save['matrix_y'][current_channel] = spec[observe_spect]



	if current_channel == (matrix_size_y + matrix_size_x - 1):
		FILE = open(file_name, 'w')

		for data in data_save['matrix_x']:
			FILE.write('{:f}, '.format(data))
		FILE.write('\n')
		for data in data_save['matrix_y']:
			FILE.write('{:f}, '.format(data))

		FILE.close()



