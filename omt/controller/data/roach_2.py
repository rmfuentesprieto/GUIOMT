import csv
import os
import struct
import corr
import logging
import time

import datetime
import numpy
from Gnuplot import Gnuplot

from omt.controller.abstract_parallel_proces import Process
from omt.util.data_type import data_type_dictionart


class Roach2(object):

    def __init__(self, data_dic):
        print data_dic
        self.port = int(data_dic['port'])
        self.ip = data_dic['ip']
        self.register_list = data_dic['reg']
        self.bof_path = data_dic['bof_path']
        self.bitstream = data_dic['name'] + '.bof'
        self.brams_info = data_dic['bram']

        self.plot_brams = []
        self.store_drams = []

        for cont in range(len(self.brams_info)):
            aplot = None
            if self.brams_info[cont]['plot']:
                aplot = Gnuplot(debug=1)
                aplot.clear()
                aplot('set style data linespoints')
                aplot.ylabel('Power AU (dB)')
                aplot('set xrange [-50:2098]')
                aplot('set yrange [0:100]')
                aplot('set ytics 5')
                aplot('set xtics 256')
                aplot('set grid y')
                aplot('set grid x')
            self.plot_brams.append(aplot)

            astore = None

            if self.self.brams_info[cont]['store']:
                ts = time.time()
                time_stamp = st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
                file_name = self.bof_path[:-len('.bof')] + time_stamp + '.csv'
                file = open(file_name, 'w')

                csv_writer = csv.writer(file, delimiter = ',')
                astore = (csv_writer,file)
            self. store_drams.append(astore)

        self.fpga = None

        self.handler = corr.log_handlers.DebugLogHandler()
        self.logger = logging.getLogger(self.ip)
        self.logger.addHandler(self.handler)
        self.logger.setLevel(10)

    def connect_to_roach(self):
        print self.port
        self.fpga = corr.katcp_wrapper.FpgaClient(self.ip, self.port, timeout=10, logger=self.logger)
        time.sleep(1)

    def is_conected(self):
        print 'roach'
        to_return = self.fpga.is_connected()
        print 'roach2', to_return

        return to_return

    def send_bof(self):
        send_command = 'scp %s root@%s:/boffiles/%s' % (self.bof_path, self.ip, self.bitstream)
        chmod_command = 'ssh root@%s chmod 777 /boffiles/%s'% ( self.ip, self.bitstream)

        print send_command
        print chmod_command

        os.system(send_command)
        os.system(chmod_command)

    def config_register(self):
        for reg_info in self.register_list:
            self.fpga.write_int(reg_info[0],int(reg_info[1]))

    def accuaire_data(self):

        if not self.is_conected():
            return {}

        return_data = {}
        bram_cont = 0

        for bram in self.brams_info:
            acc_len_ref = bram['acc_len_reg']
            data_type = bram['data_type']
            array_size = bram['size']

            acc_n = self.fpga.read_uint(acc_len_ref)

            print acc_n

            have_real = True
            have_imag = True

            real_data = []
            imag_data = []

            nbram = len(bram['bram_names'])

            for names in bram['bram_names']:
                real_name = names[0]
                imag_name = names[1]

                print '>'+str(array_size) + data_type, real_name,str(int(array_size)*data_type_dictionart[data_type]), 0

                if len(real_name) > 0:
                    real_array = struct.unpack('>'+str(array_size) + data_type, self.fpga.read(real_name,str(int(array_size)*data_type_dictionart[data_type]), 0))
                    real_data.append(real_array)
                else:
                    have_real = have_real and False

                if len(imag_name) > 0:
                    imag_array = struct.unpack('>'+str(array_size) +
                                               data_type, self.fpga.read(imag_name,str(int(array_size)*data_type_dictionart[data_type]), 0))
                    imag_data.append(imag_array)
                else:
                    have_imag = have_imag and False

            final_array = numpy.zeros((int(array_size)*nbram),dtype=complex)

            for cont0 in range(int(array_size)):

                for cont1 in range(nbram):
                    if have_real:
                        real_part = real_data[cont1][cont0]
                    else:
                        real_part = 0

                    if have_imag:
                        imag_part = imag_data[cont1][cont0]
                    else:
                        imag_part = 0

                    final_array[cont0*nbram + cont1] = real_part + 1j*imag_part

            return_data[bram['array_id']] = (final_array, acc_n)

            if bram['plot']:
                aplot = self.plot_brams[bram_cont]
                aplot.plot(numpy.absolute(final_array))
                aplot.title('plot of data array %s, acc count %s'%(self.brams_info[bram_cont]['array_id'],str(acc_n)))
                time.sleep(0.3)

            if bram['store']:
                files =  self.store_drams[bram_cont]
                files[0].wirterow(final_array)



        return return_data



    def program_fpga(self):
        self.fpga.progdev(self.bitstream)

    def stop(self):
        self.fpga.stop()

    def fail(self):
        return self.handler.printMessages()