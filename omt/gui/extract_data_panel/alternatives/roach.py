from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput

from omt.gui.empty import Empty


class ROACH(Empty):

    def __init__(self, **kwargs):

        super(ROACH, self).__init__(kwargs=kwargs)

        big_one = BoxLayout(orientation='vertical')

        # reg layout
        roach_connection_info = BoxLayout(orientation='horizontal',  size_hint=(1,None), size=(1,30))
        roach_register = BoxLayout(orientation='vertical', size_hint=(1,None), size=(1,40))

        ip_label = Label(text='IP :')
        port_label = Label(text='Port :')

        self.ip = TextInput(multiline=False)
        self.port = TextInput(multiline=False, Text='7417')

        roach_connection_info.add_widget(ip_label)
        roach_connection_info.add_widget(self.ip)
        roach_connection_info.add_widget(port_label)
        roach_connection_info.add_widget(self.port)

        new_reg = Button(text='nuevo registro')
        new_reg.bind(on_press=self.add_registers)



        roach_register.add_widget(new_reg)

        self.reg_container = GridLayout(cols=1, spacing = 1, size_hint_y = None)
        self.reg_container.bind(minimum_height=self.reg_container.setter('height'))

        scroll_root = ScrollView(size_hint=(1,None), size=(400,100))
        scroll_root.add_widget(self.reg_container)

        # acc layout
        free_running = BoxLayout(orientation='horizontal', size_hint=(1,None), size=(1,30))
        add_free_running = Button(text = 'Adquirir Nuevo')
        add_free_running.bind(on_press=self.add_free_running)

        free_running.add_widget(add_free_running)

        self.free_run_container = GridLayout(cols=1, spacing = 1, size_hint_y = None)
        self.free_run_container.bind(minimum_height=self.reg_container.setter('height'))

        scroll_root_free_run = ScrollView(size_hint=(1,None), size=(400,100))
        scroll_root_free_run.add_widget(self.free_run_container)

        big_one.add_widget(roach_connection_info)
        big_one.add_widget(roach_register)
        big_one.add_widget(scroll_root)
        big_one.add_widget(free_running)
        big_one.add_widget(scroll_root_free_run)

        self.add_widget(big_one)

        self.register_list = []

    def add_registers(self, instance):
        btn = Button(text=str(2), size_hint_y=None, height=30)
        self.reg_container.add_widget(btn)

    def add_free_running(self, instance):
        btn = Button(text=str(2), size_hint_y=None, height=30)
        self.free_run_container.add_widget(btn)

