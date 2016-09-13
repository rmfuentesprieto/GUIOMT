import time

from omt.controller.source.beam_scanner.move_xy import MoveXY
from omt.controller.source.beam_scanner.rotate import Rotate
from omt.controller.source.source_thread_function import AbstractSource
from omt.controller.source.source_tone_or_dc import ToneDCSource


class BeamScannerController(AbstractSource):

    def __init__(self, config_dic):
        print 'beam scanner controller', config_dic
        self.ip = '192.168.1.62'
        self.port = 9988

        self.move_xy = MoveXY(self.ip, self.port)
        self.rotate = Rotate(self.ip, self.port)

        self.point = float(config_dic['total_points'])
        self.side_size = float(config_dic['size'])
        angle = float(config_dic['angle_to_measure'])

        angle_speed = float(config_dic['angle_speed'])

        self.rotate.start_connection()
        self.move_xy.start_connection()

        self.rotate.set_hspd(angle_speed)

        self.fast_sweep = config_dic['fast']

        if not self.rotate.move_absolute(angle):
            raise Exception('fail to rotate')

        if not self.move_xy.move_absolute(0.0,0.0):
            raise Exception('fail to position')

        from math import sqrt
        if self.fast_sweep:
            self.side_points = (self.point)/2
        else:
            self.side_points = sqrt(self.point)
        self.total_points = self.point

        self.distance_step = self.side_size/(self.side_points-1)
        print 'side', self.distance_step

        if self.fast_sweep:
            self.move_xy.move_absolute(0,-self.side_size/2)
        else:
            self.move_xy.move_absolute(-self.side_size/2,-self.side_size/2)

        self.rotate.close_connection()

        time.sleep(5)

        self.delta_x = 0
        self.prev_x_delta = self.distance_step
        self.delta_y = 0

    def set_generator_fast_sweep(self, current_channel):
        if current_channel == 0:
            return

        self.delta_x = 0
        self.delta_y = 0
        if current_channel >= self.side_points:
            if current_channel == self.side_points:
                self.move_xy.move_absolute(-self.side_size/2,0)
            self.delta_x = self.distance_step
        else:
            self.delta_y = self.distance_step

        self.move_xy.move_relative(self.delta_x, self.delta_y)

        time.sleep(0.5)

        print 'move to postion: ',int(current_channel/self.side_points), ' , ' ,current_channel%self.side_points

    def set_generator(self, current_channel):

        if self.fast_sweep:
            self.set_generator_fast_sweep(current_channel)
            return

        change_detector = current_channel%self.side_points
        direcction = int(current_channel/self.side_points)

        if current_channel == 0:
            self.delta_x = 0
            self.delta_y = 0
        else:

            if change_detector == 0:
                if direcction%2 == 0:
                    self.prev_x_delta = self.distance_step
                if direcction%2 ==1:
                    self.prev_x_delta = -self.distance_step
                self.delta_y = self.distance_step
                self.delta_x = 0
            else:
                self.delta_y = 0
                self.delta_x = self.prev_x_delta

        self.move_xy.move_relative(self.delta_x, self.delta_y)
        time.sleep(0.5)

        print 'move to postion: ',int(current_channel/self.side_points), ' , ' ,current_channel%self.side_points

    def close_process(self):
        self.move_xy.move_absolute(0.0,0.0)
        self.move_xy.close_connection()

class BeamScannerControllerTone(ToneDCSource):

    def __init__(self, config_dic):
        print 'beam scanner controller', config_dic
        self.ip = '192.168.1.62'
        self.port = 9988

        self.move_xy = MoveXY(self.ip, self.port)
        self.rotate = Rotate(self.ip, self.port)

        self.x = config_dic['x']
        self.y = config_dic['y']
        self.theta = config_dic['theta']

        angle_speed = float(config_dic['angle_speed'])

        self.rotate.start_connection()
        self.move_xy.start_connection()

        self.rotate.set_hspd(angle_speed)

    def turn_on(self):

        if not self.rotate.move_absolute(self.theta):
            raise Exception('fail to rotate')

        if not self.move_xy.move_absolute(self.x, self.y):
            raise Exception('fail to position')

    def stop_source(self):
        self.rotate.close_connection()
        self.move_xy.close_connection()

    def turn_off(self):
        if not self.rotate.move_absolute(0):
            raise Exception('fail to rotate')

        if not self.move_xy.move_absolute(0,0):
            raise Exception('fail to position')





