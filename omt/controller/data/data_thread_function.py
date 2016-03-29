import telnetlib
import time

from omt.controller.abstract_parallel_proces import Process
from omt.controller.data.roach_2 import Roach2

'''
this class is thoiught to handle the data aquasition
comming from the roach board
'''


class DataThread(Process):

    def __init__(self, data_dic, ini_monitor, end_monitor, channel_obj, end_signal):
        super(DataThread, self).__init__(ini_monitor,end_monitor)

        self.ask_channel = channel_obj
        self.kill_me = end_signal

        self.roach = Roach2(data_dic)


    def run(self):
        current_channel = 0

        self.roach.connect_to_roach()
        self.roach.config_register()

        if not self.roach.is_conected():
            raise Exception('Not connected')
        while(True):

            # waits for the source to emit the rigth signal
            self.initialize_monitor.wait()

            if self.kill_me.ask_if_stop():
                break

            time.sleep(2)

            print 'addquiere ' + self.roach.aquare_data()
            #raw_input()
            if self.ask_channel.get_number_of_channels() == (current_channel+1):
                break
            current_channel += 1

            #looks the initializer monitor and awaits
            #for the source thread to clear it
            self.initialize_monitor.clear()
            # ask for the following sinal
            self.end_monitor.set()
        self.kill_me.stop_all()
        print 'sleep'
        self.end_monitor.set()

    def close_process(self):
        pass