import socket
import threading
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.progressbar import ProgressBar

from omt.controller.data.data_thread_function import DataThread, RoachException
from omt.controller.data.fpga import MissingInformation
from omt.controller.procesing.procesing_thread_function import ProccesThread
from omt.controller.source.source_thread_function import FailToConnectTelnet, DummySourceThread
from omt.controller.source.source_tone_or_dc import ToneDCSource


class SuperCoordinator(threading.Thread):

    def __init__(self, list_dict):
        super(SuperCoordinator, self).__init__()

        self.all_configurations = list_dict

        self.save_data = {}

        self.end_sweep = False

    def run(self):

        for configuration in self.all_configurations:

            if self.end_sweep:
                print 'force stop, super controller'
                return

            sweep_source_dic = {}

            source_dictionary = configuration[0]
            data_dictionary = configuration[1]
            fucntion_dictionary = configuration[2]

            if 'sweep' in source_dictionary:
                sweep_source_dic = source_dictionary['sweep']
                self.frec_number_point = sweep_source_dic['frec_number_point']
                try:
                    self.thread_source = sweep_source_dic['instance'](sweep_source_dic)
                except FailToConnectTelnet as e:
                    error_label = Label(text = e.message)
                    Popup(title='Source error', content=error_label, size_hint=(None, None), size=(300,300)).open()
                    return
                except socket.error as e:
                    error_label = Label(text = 'fail to connect,\ncheck connection.')
                    Popup(title='Server error', content=error_label, size_hint=(None, None), size=(300,300)).open()
                    return
            else:
                self.frec_number_point = -1
                self.thread_source = DummySourceThread()

            self.tone_source = []
            if 'tone' in source_dictionary:
                for source_config in source_dictionary['tone']:
                    self.tone_source.append(source_config['instance'](source_config))
            try:
                self.thread_data = DataThread(data_dictionary['roach'])
            except MissingInformation as e:
                print 'finish for all this %s' %(e.message)
                return

            self.thread_procesing = ProccesThread(fucntion_dictionary)

            self.end_sweep = False

            for source in self.tone_source:
                source.turn_on()

            progress_bar = ProgressBar(max=self.frec_number_point, value = 0)
            progress_bar_popup = Popup(content=progress_bar, size_hint = (None, None), size = (300,300), title='Sweep state of progress')

            progress_bar_popup.open()

            try:
                current_channel = 0

                self.thread_data.start_connections()

                while not self.end_sweep:
                    self.thread_source.set_generator(current_channel)
                    extract_dictionary = self.thread_data.accuaire_data()
                    extract_dictionary['current_channel'] = current_channel
                    self.thread_procesing.run_execute_functions(extract_dictionary)

                    if self.frec_number_point - 1 == (current_channel):
                        break
                    current_channel += 1

                    progress_bar.value = current_channel

            except RoachException as roach_e:

                Popup(title='Error Roach', content=Label(text=roach_e.message),\
                              size_hint=(None, None), size=(300, 120)).open()

            except Exception as e:
                Popup(title='Error', content=Label(text=e.message),\
                              size_hint=(None, None), size=(400, 120)).open()



            print "stop it all lol"

            self.thread_data.close_process()
            self.thread_source.close_process()

            for source in self.tone_source:
                source.turn_off()
                source.stop_source()

            progress_bar_popup.dismiss()

        self.end_sweep = True

    def stop_the_process(self):
        print 'kill signal'
        self.end_sweep = True