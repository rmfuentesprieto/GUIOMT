from omt.controller.controller_starter import Coordinator
from omt.controller.source.source_thread_function import SourceThread


import threading
import time


data_dic_s = {}
data_dic_d = {}

'''

        self.frec_init = data_dic['frec_init']
        self.frec_end = data_dic['frec_end']
        self.frec_step = data_dic['frec_step']

        self.connection = telnetlib.Telnet(self.ip, self.port)

        self.connection.write('power ' + data_dic['power'] + ' dbm\r\n')

        print self.ask_a_command('power'), data_dic['power']
'''

data_dic_s['frec_init'] = 10000
data_dic_s['frec_end']  = 1000000
data_dic_s['frec_number_point'] =  11
data_dic_s['power'] = '-6'
data_dic_s['ip'] = '192.168.1.34'
data_dic_s['port'] = '5024'

controller = Coordinator(data_dic_s,data_dic_d)
controller.start()