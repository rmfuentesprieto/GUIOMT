import telnetlib
import time

from omt.controller.abstract_parallel_proces import Process


class SourceThread(Process):

    def __init__(self, data_dic, ini_monitor, end_monitor, channel_obj, end_signal):
        super(SourceThread, self).__init__(ini_monitor,end_monitor)

        self.channel_obj = channel_obj
        self.kill_me = end_signal

        self.ip = data_dic['ip']
        self.port = data_dic['port']

        self.frec_init = data_dic['frec_init']
        self.frec_end = data_dic['frec_end']
        self.frec_number_of_points = data_dic['frec_number_point']
        self.frec_step = (self.frec_end - self.frec_init)/(self.frec_number_of_points - 1.0)

        self.connection = telnetlib.Telnet(self.ip, self.port)

        self.connection.write('power ' + data_dic['power'] + ' dbm\r\n')

    def ask_a_command(self, a_command):
        self.connection.write(a_command + '?\r\n')
        response = self.connection.read_until(b"\n")
        return response

    def run(self):

        self.connection.write('outp on\r\n')

        for current_channel in range(self.frec_number_of_points+1):

            self.initialize_monitor.wait()
            if self.kill_me.ask_if_stop():
                return

            self.channel_obj.next_channel()
            self.connection.write('freq ' + str(current_channel * self.frec_step + self.frec_init) + '\r\n')
            self.initialize_monitor.clear()
            self.end_monitor.set()

        self.initialize_monitor.wait()
        self.connection.write('outp off\r\n')

    def close_process(self):
        self.connection.close()