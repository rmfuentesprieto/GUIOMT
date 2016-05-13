import os

from omt.controller.data.fpga import Roach_FPGA


class Roach_I_Controller(Roach_FPGA):

    def send_bof(self):
        if not self.program:
            return
        send_command = 'scp %s root@%s:/boffiles/%s' % (self.bof_path, self.ip, self.bitstream)
        chmod_command = 'ssh root@%s chmod 777 /boffiles/%s'% ( self.ip, self.bitstream)

        os.system(send_command)
        print send_command
        os.system(chmod_command)
        print chmod_command