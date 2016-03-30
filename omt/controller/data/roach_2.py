import struct
import corr
import logging
import time

import numpy

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

        self.fpga = None

        self.handler = corr.log_handlers.DebugLogHandler()
        self.logger = logging.getLogger(self.ip)
        self.logger.addHandler(self.handler)
        self.logger.setLevel(10)

        self.send_bof()

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
        pass

    def config_register(self):
        for reg_info in self.register_list:
            self.fpga.write_int(reg_info[0],int(reg_info[1]))

    def aquare_data(self):

        if not self.is_conected():
            return {}

        return_data = {}
        cont_key = 0

        print 'in'

        for bram in self.brams_info:
            print 'la'
            acc_len_ref = bram['acc_len_reg']
            data_type = bram['data_type']
            array_size = bram['size']

            acc_n = self.fpga.read_uint(acc_len_ref)

            have_real = True
            have_imag = True

            real_data = []
            imag_data = []

            nbram = len(bram['bram_names'])

            for names in bram['bram_names']:
                real_name = names[0]
                imag_name = names[1]

                if len(real_name) > 0:
                    real_array = struct.unpack('>'+str(array_size) +
                                               data_type, self.fpga.read(real_name,str(int(array_size)*data_type_dictionart[data_type]), 0))
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

            return_data[str(cont_key)] = (final_array, acc_n)

        return return_data



    def program_fpga(self):
        self.fpga.progdev(self.bitstream)

    def stop(self):
        self.fpga.stop()

    def fail(self):
        return self.handler.printMessages()