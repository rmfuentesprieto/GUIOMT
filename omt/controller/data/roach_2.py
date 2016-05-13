import os
import re
import telnetlib
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup

import corr
import thread
from kivy.uix.spinner import Spinner

import time

from omt.controller.data.fpga import Roach_FPGA


class Roach_II_Controller(Roach_FPGA):
    def send_bof(self):
        # self.connection.write(a_command + '?\r\n')
        # response = self.connection.read_until(b"\n")
        if not self.program:
            return
        connection = telnetlib.Telnet(self.ip, self.port)
        connection.read_until('0', timeout=1)
        connection.write('?listbof\r\n')

        return_lit = connection.expect(['.*!listbof ok .*', ])

        aList = return_lit[2]
        lol = aList.split('\n')

        pattern = r'#listbof (?P<bof_name>.*.bof)'
        regex_c = re.compile(pattern)

        bof_files = []
        for data in lol:
            outP = regex_c.search(data)
            if outP:
                bof_files.append(outP.group('bof_name'))

        for cont in range(len(bof_files)):
            print cont + 1, bof_files[cont]

        # is given the alternative to delete one bof
        # if the fpga is full

        if (len(bof_files) == 17 and not(self.bitstream in bof_files) ):
            content = BofSelector("", bof_files)
            a_popup = Popup(title='Choose Bof', auto_dismiss=False, content=content, size_hint=(None, None), size=(400,400))
            content.set_popup(a_popup)
            a_popup.open()

            while content.continues:
                pass

            chossen = content.choosen_name
            print chossen, '--'
            if len(chossen) > 0:
                connection.write('?delbof %s\r\n' % (chossen))
                print connection.read_until('!delbof ok', timeout=3)

            print 'finish'
        #thread.start_new(self.send_it, (connection,)) #connection
        command = '?uploadbof 3000 %s\r\n'%(self.bitstream)
        connection.write(command)
        time.sleep(1)
        print 'sending bof'
        command = 'nc %s 3000 < %s' %(self.ip, self.bof_path)
        os.system(command)

        connection.close()

    def send_it(self, connection):
        print 'hello'
        command = '?uploadbof 3000 %s\r\n'%(self.bitstream)
        connection.write(command)
        print 'hello'


class BofSelector(BoxLayout):

    def __init__(self, text_, value_):
        super(BofSelector, self).__init__(orientation='vertical', size_hint=(1,1))

        top_padding = BoxLayout(size_hint=(1,1))
        self.bof_spinner = Spinner(text=text_, values=value_, size_hint=(1,None), size=(1,30))
        bottom_padding = BoxLayout(size_hint=(1,1))
        ok_button = Button(text='Ok',  size_hint=(1,0.2))
        ok_button.bind(on_press=self.selection_made)

        self.add_widget(top_padding)
        self.add_widget(self.bof_spinner)
        self.add_widget(bottom_padding)
        self.add_widget(ok_button)

        self.choosen_name = ''
        self.popup = None

        self.continues = True

    def set_popup(self, popup_):
        self.popup = popup_

    def selection_made(self, instance):
        self.choosen_name = self.bof_spinner.text
        self.popup.dismiss()
        self.continues = False