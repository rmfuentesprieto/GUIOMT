from unittest import TestCase
import time
from omt.controller.controller_starter import Coordinator
from omt.controller.source.source_thread_function import FailToConnectTelonet


class TestCoordinator(TestCase):

    def test_stop_the_process(self):
        data_dic_s = {}
        data_dic_sw = {}
        data_dic_d = {}

        data_dic_sw['frec_init'] = 10000
        data_dic_sw['frec_end']  = 1000000
        data_dic_sw['frec_number_point'] =  101
        data_dic_sw['power'] = '-6'
        data_dic_sw['ip'] = '192.168.1.34'
        data_dic_sw['port'] = '5023'

        data_dic_s['sweep'] = data_dic_sw

        controller = Coordinator(data_dic_s,data_dic_d)
        self.assertFalse(controller.end_sweep,msg='wrong initialization')
        controller.start()
        time.sleep(1)
        controller.stop_the_process()
        time.sleep(1)
        print controller.end_sweep
        self.assertTrue(controller.end_sweep,msg='fail to stop')

    def test_stop_if_fail_conection(self):
        data_dic_s = {}
        data_dic_sw = {}
        data_dic_d = {}

        data_dic_sw['frec_init'] = 10000
        data_dic_sw['frec_end']  = 1000000
        data_dic_sw['frec_number_point'] =  101
        data_dic_sw['power'] = '-6'
        # fake ip, make sure it doesn't connecto to something
        data_dic_sw['ip'] = '192.168.0.11'
        data_dic_sw['port'] = '5023'

        data_dic_s['sweep'] = data_dic_sw

        self.assertRaises(FailToConnectTelonet, lambda :Coordinator(data_dic_s,data_dic_d))
