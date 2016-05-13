import time

from omt.controller.source.beam_scanner.move_xy import MoveXY
from omt.controller.source.beam_scanner.rotate import Rotate
from omt.controller.source.source_thread_function import AbstractSource


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

        if not self.rotate.move_absolute(angle):
            raise Exception('fail to rotate')

        if not self.move_xy.move_absolute(0.0,0.0):
            raise Exception('fail to position')

        from math import sqrt
        self.side_points = sqrt(self.point)
        self.total_points = self.point

        self.distance_step = self.side_size/(self.side_points-1)
        print 'side', self.distance_step

        self.move_xy.move_absolute(-self.side_size/2,-self.side_size/2)

        self.rotate.close_connection()

        self.delta_x = 0
        self.prev_x_delta = self.distance_step
        self.delta_y = 0

    def set_generator(self, current_channel):

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








