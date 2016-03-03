import threading

from omt.controller.data.data_thread_function import DataThread
from omt.controller.source.source_thread_function import SourceThread, DummySourceThread
from omt.controller.source.source_tone_or_dc import ToneDCSource


class Coordinator(threading.Thread):

    def __init__(self, source_dictionary, data_dictionary):

        super(Coordinator, self).__init__()
        self.event_source = threading.Event()
        self.event_data = threading.Event()

        self.signal_kill = EndSignal()

        # extract the settings for the source thats going to sweep

        sweep_source_dic = {}
        if 'sweep' in source_dictionary:
            sweep_source_dic = source_dictionary['sweep']
            channel_comunicator = CurrentChanel(sweep_source_dic['frec_number_point'])
            self.thread_source = SourceThread(sweep_source_dic, self.event_source, self.event_data, channel_comunicator, self.signal_kill)
        else:
            channel_comunicator = CurrentChanel(-1)
            self.thread_source = DummySourceThread(data_dictionary, self.event_data, self.event_source, channel_comunicator, self.signal_kill)

        self.tone_source = []
        if 'tone' in source_dictionary:
            for source_config in source_dictionary['tone']:
                self.tone_source.append(ToneDCSource(source_config))

        self.thread_data = DataThread(data_dictionary, self.event_data, self.event_source, channel_comunicator, self.signal_kill)

        self.event_source.set()
        self.event_data.clear()

        self.end_sweep = False

    def run(self):

        self.end_sweep = False

        for source in self.tone_source:
            source.turn_on()

        self.thread_data.start()
        self.thread_source.start()

        self.thread_data.join()
        self.thread_source.join()

        self.thread_data.close_process()
        self.thread_source.close_process()

        for source in self.tone_source:
            source.turn_off()
            source.stop_source()

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
