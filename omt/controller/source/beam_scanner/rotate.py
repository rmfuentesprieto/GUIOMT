from omt.controller.source.beam_scanner.beam_connection import BeamConnection


class Rotate(BeamConnection):

    def __init__(self, ip, port):

        super(Rotate, self).__init__(ip, port)

    def start_connection(self):
        super(Rotate, self).start_connection('move ang')

    def move_absolute(self, ang_dest):
        ''' move the rotator stepper motor to this position
            given the absolute origin.
            @ang_dest angle to move to in degrees'''
        self.send_command('move_absolute %s' %(str(ang_dest)) )
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

    def set_acc(self, acc_):
        self.send_command('set_acc %s' %(str(acc_)))
        txt_return = self.recieve_data()
        return txt_return == 'ok'

    def set_hca(self, hca_):
        self.send_command('set_hca %s' %(str(hca_)))
        txt_return = self.recieve_data()
        return txt_return == 'ok'

    def set_hspd(self, hspd_):
        self.send_command('set_hspd %s' %(str(hspd_)))
        txt_return = self.recieve_data()
        return txt_return == 'ok'

    def set_lspd(self, lspd_):
        self.send_command('set_lspd %s' %(str(lspd_)))
        txt_return = self.recieve_data()
        return txt_return == 'ok'
