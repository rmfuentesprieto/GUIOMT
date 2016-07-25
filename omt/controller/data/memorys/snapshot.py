import numpy

from omt.controller.data.memorys.memory import Memory


class SnapShot(Memory):

    def __init__(self, name):
        self.name = name
        self.data = []


    def does_write(self):
        return False

    def interact_roach(self, fpga):
        self.data = numpy.fromstring(fpga.snapshot_get(self.name, man_trig=True, man_valid=True)['data'], dtype='>i1')

    def get_value_name(self):
        return self.name

    def get_value(self):
        return self.data