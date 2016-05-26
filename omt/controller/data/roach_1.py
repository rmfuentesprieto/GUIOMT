import os
from kivy.uix.label import Label
from kivy.uix.popup import Popup

from omt.controller.data.fpga import Roach_FPGA


class Roach_I_Controller(Roach_FPGA):

    def send_bof(self):
        if not self.program:
            return

        send_bof_label = Label(text='Sending bof,\nplease be patient.')
        popup = Popup(title='ROACH Busnise', content=send_bof_label, size_hint=(None,None), size=(1,30))
        popup.open()

        send_command = 'scp %s root@%s:/boffiles/%s' % (self.bof_path, self.ip, self.bitstream)
        chmod_command = 'ssh root@%s chmod 777 /boffiles/%s'% ( self.ip, self.bitstream)

        os.system(send_command)
        os.system(chmod_command)

        popup.dismiss()