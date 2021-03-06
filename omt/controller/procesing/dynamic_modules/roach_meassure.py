def store_matrix(data_save, matrix_size_x, matrix_size_y, spectrum, current_channel, observe_spect, file_name):
    spec = spectrum[0]
    if current_channel == 0:

        matrix = []

        for cont in range(matrix_size_y):
            column = []
            for cont1 in range(matrix_size_x):
                column.append(0)

            matrix.append(column)

        matrix[0][0] = spec[observe_spect]

        data_save['matrix'] = matrix
        return

    matrix_y_dimention = len(data_save['matrix'])

    index_x = current_channel % matrix_y_dimention
    index_y = int(current_channel / matrix_y_dimention)

    if index_y % 2 == 1:
        # this is beacuse the scan is made doing a zig-zag
        index_x = matrix_size_x - 1 - index_x

    data_save['matrix'][index_y][index_x] = spec[observe_spect]

    if index_x == matrix_size_x - 1 and index_y == matrix_size_y - 1:
        FILE = open(file_name, 'w')

        for columns in data_save['matrix']:
            cont = 0
            for data in reversed(columns):
                if cont > 0:
                    FILE.write(' ,')
                cont += 1
                FILE.write('{:f}'.format(data))
            FILE.write('\n')
        FILE.close()
