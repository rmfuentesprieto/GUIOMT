import threading
import time
from kivy.uix.label import Label
from kivy.uix.popup import Popup

from omt.controller.abstract_parallel_proces import Process
from omt.controller.data.fpga import MissingInformation, DummyRoach_FPGA
from omt.gui.extract_data_panel.alternatives.roach import RoachWarningBox

'''
this class is thoiught to handle the data aquasition
comming from the roach board
'''


class DataThread(Process):

    def __init__(self, data_dic):
        try:
            self.roach = data_dic['instance'](data_dic)
        except MissingInformation as exp:
            warning_signal = exp.message
            content = RoachWarningBox(warning_signal + ',\nUse dummy Roach?')
            a_popup = Popup(title='Choose Bof', auto_dismiss=True, content=content, size_hint=(None, None),
                            size=(400, 400))
            content.set_popup(a_popup)
            content.set_popup(a_popup)
            a_popup.open()

            while content.continues:
                pass

            if content.choise:
                self.roach = DummyRoach_FPGA(data_dic)
                return
            raise exp

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