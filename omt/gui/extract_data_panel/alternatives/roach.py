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
        ##### Regiter container
        self.reg_container = GridLayout(cols=1, spacing = 1, size_hint_y=None)#row_default_height=30)
        self.reg_container.bind(minimum_height=self.reg_container.setter('height'))

        scroll_root = ScrollView(size_hint=(None,None), height=100)
        scroll_root.add_widget(self.reg_container)
        ####

        free_running = BoxLayout(orientation='horizontal', size_hint=(1,None), size=(1,30))
        add_free_running = Button(text = 'Adquirir Nuevo')
        add_free_running.bind(on_press=self.add_free_running)
        free_running.add_widget(add_free_running)

        #### free run container
        self.free_run_container = GridLayout(cols=1, spacing = 1,size_hint=(1,None), size=(1,30))
        self.free_run_container.bind(minimum_height=self.free_run_container.setter('height'))

        scroll_root_free_run = ScrollView(size_hint=(1,None), size=(1,100))
        scroll_root_free_run.add_widget(self.free_run_container)
        ####

        big_one.add_widget(roach_connection_info)
        big_one.add_widget(roach_register)
        big_one.add_widget(scroll_root)
        big_one.add_widget(free_running)
        big_one.add_widget(scroll_root_free_run)

        self.add_widget(big_one)

        self.register_list = []

    def add_registers(self, instance):
        data = Register(orientation='horizontal', size_hint_y=None, size=(1,30))
        data.config()
        self.reg_container.add_widget(data)

    def add_free_running(self, instance):
        btn = Button(text='lol',size_hint_y=None, height=30)
        self.free_run_container.add_widget(btn)


class Register(BoxLayout):

    def __init__(self,**kwargs):
        super(Register, self).__init__(kwargs=kwargs)

    def config(self):
        self.name_label = Label(text='Nombre',size_hint=(0.25,None), height=30)
        self.name_value = TextInput( size_hint=(0.25,None),heigth=30)

        self.values_label = Label(text='Valor', size_hint=(0.25,None), height=30)
        self.values_value = TextInput(size_hint=(0.25,None), height=30)

        self.add_widget(self.name_label)
        self.add_widget(self.name_value)
        self.add_widget(self.values_label)
        self.add_widget(self.values_value)

    def get_name(self):
        return self.name_value._get_text()

    def get_value(self):
        return self.values_value._get_text()

    def get_name_label(self):
        return self.name_label

    def get_name_input(self):
        return self.name_value

    def get_value_label(self):
        return self.values_label

    def get_value_input(self):
        return self.values_value


