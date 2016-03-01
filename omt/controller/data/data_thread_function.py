import telnetlib

from omt.controller.abstract_parallel_proces import Process

'''
this class is thoiught to handle the data aquasition
comming from the roach board
'''

class DataThread(Process):

    def __init__(self, data_dic, ini_monitor, end_monitor):
        super(DataThread, self).__init__(ini_monitor,end_monitor)

        self.ip = data_dic['ip']
        self.port = data_dic['port']

        self.fpga_data = data_dic['fpga_obj']

        print self.ask_a_command('power'), data_dic['power']


    def ask_a_command(self, a_command):
        self.connection.write(a_command + '?')
        return self.connection.read_until(b"\n")

    def parrallel(self):

        current_frec = self.frec_init
        while(True):

            self.initialize_monitor.wait()
            self.connection.write('freq ' + str(current_frec))
            self.initialize_monitor.clear()
            self.end_monitor.set()

            current_frec += self.frec_step

            if current_frec > self.frec_end:
                self.end_process()
                break

    def end_process(self):
        pass