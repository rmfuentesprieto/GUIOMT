import csv
import struct
import corr
import logging
import time

import datetime
import numpy
from Gnuplot import Gnuplot

fpga = corr.katcp_wrapper.FpgaClient('192.168.1.12', 7147, timeout=10)

from omt.util.data_type import data_type_dictionart

def get_data_roach( array_size, data_type, name):
    if len(name) > 0:
        return lambda : fpga.read(name, str(int(array_size)*data_type_dictionart[data_type]), 0)
    else:
        return [0] * int(array_size)

def create_scope( f_new, f_old):
    if f_new == None:
        return f_old
    return lambda : (f_old() + (f_new(),))

fpga = corr.katcp_wrapper.FpgaClient('192.168.1.12', 7147, timeout=10)
time.sleep(1)

array_size = '512'
data_type = 'q'

name = 'dout0_0'

start = time.time()
data = fpga.read(name, str(int(array_size)*data_type_dictionart[data_type]), 0)
data = fpga.read(name, str(int(array_size)*data_type_dictionart[data_type]), 0)
data = fpga.read(name, str(int(array_size)*data_type_dictionart[data_type]), 0)
data = fpga.read(name, str(int(array_size)*data_type_dictionart[data_type]), 0)
end = time.time()

print 'alone', end - start

names = ['dout0_0','dout0_2','dout0_4','dout0_6']

final = lambda : ()
for name in names:
    f = get_data_roach(array_size, data_type, name)
    final = create_scope(f,final)

start = time.time()
final()
end = time.time()

print 'full ', end - start


start = time.time()
a = fpga.read('dout0_0', str(int(array_size)*data_type_dictionart[data_type]), 0)
a = fpga.read('dout0_2', str(int(array_size)*data_type_dictionart[data_type]), 0)
a = fpga.read('dout0_4', str(int(array_size)*data_type_dictionart[data_type]), 0)
a = fpga.read('dout0_6', str(int(array_size)*data_type_dictionart[data_type]), 0)
end = time.time()

print 'for  ', end - start