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
souce_dic = {}
data_dic_s = {}
data_dic_d = {}
data_dic_s['frec_init'] = 10000
data_dic_s['frec_end']  = 1000000
data_dic_s['frec_number_point'] =  101
data_dic_s['power'] = '-6'
data_dic_s['ip'] = '192.168.1.34'
data_dic_s['port'] = '5023'

data_dic_tone = {}
data_dic_tone['ip'] = '192.168.1.34'
data_dic_tone['port'] = '5023'
data_dic_tone['frec'] = 123100
data_dic_tone['power'] = '-6'

#souce_dic['sweep'] = data_dic_s
souce_dic['tone'] = [data_dic_tone,]
controller = Coordinator(souce_dic,data_dic_d)
controller.start()
raw_input('hit me: ')
controller.stop_the_process()
