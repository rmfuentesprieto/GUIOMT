import telnetlib
import time

from omt.controller.abstract_parallel_proces import Process


class DummySourceThread(Process):

    def __init__(self, data_dic, ini_monitor, end_monitor, channel_obj):
        super(DummySourceThread, self).__init__(ini_monitor,end_monitor)

        self.channel_obj = channel_obj

    def ask_a_command(self, a_command):
        self.connection.write(a_command + '?\r\n')
        response = self.connection.read_until(b"\n")
        return response

    def run(self):

        for current_channel in range(self.frec_number_of_points+1):

            self.initialize_monitor.wait()
            self.channel_obj.next_channel()
            self.initialize_monitor.clear()
            self.end_monitor.set()

        self.initialize_monitor.wait()

    def close_process(self):
        print 'stop'