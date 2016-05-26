from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton

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

        #self.snapshot_array = {}
        #self.snapshot_cont = 0

        self.prog_dev = False
        self.bof_path = ''

        self.sources = []
        self.function = []

        # reg layout
        roach_connection_info = BoxLayout(orientation='horizontal',  size_hint=(1,None), size=(1,30))
        roach_register = BoxLayout(orientation='horizontal', size_hint=(1,None), size=(1,40))

        ip_label = Label(text='IP :')
        port_label = Label(text='Port :')

        self.ip = TextInput(multiline=False)
        self.port = TextInput(multiline=False, Text='7417')

        roach_connection_info.add_widget(ip_label)
        roach_connection_info.add_widget(self.ip)
        roach_connection_info.add_widget(port_label)
        roach_connection_info.add_widget(self.port)

        clear_button = Button(text='clear', size_hint=(0.33,1))
        save_button = Button(text='save',  size_hint=(0.33,1))
        clear_button.bind(on_press=self.clear_button)
        save_button.bind(on_press=self.button_save_all)
        self.program_button = ToggleButton(text='program',  size_hint=(0.33,1))

        buttons_layout = BoxLayout(orientation='horizontal', size_hint=(1,None), size=(1,30))
        buttons_layout.add_widget(clear_button)
        buttons_layout.add_widget(save_button)
        buttons_layout.add_widget(self.program_button)

        new_reg_label = Label(text='Initial Values', size_hint=(0.6,None), height=40)
        new_reg = Button(text='new reg', size_hint=(0.4,None), height=40)
        new_reg.bind(on_press=self.add_registers)

        roach_register.add_widget(new_reg_label)
        roach_register.add_widget(new_reg)
        ##### Regiter container
        self.reg_container = GridLayout(cols=1, spacing=0, size_hint_y=None)#row_default_height=30)
        self.reg_container.bind(minimum_height=self.reg_container.setter('height'))

        scroll_root = ScrollView(size_hint=(1,1),  size=(1, 125))
        scroll_root.add_widget(self.reg_container)
        ####

        free_running_label_layout = BoxLayout(orientation='horizontal', size_hint=(1,None), size=(1,30))
        add_free_running_label = Label(text="Free Running", size_hint=(0.45,1))
        free_running_label_layout.add_widget(add_free_running_label)

        free_running = BoxLayout(orientation='horizontal', size_hint=(1,None), size=(1,30))
        add_free_running_bram = Button(text = 'New BRAM', size_hint=(0.30,1))
        add_free_running_reg = Button(text = 'New Reg', size_hint=(0.25,1))
        add_free_running_snapshot = Button(text = 'SnapShot', size_hint=(0.25,1))
        add_free_running_bram.bind(on_press=self.add_free_running)
        add_free_running_reg.bind(on_press=self.add_register_free_running)
        add_free_running_snapshot.bind(on_press=self.add_snapshot_free_running)

        free_running.add_widget(add_free_running_bram)
        free_running.add_widget(add_free_running_reg)
        free_running.add_widget(add_free_running_snapshot)

        #### free run container
        self.free_run_container = GridLayout(cols=1, spacing = 3,size_hint=(1,None), size=(1,30))
        self.free_run_container.bind(minimum_height=self.free_run_container.setter('height'))

        scroll_root_free_run = ScrollView(size_hint=(1,1), size=(1,195), scroll_type=['bars'])
        scroll_root_free_run.add_widget(self.free_run_container)
        scroll_root_free_run.bar_width = 10
        ####

        size_ = 30
        name_config = Button(text='Name',size_hint=(0.25,None), height=size_)
        self.name_config_input = TextInput(size_hint=(0.5,None), height=size_)
        buton_bof_file = Button(text='Add bof',size_hint=(0.25,None), height=size_)

        print os.path.dirname(os.path.realpath(__file__)) + '/roach_configurations'


        name_config.bind(on_press=self.open_look_directory)


        fc = BofFileChooserIconView(self.set_bof_path)
        self.file_choose_popup = Popup(title='Choose Bof', auto_dismiss=False, content=fc,\
                                       size_hint=(None, None), size=(400,400))
        fc.set_popup(self.file_choose_popup)
        buton_bof_file.bind(on_press=self.file_choose_popup.open)

        name = BoxLayout(orientation='horizontal', size_hint=(1,None), size=(1,30))
        name.add_widget(name_config)
        name.add_widget(self.name_config_input)
        name.add_widget(buton_bof_file)

        ## store or plot

        big_one.add_widget(name)
        big_one.add_widget(roach_connection_info)
        big_one.add_widget(buttons_layout)
        big_one.add_widget(roach_register)
        big_one.add_widget(scroll_root)
        big_one.add_widget(free_running_label_layout)
        big_one.add_widget(free_running)
        big_one.add_widget(scroll_root_free_run)

        padding_layout = BoxLayout()
        #big_one.add_widget(padding_layout)

        self.add_widget(big_one)
        self.do_extraction = None

    def open_look_directory(self, instance):
        fc_conf = BofFileChooserIconView(self.load_data, path=os.path.dirname(os.path.realpath(__file__)) + '/roach_configurations' , filter=['*.pkl'])
        self.file_roch_popup = Popup(title='Choose Configuration', auto_dismiss=False, content=fc_conf,\
                                       size_hint=(None, None), size=(400,400))
        fc_conf.set_popup(self.file_roch_popup)
        self.file_roch_popup.open()

    def add_register_free_running(self, instance):
        self.load_register_free_running('','')

    def load_register_free_running(self, value_, name_):
        bram = self.create_registers(value_, name_, self.free_run_container, self.remove_from_widget_list_free_run, \
                                     str(self.bram_cont))

        self.bram_array[str(self.bram_cont)] = bram
        bram.set_extraction_function(self.do_extraction)
        self.bram_cont += 1

    def add_registers(self, instance):
        self.load_registers("","", self.reg_container)

    def load_registers(self, values_, name_, where_load_):
        reg_val = self.create_registers(values_, name_, where_load_, self.remove_from_widget_list_config, str(self.reg_cont))

        self.reg_array[str(self.reg_cont)] = reg_val
        self.reg_cont += 1

    def create_registers(self, values_, name_, where_load_, remove_function_, cont_key_):

        size_ = 30
        data = BoxLayout(orientation='horizontal',size_hint=(1, None), size=(1,size_))

        label_name = Label(text='Name', size_hint=(0.225,None), height=size_)
        value_name = TextInput( size_hint=(0.225,None), height=size_)
        label_val = Label(text='Value', size_hint=(0.225,None), height=size_)
        value_val = TextInput( size_hint=(0.225,None), height=size_)
        delate = Button(text='-', size_hint=(0.1,None), height=size_)

        delate.bind(on_press=lambda instant:\
                    remove_function_(data, cont_key_))# where_load_.remove_widget(data))


        data.add_widget(label_name)
        data.add_widget(value_name)
        data.add_widget(label_val)
        data.add_widget(value_val)
        data.add_widget(delate)

        value_name._set_text(name_)
        value_val._set_text(values_)

        where_load_.add_widget(data)

        return Register(value_name, value_val)

    def add_free_running(self, instance):
        self.load_free_running('i', '', [], '','')

    def is_active(self):
        return True

    def activate_extract(self, f):
        self.do_extraction = f

    def get_source_config(self):
        dic_return = {}

        regs = []
        keys = self.reg_array.keys()
        keys.sort()

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

        dic_return['progdev'] = True if self.program_button.state == 'down' else False

        source_dic_config = {}
        for a_source in self.sources:
            source_dic_config.update( a_source.save_config_dictionary())
        dic_return['sources'] = source_dic_config

        function_dic_config = {}
        for a_function in self.function:
            function_dic_config.update(a_function.sava_config_dictionary())
        dic_return['functions'] = function_dic_config

        dic_return['wich'] = self.which_roach()

        # this line saves the dictionary to file with pikle
        self.config_manager.store_dictionary(dic_return)

        dic_return['instance'] = self.get_controller_fpga_insctance()

        return dic_return

    def get_controller_fpga_insctance(self):
        pass

    def set_bof_path(self, path):

        if len(self.name_config_input.text) <1:
            Popup(content=Label(text='Enter Name'), size_hint=(None,None),size=(200,100)).open()
            return

        self.bof_path = self.config_manager.copy_bof_to_folder(path, self.name_config_input._get_text())
        self.program_button.state = "down"

    def load_data(self, path):
        self.clean_all()
        dic = self.config_manager.load_dictionary(path)

        try:
            if dic['wich'] != self.which_roach():
                return
        except:
            pass

        regs = dic['reg']

        for a_reg in regs:
            self.load_registers(a_reg[1], a_reg[0], self.reg_container)

        brams = dic['bram']

        for a_bram in brams:
            if a_bram['is_bram']:
                try:
                    self.load_free_running(a_bram['data_type'],a_bram['size'],a_bram['bram_names'],a_bram['acc_len_reg'], \
                                       a_bram['array_id'], a_bram['store'], a_bram['plot'])
                except:
                    self.load_free_running(a_bram['data_type'],a_bram['size'],a_bram['bram_names'],a_bram['acc_len_reg'], \
                                       a_bram['array_id'])

            else:
                if 'snap' in a_bram:
                    self.load_snapshot_free_running(a_bram['name'])
                else:
                    self.load_register_free_running(a_bram['reg_value'], a_bram['reg_name'])

        self.ip._set_text(dic['ip'])
        self.port._set_text(dic['port'])

        self.program_button.state = 'down' if dic['progdev'] else 'normal'

        self.bof_path = os.path.dirname(os.path.realpath(__file__)) + '/roach_configurations/' + dic['name'] + '/' + dic['name'] + '.bof'
        self.name_config_input._set_text(dic['name'])

        try:
            for a_source in self.sources:
                a_source.set_configuration(dic['sources'])


        except Exception as e:
            pass

        for a_function in self.function:
                a_function.set_configuration(dic['functions'])


        self.do_extraction()

    def load_free_running(self, a_data_type, array_size_, real_imag_list_, acc_len_reg_name_, array_label_, store_ = False, plot_ = False):
        size_ = 30
        data = BoxLayout(orientation='vertical',size_hint=(1, None), size=(1,8*size_))

        #plot_label = Label(text='Plot data:', size_hint=(0.4,1))
        plot_toogle = ToggleButton(text='Plot Data', size_hint=(0.5,1))
        store_data = ToggleButton(text='Store Data', size_hint=(0.5,1))
        handle_data = BoxLayout(orientation='horizontal', size_hint=(1,None), size=(1,30))
        handle_data.add_widget(plot_toogle)
        handle_data.add_widget(store_data)


        data_type_label = Label(text='Tipo de Dato',size_hint=(0.4,None), height=size_)
        data_type_spinner = Spinner(
            # default value shown
            text=a_data_type,
            # available values
            values=['c','b','B','h','H','i','I','l','L','q','Q','f','d'],
            # just for positioning in our example
            size_hint=(0.3, None),
            size = (1,size_)
        )
        delate_label = Label(text='Quitar',size_hint=(0.2,None), height=size_)
        delate_me = Button(text='-',size_hint=(0.1,None), height=size_)
        str_cont = str(self.bram_cont)
        delate_me.bind(on_press=lambda instance:\
            self.remove_from_widget_list_free_run(data, str_cont))

        id_label = Label(text='array name',size_hint=(0.45,None), height=size_)
        id_input = TextInput(size_hint=(0.45,None), height=size_)

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

        data_id = BoxLayout(orientation='horizontal',size_hint=(1, None), size=(1,size_))
        data_id.add_widget(id_label)
        data_id.add_widget(id_input)

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

        data.add_widget(handle_data)
        data.add_widget(data_type)
        data.add_widget(data_id)
        data.add_widget(data_size)
        data.add_widget(data_add_merge_data)
        data.add_widget(data_name)
        data.add_widget(data_acc_len_reg)

        bram = BRAMArray( size_input, acc_len_reg_name_input,real_imag, id_input, data_type_spinner, store_data
                          , plot_toogle)
        bram.set_extraction_function(self.do_extraction)

        add_new_array_to_merge.bind(on_press=lambda instance: bram.add_real_imag_widget())

        self.bram_array[str(self.bram_cont)] = bram
        self.bram_cont += 1
        self.free_run_container.add_widget(data)

        size_input._set_text(array_size_)
        acc_len_reg_name_input._set_text(acc_len_reg_name_)
        id_input._set_text(array_label_)

        store_data.state = 'down' if store_ else 'normal'
        plot_toogle.state = 'down' if plot_ else 'normal'

        for real_imag_pair in real_imag_list_:
            bram.load_real_imag_widget(real_imag_pair[0], real_imag_pair[1])

    def remove_from_widget_list_free_run(self, widget_, list_cont_val_):
        self.free_run_container.remove_widget(widget_)
        del self.bram_array[list_cont_val_]

    def remove_from_widget_list_config(self, widget_, list_cont_val_):
        self.reg_container.remove_widget(widget_)
        del self.reg_array[list_cont_val_]

    def clean_all(self):
        self.free_run_container.clear_widgets()
        self.reg_container.clear_widgets()

        self.bram_array = {}
        self.reg_array = {}

        self.bram_cont = 0
        self.reg_cont = 0

        self.name_config_input.text = ''
        self.bof_path = ''
        self.ip.text = ''
        self.port.text = ''

        self.program_button.state = 'normal'

    def clear_button(self, inatance):
        self.clean_all()

    def button_save_all(self, instance):
        self.get_source_config()

    def pass_source(self, sources_):
        self.sources = sources_

    def pass_functions(self, functions_):
        self.function = functions_

    def which_roach(self):
        pass

    def add_snapshot_free_running(self, instance):
        self.load_snapshot_free_running('')

    def load_snapshot_free_running(self,snapshot_name_):
        size_ = 30
        data = BoxLayout(orientation='horizontal',size_hint=(1, None), size=(1,size_))

        snap_name_label = Label(text='Snap Name',size_hint=(0.4,None), height=size_)
        snap_name_value = TextInput(size_hint=(0.4,None), height=size_)
        snap_name_value.text = snapshot_name_

        delate_me = Button(text='-',size_hint=(0.1,None), height=size_)
        str_cont = str(self.bram_cont)
        delate_me.bind(on_press=lambda instance:\
            self.remove_from_widget_list_free_run(data, str_cont))

        snap = SnapShot(snap_name_value)
        snap.set_extraction_function(self.do_extraction)

        data.add_widget(snap_name_label)
        data.add_widget(snap_name_value)
        data.add_widget(delate_me)

        self.free_run_container.add_widget(data)

        self.bram_array[str(self.bram_cont)] = snap
        self.bram_cont += 1

