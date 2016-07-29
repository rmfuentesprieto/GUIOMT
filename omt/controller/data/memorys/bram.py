from math import log10

import numpy
import struct

from omt.controller.data.memorys.memory import Memory
from omt.util.data_type import data_type_dictionart


class BRam(Memory):

    def __init__(self, array_id,  bram_names, data_type, data_length, does_plot, plot, does_write, write, reg_name, fpga):
        self.data_r = []
        self.data_i = []
        self.array_size = data_length
        self.data_type = data_type
        self.bram_names = bram_names
        self.reg_name = reg_name
        self.array_id = array_id
        self.does_plot = does_plot
        self.plot = plot
        self.does_write = does_write
        self.write = write
        self.count = -1
        self.initial_count = -2
        if reg_name:
            self.initial_count = fpga.read_int(reg_name)


    def does_write(self):
        return False

    def interact_roach(self, fpga):
        self.data_r = []
        self.data_i = []

        for name_r, name_i in self.bram_names:
            if len(name_r) > 0:
                self.data_r += struct.unpack('>' + self.array_size + self.data_type,
                                           fpga.read(name_r,
                                                     str(int(self.array_size)*data_type_dictionart[self.data_type]),
                                                     0))
            else:
                self.data_r += [0] * int(self.array_size)

            if len(name_i) > 0:
                self.data_i += struct.unpack('>' + self.array_size + self.data_type,
                                           fpga.read(name_i,
                                                     str(int(self.array_size)*data_type_dictionart[self.data_type]),
                                                     0))
            else:
                self.data_i += [0] * int(self.array_size)

    def has_acc_len(self):
        return not self.reg_name == ''

    def get_acc_len_reg_name(self):
        return self.reg_name

    def get_value_name(self):
        return self.array_id

    def get_value(self):
        size = int(self.array_size)
        final = []

        for cont1 in range(size):
            for cont in range(len(self.bram_names)):
                index = size*cont + cont1
                final.append(self.data_r[index] + 1j* self.data_i[index])

        # plot and store the data

        if self.does_plot:
            aplot = self.plot
            aplot.clear()

            acc_count = self.count
            #data = 10*numpy.log10(1.0+numpy.absolute(final))
            data = []
            for val in final:
                r2 = abs(val*val.conjugate()) + 1.0
                power = 10*log10(r2)
                data.append(power)
            x_range = int(numpy.amax(data) * 1.1)
            phase_max = numpy.amax(abs(numpy.angle(final)*180/3.141592))

            if phase_max > 5:

                aplot('set multiplot layout 2,1 rowsfirst')
                aplot('set yrange [0:%s]' % (str(x_range)))
                aplot('set xrange [0:%s]' % (len(data),))
                aplot('set ytics 10')
                aplot('set xtics %s' % (len(data)/16,))
                aplot.plot(data)
                aplot.ylabel('Phase [degree]')
                aplot('set ytics 20')
                aplot('set xtics %s' %(len(data)/16,))
                aplot('set yrange [-181:181]')
                aplot('set xrange [0:%s]' % (len(data),))
                aplot.plot(abs(numpy.angle(final)*180/3.141592))

                aplot('unset multiplot')
            else:
                aplot('set yrange [0:%s]' % (str(x_range)))
                aplot('set xrange [0:%s]' % (len(data),))
                aplot('set xtics 16')

                aplot.plot(data)
            aplot.title('plot of data array %s, acc count %s'%(self.array_id,str(acc_count)))
            #time.sleep(0.1)

        if self.does_write:
            files = self.write
            str_final = []
            for data in final:
                str_final.append('{:f}'.format(data))

            files[0].writerow(str_final)

        return final,self.count

    def set_acc_count(self, count):
        self.count = count
