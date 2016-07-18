import csv
import corr
import logging
import time

import datetime
from Gnuplot import Gnuplot

from omt.controller.data.memorys.bram import BRam
from omt.controller.data.memorys.register import RegisterWrite, RegisterRead
from omt.controller.data.memorys.snapshot import SnapShot


class Roach_FPGA(object):

    def __init__(self, data_dic):

        print data_dic
        try:
            self.port = int(data_dic['port'])
        except:
            raise MissingInformation('port')
        try:
            self.ip = data_dic['ip']
        except:
            raise MissingInformation('ip')
        self.register_list = data_dic['reg']
        self.bof_path = data_dic['bof_path']
        self.bitstream = str(data_dic['name'] + '.bof')
        self.brams_info = data_dic['bram']
        self.program = data_dic['progdev']

        self.plot_brams = []
        self.store_drams = []

        for cont in range(len(self.brams_info)):
            self.brams_info[cont]['prev_acc'] = 0

        for cont in range(len(self.brams_info)):
            aplot = lambda x : x
            if self.brams_info[cont]['plot']:
                aplot = Gnuplot(debug=1)
                aplot.clear()
                aplot('set style data linespoints')
                aplot.ylabel('Power AU (dB)')
                aplot('set xrange [-50:2098]')
                aplot('set yrange [0:100]')
                aplot('set ytics 10')
                aplot('set xtics 256')
                aplot('set grid y')
                aplot('set grid x')

            self.brams_info[cont]['plot_'] = aplot

            class a:
                def close (self):
                    pass
                def writerow (self,x):
                    pass

            astore = (a(),a())

            if self.brams_info[cont]['store']:
                ts = time.time()
                time_stamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
                print self.brams_info[cont].keys()
                file_name = self.bof_path[:-len('.bof')] + '-' + self.brams_info[cont]['array_id'] + '-' + time_stamp + '.csv'
                file = open(file_name, 'w')

                csv_writer = csv.writer(file, delimiter = ',')
                astore = (csv_writer,file)
            self.brams_info[cont]['store_'] = astore

        self.fpga = None
        self.last_acc_count = {}

        self.handler = corr.log_handlers.DebugLogHandler()
        self.logger = logging.getLogger(self.ip)
        self.logger.addHandler(self.handler)
        self.logger.setLevel(10)

    def connect_to_roach(self):
        self.fpga = corr.katcp_wrapper.FpgaClient(self.ip, self.port, timeout=10, logger=self.logger)
        time.sleep(1)

    def is_conected(self):
        to_return = self.fpga.is_connected()
        return to_return

    def send_bof(self):
        if not self.program:
            return

    def config_register(self):
        for reg_info in self.register_list:
            self.fpga.write_int(reg_info[0],int(reg_info[1]))

    def write_reg_roach(self, name, value):
        return lambda : self.fpga.write_int(name, value)

    def read_reg_roach(self, name):
        self.fpga.read_int(name)

    def accuaire_data(self):

        if not self.is_conected():
            return {}

        reg_snap_bram_things = [['',[]],]

        # order the data
        for bram in self.brams_info:

            if bram['is_bram']:
                last_reg = reg_snap_bram_things[-1][0]
                bRam = BRam(bram['array_id'], bram['bram_names'], bram['data_type'], bram['size'], bram['plot'],
                             bram['plot_'], bram['store'], bram['store_'], bram['acc_len_reg'],self.fpga)

                if not bram['acc_len_reg'] in self.last_acc_count:
                    self.last_acc_count[bram['acc_len_reg']] = -1

                if bram['acc_len_reg'] == last_reg:
                    reg_snap_bram_things[-1][1].append(bRam)
                else:
                    reg_snap_bram_things.append([ bram['acc_len_reg'],[bRam,]])

            else:
                if 'snap' in bram:
                    reg_snap_bram_things[-1][1].append(SnapShot(bram['name']))
                else:
                    if bram['load_data']:
                        reg_snap_bram_things[-1][1].append(RegisterWrite(bram['reg_name'],int(bram['reg_value'])))
                    else:
                        reg_snap_bram_things[-1][1].append(RegisterRead(bram['reg_name']))

        # extract data
        while 1:
            break_out = True
            for data in reg_snap_bram_things:
                count = 0
                # ensures that all the read data is from the same acumulation
                acc_error = 0
                while 1:
                    if data[0]:
                        count = self.fpga.read_int(data[0])
                    for mem in data[1]:
                        mem.set_acc_count(count)
                        mem.interact_roach(self.fpga)

                    # this condition ratifies that all data are from the same acumulation
                    # and a different acumulation as the last one
                    if not data[0] or (count == self.fpga.read_int(data[0]) ):#and
                        if not data[0] or count > self.last_acc_count[data[0]]:
                            break_out = break_out and True
                            self.last_acc_count[data[0]] = count
                        else:
                            break_out = break_out and False
                    #    self.last_acc_count[data[0]] = count
                        break
                    else:
                        acc_error += 1
                        if acc_error > 5:
                            raise Exception('Increase accumulation length')
            if break_out:
                break

        # preper the return dictionary
        return_data = {}
        for data in reg_snap_bram_things:
            for mem in data[1]:
                key = mem.get_value_name()
                return_data[key] = mem.get_value()

        return_data['fpga'] = self.fpga

        return return_data

    def program_fpga(self):
        if self.program:
            self.fpga.progdev(self.bitstream)

    def stop(self):
        self.fpga.stop()

        bram_cont = 0

        for bram in self.brams_info:
            if bram['is_bram']:
                if bram['plot']:
                    bram['plot_'].close()

                if bram['store']:
                    files = bram['store_']
                    files[1].close()
            bram_cont += 1


    def fail(self):
        return self.handler.printMessages()

    def get_fpga_instance(self):
        pass


class DummyRoach_FPGA(Roach_FPGA):

    def __init__(self, data_dic):
        self.brams_info = data_dic['bram']

    def connect_to_roach(self):
        pass

    def is_conected(self):
        return True

    def send_bof(self):
        pass

    def config_register(self):
        pass

    def accuaire_data(self):

        if not self.is_conected():
            return {}

        return_data = {}

        for bram in self.brams_info:
            if bram['is_bram']:
                return_data[bram['array_id']] = ((-1 + 1j,-1 + 2j,-1 + 3j, 1 + 4j, 1 + 5j), -1)
            else:
                if bram['load_data']:
                    pass
                else:
                    return_data[bram['reg_name']] = 0

        return return_data


    def program_fpga(self):
        pass

    def stop(self):
        pass


class MissingInformation(Exception):

    def __init__(self, text):
        self.message = 'missing ROACH: %s'% (text)