class Register(object):

    def __init__(self, name, value):

        self.name = name
        self.value = value

        self.active_function = None
        self.is_active_function = False

    def set_extraction_function(self,f):
        self.active_function = f
        self.is_active_function = True

    def get_name(self):
        return self.name._get_text()

    def get_value(self):
        return self.value._get_text()

    def info_dictionary(self):
        dictionary = {'is_bram': False, 'reg_name': self.name.text, 'array_id': self.name.text,
                      'load_data': True if len(self.value.text) > 0 else False}

        if dictionary['load_data']:
            dictionary['reg_value'] = self.value.text
        else:
            dictionary['reg_value'] = ''

        dictionary['plot'] = False
        dictionary['store'] = False

        return dictionary


class BRAMArray(object):

    def __init__(self, size_array, acc_len_reg, grid_layout, array_id, data_type_, data_store_, data_plot_):
        self.size_array = size_array
        self.real_imag_bram = {}
        self.acc_len_reg = acc_len_reg
        self.grid_layout = grid_layout
        self.cont = 0
        self.array_id = array_id

        self.plot = data_plot_
        self.store = data_store_

        self.data_type = data_type_
        self.do_extraction = None

        self.array_id.bind(focus=self.lose_focus)

    def lose_focus(self, instance, value):
        if value:
            return
        self.do_extraction()

    def set_extraction_function(self,f):
        self.do_extraction = f

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

        dictionary['data_type'] = self.data_type.text
        dictionary['size'] = self.size_array._get_text()
        dictionary['acc_len_reg'] = self.acc_len_reg._get_text()
        dictionary['bram_names'] = self.get_names()
        dictionary['array_id'] = self.array_id._get_text()
        dictionary['is_bram'] = True
        dictionary['plot'] = not self.plot.state == 'normal'
        dictionary['store'] = not self.store.state == 'normal'

        return dictionary

    def get_names(self):
        to_return = []

        for key in self.real_imag_bram:
            name_tupple = self.real_imag_bram[key]
            real = name_tupple[0]
            imag = name_tupple[1]

            to_return.append((real._get_text(), imag._get_text()))

        return  to_return

