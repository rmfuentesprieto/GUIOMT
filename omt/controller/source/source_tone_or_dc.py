import socket
import telnetlib
import time

import visa

from omt.controller.source.source_thread_function import FailToConnectTelnet


class ToneDCSource(object):

    def __init__(self, config_dic):

        self.ip = config_dic['ip']
        self.port = config_dic['port']
        self.frec = config_dic['frec']
        self.power = config_dic['power']

        try:
            self.connection = telnetlib.Telnet(self.ip, self.port)# for test purpuses timeout=3)
        except socket.error, exc:
            raise FailToConnectTelnet(self.ip, self.port)

        self.connection.write('power %s dbm\r\n'% self.power)
        self.connection.write('freq %s\r\n'% str(self.frec))

    def turn_on(self):
        self.connection.write('outp on\r\n')


    def turn_off(self):
        print 'tone off'
        self.connection.write('outp off\r\n')
        time.sleep(0.1)

    def stop_source(self):
        self.connection.close()


class AnritsuTone(ToneDCSource):
    def __init__(self, dictionary):
        self.addrs = dictionary['ip_direction']
        self.power = dictionary['power']
        self.freq = dictionary['frequency']

        rm = visa.ResourceManager('/usr/local/vxipnp/linux/lib64/libvisa.so');self.device = rm.get_instrument(self.addrs)
        self.device = rm.get_instrument(self.addrs)
        self.device.write('freq {} hz'.format(self.freq))
        self.device.write('power {} dbm'.format(self.power))


    def turn_on(self):
        self.device.write('outp on')

    def turn_off(self):
        try:
            self.device.write('outp off')
            time.sleep(0.1)
        except Exception:
            rm = visa.ResourceManager('/usr/local/vxipnp/linux/lib64/libvisa.so');self.device = rm.get_instrument(self.addrs)
            self.device = rm.get_instrument(self.addrs)
            self.device.write('outp off')

    def stop_source(self):
        self.device.close()


