from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput

from omt.gui.empty import Empty
from omt.gui.extract_data_panel.alternatives.BofFileChooser import BofFileChooserIconView

import os

from omt.gui.extract_data_panel.alternatives.configuration_manager import LoadSaveConfig


class ROACH(Empty):

    def __init__(self, **kwargs):

        super(ROACH, self).__init__(kwargs=kwargs)

        self.config_manager = LoadSaveConfig(os.path.dirname(os.path.realpath(__file__)) + '/roach_configurations')
        big_one = BoxLayout(orientation='vertical')

        self.reg_array = {}
        self.reg_cont = 0

        self.bram_array = {}
        self.bram_cont = 0

        self.bof_path = ''

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

        scroll_root = ScrollView(size_hint=(1,None),  size=(1, 125))
        scroll_root.add_widget(self.reg_container)
        ####

        free_running = BoxLayout(orientation='horizontal', size_hint=(1,None), size=(1,30))
        add_free_running = Button(text = 'Adquirir Nuevo')
        add_free_running.bind(on_press=self.add_free_running)
        free_running.add_widget(add_free_running)

        #### free run container
        self.free_run_container = GridLayout(cols=1, spacing = 3,size_hint=(1,None), size=(1,30))
        self.free_run_container.bind(minimum_height=self.free_run_container.setter('height'))

        scroll_root_free_run = ScrollView(size_hint=(1,None), size=(1,195), scroll_type=['bars'])
        scroll_root_free_run.add_widget(self.free_run_container)
        scroll_root_free_run.bar_width = 10
        ####

        size_ = 30
        name_config = Button(text='Nombre',size_hint=(0.25,None), height=size_)
        self.name_config_input = TextInput(size_hint=(0.5,None), height=size_)
        buton_bof_file = Button(text='Add bof',size_hint=(0.25,None), height=size_)

        fc_conf = BofFileChooserIconView(self.load_data, path=os.path.dirname(os.path.realpath(__file__)) + '/roach_configurations' , filter=['*.pkl'])
        file_roch_popup = Popup(title='Seleccione Configuracion', auto_dismiss=False, content=fc_conf,\
                                       size_hint=(None, None), size=(400,400)  )
        fc_conf.set_popup(file_roch_popup)
        name_config.bind(on_press=file_roch_popup.open)


        fc = BofFileChooserIconView(self.set_bof_path)
        self.file_choose_popup = Popup(title='Seleccione Bof', auto_dismiss=False, content=fc,\
                                       size_hint=(None, None), size=(400,400))
        fc.set_popup(self.file_choose_popup)

        buton_bof_file.bind(on_press=self.file_choose_popup.open)

        name = BoxLayout(orientation='horizontal', size_hint=(1,None), size=(1,30))
        name.add_widget(name_config)
        name.add_widget(self.name_config_input)
        name.add_widget(buton_bof_file)

        big_one.add_widget(name)
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

        real_imag = GridLayout(cols=1, spacing = 3,size_hint=(1,None), size=(1,60))
        real_imag.bind(minimum_height=real_imag.setter('height'))

        scroll_real_imag = ScrollView(size_hint=(0.8,None), size=(1,2*size_))
        scroll_real_imag.add_widget(real_imag)

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
        data_name.add_widget(scroll_real_imag)

        data_acc_len_reg = BoxLayout(orientation='horizontal',size_hint=(1, None), size=(1,size_))
        data_acc_len_reg.add_widget(acc_len_reg_name_label)
        data_acc_len_reg.add_widget(acc_len_reg_name_input)

        data.add_widget(data_type)
        data.add_widget(data_size)
        data.add_widget(data_add_merge_data)
        data.add_widget(data_name)
        data.add_widget(data_acc_len_reg)

        bram = BRAMArray( size_input, acc_len_reg_name_input,real_imag)
        data_type_spinner.bind(text=bram.selected_data_type)

        add_new_array_to_merge.bind(on_press=lambda instance: bram.add_real_imag_widget())

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

        brams = []
        for bram in self.bram_array:
            brams.append(self.bram_array[bram].info_dictionary())

        dic_return['bram'] = brams

        dic_return['ip'] = self.ip._get_text()
        dic_return['port'] = self.port._get_text()

        dic_return['bof_path'] = self.bof_path
        dic_return['name'] = self.name_config_input._get_text()

        self.config_manager.store_dictionary(dic_return)

        return dic_return

    def set_bof_path(self, path):

        path = path[0]
        if len(self.name_config_input._get_text()) <1:
            Popup(content=Label(text='Ingrese Nombre'), size_hint=(None,None),size=(200,100)).open()
            return

        self.config_manager.copy_bof_to_folder(path, self.name_config_input._get_text())

    def load_data(self, path):
        path = path[0]
        dic = self.config_manager.load_dictionary(path)
        print 2

        regs = dic['reg']

        for a_reg in regs:
            self.load_registers(a_reg[1], a_reg[0])

        brams = dic['bram']
        '''
        dictionary['data_type'] = self.data_type
        dictionary['size'] = self.size_array._get_text()
        dictionary['acc_len_reg'] = self.acc_len_reg._get_text()
        dictionary['bram_names'] = self.get_names()
        '''

        for a_bram in brams:
            self.load_free_running(a_bram['data_type'],a_bram['size'],a_bram['bram_names'],a_bram['acc_len_reg'])

        self.ip._set_text(dic['ip'])
        self.port._set_text(dic['port'])

        self.bof_path = dic['bof_path']
        self.name_config_input._set_text(dic['name'])

    def load_registers(self, values_, name_):

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

        value_name._set_text(name_)
        value_val._set_text(values_)

    def load_free_running(self, data_type, array_size_, real_imag_list_, acc_len_reg_name_):
        size_ = 30
        data = BoxLayout(orientation='vertical',size_hint=(1, None), size=(1,6*size_))

        data_type_label = Label(text='Tipo de Dato',size_hint=(0.4,None), height=size_)
        data_type_spinner = Spinner(
            # default value shown
            text=data_type,
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

        real_imag = GridLayout(cols=1, spacing = 3,size_hint=(1,None), size=(1,60))
        real_imag.bind(minimum_height=real_imag.setter('height'))

        scroll_real_imag = ScrollView(size_hint=(0.8,None), size=(1,2*size_))
        scroll_real_imag.add_widget(real_imag)

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
        data_name.add_widget(scroll_real_imag)

        data_acc_len_reg = BoxLayout(orientation='horizontal',size_hint=(1, None), size=(1,size_))
        data_acc_len_reg.add_widget(acc_len_reg_name_label)
        data_acc_len_reg.add_widget(acc_len_reg_name_input)

        data.add_widget(data_type)
        data.add_widget(data_size)
        data.add_widget(data_add_merge_data)
        data.add_widget(data_name)
        data.add_widget(data_acc_len_reg)

        bram = BRAMArray( size_input, acc_len_reg_name_input,real_imag)
        data_type_spinner.bind(text=bram.selected_data_type)

        add_new_array_to_merge.bind(on_press=lambda instance: bram.add_real_imag_widget())

        self.bram_array[str(self.bram_cont)] = bram
        self.bram_cont += 1
        self.free_run_container.add_widget(data)

        size_input._set_text(array_size_)
        acc_len_reg_name_input._set_text(acc_len_reg_name_)

        for real_imag_pair in real_imag_list_:
            bram.load_real_imag_widget(real_imag_pair[0], real_imag_pair[1])

class Register(object):

    def __init__(self, name, value):

        self.name = name
        self.value = value

    def get_name(self):
        return self.name._get_text()

    def get_value(self):
        return self.value._get_text()

class BRAMArray(object):
    def __init__(self, size_array, acc_len_reg, grid_layout):
        self.size_array = size_array
        self.real_imag_bram = {}
        self.acc_len_reg = acc_len_reg
        self.grid_layout = grid_layout
        self.cont = 0

        self.data_type = 'q'

    def add_real_imag(self, real_bram, imag_bram, key):
        self.real_imag_bram[key] = (real_bram,imag_bram)

    def del_bram(self, key):
        del self.real_imag_bram[key]

    def del_widget(self, wid):
        self.grid_layout.remove_widget(wid)

    def add_real_imag_widget(self):
        size_ = 30

        real_label = Label(text='real', size_hint=(0.225,None), height=size_)
        real_input = TextInput(size_hint=(0.225,None), height=size_)

        imag_label = Label(text='imag', size_hint=(0.225,None), height=size_)
        imag_input = TextInput(size_hint=(0.225,None), height=size_)

        del_button = Button(text='-', size_hint=(0.1,None), height=size_)


        data = BoxLayout(orientation='horizontal',size_hint=(1, None), size=(1,size_))

        data.add_widget(real_label)
        data.add_widget(real_input)
        data.add_widget(imag_label)
        data.add_widget(imag_input)
        data.add_widget(del_button)

        self.grid_layout.add_widget(data)
        self.grid_layout.width += 30

        a_key = self.cont
        self.cont += 1
        del_button.bind(on_press=lambda instant: self.remove_all(data, a_key))

        self.add_real_imag(real_input, imag_input, a_key)

    def load_real_imag_widget(self, real_name_, imag_name_):
        size_ = 30

        real_label = Label(text='real', size_hint=(0.225,None), height=size_)
        real_input = TextInput(size_hint=(0.225,None), height=size_)

        imag_label = Label(text='imag', size_hint=(0.225,None), height=size_)
        imag_input = TextInput(size_hint=(0.225,None), height=size_)

        del_button = Button(text='-', size_hint=(0.1,None), height=size_)


        data = BoxLayout(orientation='horizontal',size_hint=(1, None), size=(1,size_))

        data.add_widget(real_label)
        data.add_widget(real_input)
        data.add_widget(imag_label)
        data.add_widget(imag_input)
        data.add_widget(del_button)

        self.grid_layout.add_widget(data)
        self.grid_layout.width += 30

        a_key = self.cont
        self.cont += 1
        del_button.bind(on_press=lambda instant: self.remove_all(data, a_key))

        self.add_real_imag(real_input, imag_input, a_key)

        real_input._set_text(real_name_)
        imag_input._set_text(imag_name_)

    def remove_all(self, data, key):
        self.del_widget(data)
        self.del_bram(key)

    def info_dictionary(self):
        dictionary = {}

        dictionary['data_type'] = self.data_type
        dictionary['size'] = self.size_array._get_text()
        dictionary['acc_len_reg'] = self.acc_len_reg._get_text()
        dictionary['bram_names'] = self.get_names()

        return dictionary

    def selected_data_type(self, instant, text):
        self.data_type = text

    def get_names(self):
        to_return = []

        for key in self.real_imag_bram:
            name_tupple = self.real_imag_bram[key]
            real = name_tupple[0]
            imag = name_tupple[1]

            to_return.append((real._get_text(), imag._get_text()))

        return  to_return


