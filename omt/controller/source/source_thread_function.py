import telnetlib
import time

from omt.controller.abstract_parallel_proces import Process


class SourceThread(Process):

    def __init__(self, data_dic, ini_monitor, end_monitor):
        super(SourceThread, self).__init__(ini_monitor,end_monitor)

        self.ip = data_dic['ip']
        self.port = data_dic['port']

        self.frec_init = data_dic['frec_init']
        self.frec_end = data_dic['frec_end']
        self.frec_step = data_dic['frec_step']

        self.connection = telnetlib.Telnet(self.ip, self.port)

        self.connection.write('power ' + data_dic['power'] + ' dbm\r\n')

        print self.ask_a_command('power'), data_dic['power']


    def ask_a_command(self, a_command):
        self.connection.write(a_command + '?\r\n')
        response = self.connection.read_until(b"\n")
        return response

    def parrallel(self):

        current_frec = self.frec_init

        self.connection.write('outp on\r\n')

        while(True):

            #self.initialize_monitor.wait()
            self.connection.write('freq ' + str(current_frec) + '\r\n')
            time.sleep(1)
            #self.initialize_monitor.clear()
            #self.end_monitor.set()

            current_frec += self.frec_step

            if current_frec > self.frec_end:
                self.end_process()
                break

        self.connection.write('outp off\r\n')

    def end_process(self):
        print 'stop'