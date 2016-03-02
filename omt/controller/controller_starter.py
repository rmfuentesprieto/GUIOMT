import threading

from omt.controller.data.data_thread_function import DataThread
from omt.controller.source.source_thread_function import SourceThread


class Coordinator(threading.Thread):

    def __init__(self, source_dictionary, data_dictionary):

        super(Coordinator, self).__init__()
        self.event_source = threading.Event()
        self.event_data = threading.Event()

        self.signal_kill = EndSignal()

        channel_comunicator = CurrentChanel(source_dictionary['frec_number_point'])
        self.thread_source = SourceThread(source_dictionary, self.event_source, self.event_data, channel_comunicator, self.signal_kill)
        self.thread_data = DataThread(data_dictionary, self.event_data, self.event_source, channel_comunicator, self.signal_kill)

        self.event_source.set()
        self.event_data.clear()

        self.end_sweep = False

    def run(self):

        self.end_sweep = False

        self.thread_data.start()
        self.thread_source.start()

        self.thread_data.join()
        self.thread_source.join()

        self.end_sweep = True

    def stop_the_process(self):

        self.signal_kill.stop_all()
        while not self.end_sweep:
            self.event_data.set()



class EndSignal(object):

    def __init__(self):
        self.kill_all = False

    def stop_all(self):
        self.kill_all = True

    def ask_if_stop(self):
        return self.kill_all

class CurrentChanel(object):

    def __init__(self, number_chanels):

        self.n_chan = number_chanels
        self.current_chan = -1

    def next_channel(self):
        self.current_chan += 1

    def get_channel(self):
        return self.current_chan

    def get_number_of_channels(self):
        return self.n_chan