class RoachWarningBox(BoxLayout):

    def __init__(self, text_):
        super(RoachWarningBox, self).__init__(orientation='vertical', size_hint=(1,1))

        top_padding = BoxLayout(size_hint=(1,1))
        self.square_label = Label(text = text_)
        bottom_padding = BoxLayout(size_hint=(1,1))
        buttons = BoxLayout(orientation='horizontal', size_hint=(1, 1))

        ok_button = Button(text='Yes',  size_hint=(1,0.2))
        ok_button.bind(on_press=self.selection_yes)
        cancel_button = Button(text='No', size_hint=(1, 0.2))
        cancel_button.bind(on_press=self.selection_no)

        buttons.add_widget(ok_button)
        buttons.add_widget(cancel_button)

        self.add_widget(top_padding)
        self.add_widget(self.square_label)
        self.add_widget(bottom_padding)
        self.add_widget(buttons)

        self.choosen_name = ''
        self.popup = None

        self.continues = True
        self.choise = True

    def set_popup(self, popup_):
        self.popup = popup_

    def selection_made(self):
        self.popup.dismiss()
        self.continues = False

    def selection_yes(self, instance):
        self.selection_made()

    def selection_no(self, instance):
        self.choise = False
        self.selection_made()

class SnapShot(object):

    def __init__(self, name):
        self.name = name
        self.do_extraction = None
        self.name.bind(focus=self.lose_focus)

    def info_dictionary(self):
        return {'name':self.name.text, 'snap':'shot', 'is_bram':False,'array_id':self.name.text}

    def lose_focus(self, instance, value):
        if value:
            return
        self.do_extraction()

    def set_extraction_function(self,f):
        self.do_extraction = f