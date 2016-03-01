from omt.controller.source.source_thread_function import SourceThread

data_dic = {}

'''

        self.frec_init = data_dic['frec_init']
        self.frec_end = data_dic['frec_end']
        self.frec_step = data_dic['frec_step']

        self.connection = telnetlib.Telnet(self.ip, self.port)

        self.connection.write('power ' + data_dic['power'] + ' dbm\r\n')

        print self.ask_a_command('power'), data_dic['power']
'''

data_dic['frec_init'] = 100000
data_dic['frec_end']  = 200000
data_dic['frec_step'] =  10000
data_dic['power'] = '-6'
data_dic['ip'] = '192.168.1.33'
data_dic['port'] = '5025'

mytest = SourceThread(data_dic, object(), object())

mytest.parrallel()