from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.switch import Switch
from kivy.uix.textinput import TextInput

from omt.controller.source.source_tone_or_dc import AnritsuTone
from omt.gui.sourcepanel.alternatives.abstractsource import AbstractSource
from omt.gui.util.units_spinner import UnitSpinner


class Anritsu(AbstractSource):

    def __init__(self,  **kwargs):
        super(Anritsu, self).__init__(kwargs=kwargs)

        self.is_source_active = False

        on_off_label = Label(text='Use Source')
        self.on_off_switch = Switch(active=False)
        self.on_off_switch.bind(active=self.on_off)

        on_off_layout = BoxLayout(orientation='horizontal', size_hint=(1,None), size=(1,40))
        on_off_layout.add_widget(on_off_label)
        on_off_layout.add_widget(self.on_off_switch)

        init_frec_label = Label(text='Frequency',)
        self.init_frec_value = TextInput(multiline=False)
        self.init_frec_value.disabled = True
        self.init_frec_unit = UnitSpinner(UnitSpinner.hz)

        amplitud_frec_label = Label(text='Power')
        self.amplitud_frec_value = TextInput(multiline=False)
        self.amplitud_frec_value.disabled = True
        self.amplitud_frec_value.bind(text=self._check_input_number)
        self.amplitud_frec_unit = UnitSpinner(UnitSpinner.db)

        buttons_configuration = GridLayout(cols=3, row_force_default=True, row_default_height=40)

        buttons_configuration.add_widget(init_frec_label)
        buttons_configuration.add_widget(self.init_frec_value)
        buttons_configuration.add_widget(self.init_frec_unit)

        buttons_configuration.add_widget(amplitud_frec_label)
        buttons_configuration.add_widget(self.amplitud_frec_value)
        buttons_configuration.add_widget(self.amplitud_frec_unit)

        main_layout = BoxLayout(orientation='vertical')
        main_layout.add_widget(on_off_layout)
        main_layout.add_widget(buttons_configuration)

        self.add_widget(main_layout)

    def do_sweep(self):
        return False

    def is_active(self):
        return self.is_source_active

    def get_source_config(self):
        return_dic = {}

        return_dic['ip_direction'] = 'TCPIP0::192.168.1.36::inst0::INSTR'
        return_dic['power'] = self.amplitud_frec_value.text
        return_dic['frequency'] = float(self.init_frec_value.text)*self.init_frec_unit.get_unit_norm()

        return_dic['instance'] = AnritsuTone

        return  return_dic

    def save_config_dictionary(self):
        data_dic = {}

        data_dic['active'] = self.is_source_active
        data_dic['power'] = self.amplitud_frec_value.text
        data_dic['frequency'] = float(self.init_frec_value.text)*self.init_frec_unit.get_unit_norm()

        return {self.get_my_name(): data_dic}

    def get_my_name(self):
        return 'Anritsu'

    def set_configuration(self, config_dictionary):

        if self.get_my_name() in config_dictionary:
            config_dictionary_ = config_dictionary[self.get_my_name()]
            self.is_source_active = config_dictionary_['active']
            self.on_off_switch.active = self.is_source_active
            self.amplitud_frec_value.text = config_dictionary_['power']
            self.init_frec_value.text = str(config_dictionary_['frequency'])

    def on_off(self, spinner, text):
        self.is_source_active = text

        self.init_frec_value.disabled = not text
        self.amplitud_frec_value.disabled = not text

    def _check_input_number(self,instance, value):
        try:
            if len(value) > 0:
                float(value)

        except ValueError:
            if not value == '-':
                instance.text = value[0:-1]
                popup = Popup(title='Error', content=Label(text='Mal valor,\nsolo numeros'),\
                          size_hint=(None, None), size=(120, 100))
                popup.open()