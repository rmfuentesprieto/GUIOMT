import telnetlib
import time

from omt.controller.abstract_parallel_proces import Process

'''
this class is thoiught to handle the data aquasition
comming from the roach board
'''

class DataThread(Process):

    def __init__(self, data_dic, ini_monitor, end_monitor, channel_obj, end_signal):
        super(DataThread, self).__init__(ini_monitor,end_monitor)

        self.ask_channel = channel_obj
        self.kill_me = end_signal

        #self.ip = data_dic['ip']
        #self.port = data_dic['port']

        #self.fpga_data = data_dic['fpga_obj']

    def run(self):

        current_channel = 0
        while(True):

            # waits for the source to emit the rigth signal
            self.initialize_monitor.wait()

            if self.kill_me.ask_if_stop():
                break

            time.sleep(0.5)

            if self.ask_channel.get_number_of_channels() == current_channel:
                break
            current_channel += 1

            #looks the initializer monitor and awaits
            #for the source thread to clear it
            self.initialize_monitor.clear()
            # ask for the following sinal
            self.end_monitor.set()

        self.end_monitor.set()

    def end_process(self):
        pass