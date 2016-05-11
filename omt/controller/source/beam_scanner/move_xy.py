from omt.controller.source.beam_scanner.beam_connection import BeamConnection


class MoveXY(BeamConnection):

    def __init__(self, ip, port):

        super(MoveXY, self).__init__(ip, port)

    def start_connection(self):
        super(MoveXY, self).start_connection('move x,y')

    def move_absolute(self, x_dest, y_dest):
        self.send_command('move_absolute %s %s' %(str(x_dest),str(y_dest)) )
        txt_return = self.recieve_data()
        return txt_return == 'ok'

    def move_relative(self, x_delta, y_delta):
        self.send_command('move_relative %s %s' %(str(x_delta),str(y_delta)) )
        txt_return = self.recieve_data()
        return txt_return == 'ok'

    def ask_position(self):
        self.send_command('ask_position' )
        txt_return = self.recieve_data()
        return txt_return

    def set_origin(self):
        self.send_command('set_origin' )
        txt_return = self.recieve_data()
        return txt_return == 'ok'
