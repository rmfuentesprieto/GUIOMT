from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput

from omt.gui.empty import Empty


class ROACH(Empty):

    def __init__(self, **kwargs):

        super(ROACH, self).__init__(kwargs=kwargs)

        big_one = BoxLayout(orientation='vertical')

        self.reg_array = {}
        self.reg_cont = 0

        self.bram_array = {}
        self.bram_cont = 0

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
        self.reg_container = GridLayout(cols=1, spacing=0, size_hint_y=None)#row_default_height=30)
        self.reg_container.bind(minimum_height=self.reg_container.setter('height'))

        scroll_root = ScrollView(size_hint=(1,None),  size=(1, 175))
        scroll_root.add_widget(self.reg_container)
        ####

        free_running = BoxLayout(orientation='horizontal', size_hint=(1,None), size=(1,30))
        add_free_running = Button(text = 'Adquirir Nuevo')
        add_free_running.bind(on_press=self.add_free_running)
        free_running.add_widget(add_free_running)

        #### free run container
        self.free_run_container = GridLayout(cols=1, spacing = 3,size_hint=(1,None), size=(1,30))
        self.free_run_container.bind(minimum_height=self.free_run_container.setter('height'))

        scroll_root_free_run = ScrollView(size_hint=(1,None), size=(1,175))
        scroll_root_free_run.add_widget(self.free_run_container)
        ####

        big_one.add_widget(roach_connection_info)
        big_one.add_widget(roach_register)
        big_one.add_widget(scroll_root)
        big_one.add_widget(free_running)
        big_one.add_widget(scroll_root_free_run)

        self.add_widget(big_one)

    def add_registers(self, instance):

        size_ = 30
        data = BoxLayout(orientation='horizontal',size_hint=(1, None), size=(1,size_))

        label_name = Label(text='nombre', size_hint=(0.225,None), height=size_)
        value_name = TextInput( size_hint=(0.225,None), height=size_)
        label_val = Label(text='valor', size_hint=(0.225,None), height=size_)
        value_val = TextInput( size_hint=(0.225,None), height=size_)
        delate = Button(text='-', size_hint=(0.1,None), height=size_)
        delate.bind(on_press=lambda instant: self.reg_container.remove_widget(data))

        data.add_widget(label_name)
        data.add_widget(value_name)
        data.add_widget(label_val)
        data.add_widget(value_val)
        data.add_widget(delate)

        reg_val = Register(value_name, value_val)
        self.reg_array[str(self.reg_cont)] = reg_val
        self.reg_cont += 1

        self.reg_container.add_widget(data)

    def add_free_running(self, instance):
        size_ = 30
        data = BoxLayout(orientation='vertical',size_hint=(1, None), size=(1,6*size_))

        data_type_label = Label(text='Tipo de Dato',size_hint=(0.4,None), height=size_)
        data_type_spinner = Spinner(
            # default value shown
            text='i',
            # available values
            values=['i','q','Q'],
            # just for positioning in our example
            size_hint=(0.3, None),
            size = (1,size_)
        )
        delate_label = Label(text='Quitar',size_hint=(0.2,None), height=size_)
        delate_me = Button(text='-',size_hint=(0.1,None), height=size_)
        delate_me.bind(on_press=lambda instant: self.free_run_container.remove_widget(data))

        size_label = Label(text='tamano',size_hint=(0.45,None), height=size_)
        size_input = TextInput(size_hint=(0.45,None), height=size_)

        add_new_array_to_merge = Button(text='+',size_hint=(None,None), height=size_, wide = 3*size_)
        #add_new_array_to_merge.bind(on_press=)

        real_imag = GridLayout(cols=1, spacing = 3,size_hint=(1,None), size=(1,30))
        real_imag.bind(minimum_height=self.free_run_container.setter('height'))

        scroll_real_imag = ScrollView(size_hint=(0.8,None), size=(1,2*size_))
        scroll_real_imag.add_widget(real_imag)
        space_begin = Label(text='  ',size_hint=(0.1,None), height=2*size_)
        space_end = Label(text='  ',size_hint=(0.1,None), height=2*size_)

        real_label = Label(text='real', size_hint=(0.25,None), height=size_)
        real_input = TextInput(size_hint=(0.25,None), height=size_)

        imag_label = Label(text='imag', size_hint=(0.25,None), height=size_)
        imag_input = TextInput(size_hint=(0.25,None), height=size_)

        acc_len_reg_name_label = Label(text='acc len reg_name',size_hint=(0.5,None), height=size_)
        acc_len_reg_name_input = TextInput(size_hint=(0.5,None), height=size_)

        data_type = BoxLayout(orientation='horizontal',size_hint=(1, None), size=(1,size_))
        data_type.add_widget(data_type_label)
        data_type.add_widget(data_type_spinner)
        data_type.add_widget(delate_label)
        data_type.add_widget(delate_me)

        data_size = BoxLayout(orientation='horizontal',size_hint=(1, None), size=(1,size_))
        data_size.add_widget(size_label)
        data_size.add_widget(size_input)

        data_add_merge_data = BoxLayout(orientation='horizontal',size_hint=(1, None), size=(1,size_))
        data_add_merge_data.add_widget(add_new_array_to_merge)

        data_name = BoxLayout(orientation='horizontal',size_hint=(1, None), size=(1,2*size_))
        data_name.add_widget(space_begin)
        data_name.add_widget(scroll_real_imag)
        data_name.add_widget(space_end)


        data_acc_len_reg = BoxLayout(orientation='horizontal',size_hint=(1, None), size=(1,size_))
        data_acc_len_reg.add_widget(acc_len_reg_name_label)
        data_acc_len_reg.add_widget(acc_len_reg_name_input)

        data.add_widget(data_type)
        data.add_widget(data_size)
        data.add_widget(data_add_merge_data)
        data.add_widget(data_name)
        data.add_widget(data_acc_len_reg)

        bram = BRAMArray(data_type_spinner, size_input, acc_len_reg_name_input)
        self.bram_array[str(self.bram_cont)] = bram
        self.bram_cont += 1

        self.free_run_container.add_widget(data)

    def is_active(self):
        return True

    def get_source_config(self):
        dic_return = {}

        regs = []
        keys = self.reg_array.keys()
        for a_reg in keys:
            aux_data = self.reg_array[a_reg]
            reg_name = aux_data.get_name()
            reg_val = aux_data.get_value()

            regs.append((reg_name, reg_val))

        dic_return['reg'] = regs

        for bram in self.bram_array:
            pass

        return dic_return

class Register(object):

    def __init__(self, name, value):

        self.name = name
        self.value = value

    def get_name(self):
        return self.name._get_text()

    def get_value(self):
        return self.value._get_text()

class BRAMArray(object):
    def __init__(self, data_type, size_array, acc_len_reg):
        self.data_type = data_type
        self.size_array = size_array
        self.real_imag_bram = {}
        self.acc_len_reg = acc_len_reg

    def add_real_imag(self, real_bram, imag_bram, key):
        self.real_imag_bram[key] = (real_bram,imag_bram)

    def del_bram(self, key):
        del self.real_imag_bram[key]