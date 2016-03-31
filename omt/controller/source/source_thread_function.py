import telnetlib
import time
import socket

from omt.controller.abstract_parallel_proces import Process


class AbstractSource(Process):

    def __init__(self,ini_monitor,end_monitor):
        super(AbstractSource, self).__init__(ini_monitor,end_monitor)

    def is_dummy(self):
        return False

class SourceThread(AbstractSource):

    def __init__(self, config_dic, ini_monitor, end_monitor, channel_obj, end_signal):
        super(SourceThread, self).__init__(ini_monitor,end_monitor)

        self.channel_obj = channel_obj
        self.kill_me = end_signal

        self.ip = config_dic['ip']
        self.port = config_dic['port']

        # set the sweep configutation
        # the configuration comes from the GUI
        # and is pass in the Coordinator class
        self.frec_init = config_dic['frec_init']
        self.frec_end = config_dic['frec_end']
        self.frec_number_of_points = config_dic['frec_number_point']
        self.frec_step = (self.frec_end - self.frec_init)/(self.frec_number_of_points - 1.0)

        try:
            #self.connection = telnetlib.Telnet(self.ip, self.port,timeout=3) # for test purpuses, time in secconds
            self.connection = telnetlib.Telnet(self.ip, self.port)
        except socket.error, exc:
            raise FailToConnectTelnet(self.ip, self.port)
        self.connection.write('power ' + config_dic['power'] + ' dbm\r\n')

    def ask_a_command(self, a_command):
        self.connection.write(a_command + '?\r\n')
        response = self.connection.read_until(b"\n")
        return response

    def run(self):
        self.connection.write('outp on\r\n')

        #for current_channel in range(self.frec_number_of_points):
        current_channel = 0

        while True:

            self.initialize_monitor.wait()
            if self.kill_me.ask_if_stop():
                break


            self.channel_obj.next_channel()
            self.connection.write('freq ' + str(current_channel * self.frec_step + self.frec_init) + '\r\n')
            print 'addquiere ' + str(current_channel)
            # wait for the tone to adjust well
            time.sleep(2)
            self.initialize_monitor.clear()
            self.end_monitor.set()
            current_channel += 1
        self.initialize_monitor.wait()
        self.connection.write('outp off\r\n')
        print 'sleep source'

    def close_process(self):
        self.connection.close()

class DummySourceThread(Process):

    def __init__(self, data_dic, ini_monitor, end_monitor, channel_obj,  end_signal):
        super(DummySourceThread, self).__init__(ini_monitor,end_monitor)

        self.kill_me = end_signal
        self.channel_obj = channel_obj

    def run(self):

        while True:
            self.initialize_monitor.wait()
            if self.kill_me.ask_if_stop():
                return

            self.channel_obj.next_channel()
            self.initialize_monitor.clear()
            self.end_monitor.set()

        self.initialize_monitor.wait()

    def close_process(self):
        print 'dummy stop'

class FailToConnectTelnet(Exception):

    def __init__(self, ip, port):
        self.value = 'fail to conect to %s:%s'% (ip, port)