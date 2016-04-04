import telnetlib
import time
from kivy.uix.label import Label
from kivy.uix.popup import Popup

from omt.controller.abstract_parallel_proces import Process
from omt.controller.data.roach_2 import Roach2

'''
this class is thoiught to handle the data aquasition
comming from the roach board
'''


class DataThread(Process):

    def __init__(self, data_dic):
        self.roach = Roach2(data_dic)

    def start_connections(self):
        try:
            self.roach.connect_to_roach()
            if not self.roach.is_conected():
                raise Exception('Connection Fail')

            self.roach.send_bof()
            time.sleep(1)
            self.roach.program_fpga()
            time.sleep(0.1)
            self.roach.config_register()
            time.sleep(0.1)
        except Exception as e:
            raise RoachException(e.message)

    def accuaire_data(self):
        return self.roach.accuaire_data()

    def close_process(self):
        self.roach.stop()

class RoachException(Exception):

    def __init__(self, message):
        super(RoachException, self).__init__(message)