from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.uix.switch import Switch
from kivy.uix.textinput import TextInput

from omt.controller.source.source_thread_function import SourceThread
from omt.gui.sourcepanel.alternatives.abstractsource import AbstractSource
from omt.gui.util.units_spinner import UnitSpinner


class CommonSource(AbstractSource):

    def __init__(self, **kwargs):

        super(CommonSource, self).__init__(kwargs=kwargs)

        main_layout = BoxLayout(orientation='vertical')
        on_off_layout = BoxLayout(orientation='horizontal', size_hint=(1,None), size=(1,40))
        sweep_layout = BoxLayout(orientation='horizontal', size_hint=(1,None), size=(1,40))
        buttons_configuration = GridLayout(cols=3, row_force_default=True, row_default_height=40)

        self.is_source_active = False
        self.do_a_sweep = False

        on_off_label = Label(text='Usar Fuente')
        self.on_off_switch = Switch(active=False)
        self.on_off_switch.bind(active=self.on_off)
        on_off_layout.add_widget(on_off_label)
        on_off_layout.add_widget(self.on_off_switch)

        sweep_label = Label(text='Hacer Barrido')
        self.sweep_switch = Switch(active=False)
        self.sweep_switch.bind(active=self.sweepe_or_not)
        sweep_layout.add_widget(sweep_label)
        sweep_layout.add_widget(self.sweep_switch)

        init_frec_label = Label(text='Frecuencia\ninicio',)
        self.init_frec_value = TextInput(multiline=False)
        self.init_frec_value.disabled = True
        self.init_frec_value.bind(text=self.update_values)
        self.init_frec_unit = UnitSpinner(UnitSpinner.hz)

        final_frec_label = Label(text='Frecuencia\ntermino')
        self.final_frec_value = TextInput(multiline=False)
        self.final_frec_value.disabled = True
        self.final_frec_value.bind(text=self.update_values)
        self.final_frec_unit = UnitSpinner(UnitSpinner.hz)

        delta_frec_label = Label(text='Delta\nfrecuencia')
        self.delta_frec_value = TextInput(multiline=False)
        self.delta_frec_value.disabled = True
        self.delta_frec_value.bind(text=self.change_delta_frec)
        self.delta_frec_unit = UnitSpinner(UnitSpinner.hz)

        puntos_frec_label = Label(text='Numero\nde puntos')
        self.puntos_frec_value = TextInput(multiline=False)
        self.puntos_frec_value.disabled = True
        self.puntos_frec_value.bind(text=self.change_points_number)
        self.puntos_frec_unit = UnitSpinner(UnitSpinner.simple)

        amplitud_frec_label = Label(text='Potencia')
        self.amplitud_frec_value = TextInput(multiline=False)
        self.amplitud_frec_value.disabled = True
        self.amplitud_frec_value.bind(text=self._check_input_number)
        self.amplitud_frec_unit = UnitSpinner(UnitSpinner.db)



        buttons_configuration.add_widget(init_frec_label)
        buttons_configuration.add_widget(self.init_frec_value)
        buttons_configuration.add_widget(self.init_frec_unit)

        buttons_configuration.add_widget(final_frec_label)
        buttons_configuration.add_widget(self.final_frec_value)
        buttons_configuration.add_widget(self.final_frec_unit)

        buttons_configuration.add_widget(delta_frec_label)
        buttons_configuration.add_widget(self.delta_frec_value)
        buttons_configuration.add_widget(self.delta_frec_unit)

        buttons_configuration.add_widget(puntos_frec_label)
        buttons_configuration.add_widget(self.puntos_frec_value)
        buttons_configuration.add_widget(self.puntos_frec_unit)

        buttons_configuration.add_widget(amplitud_frec_label)
        buttons_configuration.add_widget(self.amplitud_frec_value)
        buttons_configuration.add_widget(self.amplitud_frec_unit)

        main_layout.add_widget(on_off_layout)
        main_layout.add_widget(sweep_layout)
        main_layout.add_widget(buttons_configuration)

        self.add_widget(main_layout)

        self.manual_change_delta = False
        self.manual_change_puntos = False
        self.manual_change_init = False
        self.manual_change_final = False

    def get_my_name(self):
        pass

    def get_my_ip(self):
        pass

    def get_my_port(self):
        pass

    def sweepe_or_not(self, spinner, text):
        self.do_a_sweep = text
        self.final_frec_value.disabled = not (text and self.is_source_active)
        self.delta_frec_value.disabled = not (text and self.is_source_active)
        self.puntos_frec_value.disabled = not (text and self.is_source_active)

    def on_off(self, spinner, text):
        self.is_source_active = text

        self.final_frec_value.disabled = not (text and self.do_a_sweep)
        self.delta_frec_value.disabled = not (text and self.do_a_sweep)
        self.puntos_frec_value.disabled = not (text and self.do_a_sweep)
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

    def update_values(self, instance, value):
        self._check_input_number(instance, value)

    def change_delta_frec(self, instance, value):
        self._check_input_number(instance, value)
        print 'frec'

        if self.manual_change_delta:
            self.manual_change_delta = False
            return

        frec_init = self.init_frec_value._get_text()
        frec_final = self.final_frec_value._get_text()

        if len(frec_init) < 1 or len(frec_final) < 1:
            return

        frec_init = float(frec_init)*self.init_frec_unit.get_unit_norm()
        frec_final = float(frec_final)*self.final_frec_unit.get_unit_norm()

        delta = float(self.delta_frec_value.text)*self.delta_frec_unit.get_unit_norm()

        npoints = int((delta + frec_final - frec_init)/delta) + 1

        power10 = 1
        while npoints >= 1000 or npoints < 1:
            if npoints >= 1000:
                power10 *= 10**3
                npoints *= 10**-3
            elif npoints < 1:
                power10 *=10**-3
                npoints *= 10**3

        self.manual_change_puntos = True

        self.puntos_frec_value.text = str(npoints)
        self.puntos_frec_unit.set_unit(power10)

        print 'end'

    def change_points_number(self, instance, value):
        self._check_input_number(instance, value)

        if self.manual_change_puntos:
            self.manual_change_puntos = False
            return

        frec_init = self.init_frec_value._get_text()
        frec_final = self.final_frec_value._get_text()

        if len(frec_init) < 1 or len(frec_final) < 1:
            return

        frec_init = float(frec_init)*self.init_frec_unit.get_unit_norm()
        frec_final = float(frec_final)*self.final_frec_unit.get_unit_norm()

        npoint = float(self.puntos_frec_value.text)*self.puntos_frec_unit.get_unit_norm()
        if npoint < 2:
            return

        delta = (frec_final - frec_init)/(npoint - 1)

        power10 = 1
        while delta >= 1000 or delta < 1:
            if delta >= 1000:
                power10 *= 10**3
                delta *= 10**-3
            elif delta < 1:
                power10 *=10**-3
                delta *= 10**3

        self.manual_change_delta = True

        self.delta_frec_unit.set_unit(power10)
        self.delta_frec_value.text = str(delta)

        print 'end pp'

    def is_active(self):
        return self.is_source_active

    def do_sweep(self):
        return self.do_a_sweep

    def get_source_config(self):
        data_dic = {}
        data_dic['ip'] = self.get_my_ip()
        data_dic['port'] = self.get_my_port()
        data_dic['power'] = self.amplitud_frec_value._get_text()

        if self.do_a_sweep:
            data_dic['frec_init'] = float(self.init_frec_value._get_text())*self.init_frec_unit.get_unit_norm()
            data_dic['frec_end'] = float(self.final_frec_value._get_text())*self.final_frec_unit.get_unit_norm()
            data_dic['frec_number_point'] = int(self.puntos_frec_value._get_text())*self.puntos_frec_unit.get_unit_norm()
            data_dic['instance'] = SourceThread

        else:
            data_dic['frec'] = float(self.init_frec_value._get_text())*self.init_frec_unit.get_unit_norm()

        data_dic['name'] = self.get_my_name()

        return data_dic

    def save_config_dictionary(self):
        data_dic = {}

        data_dic['use_source'] = self.is_source_active
        data_dic['sweep'] = self.do_a_sweep
        data_dic['ip'] = self.get_my_ip()
        data_dic['port'] = self.get_my_port()
        data_dic['power'] = self.amplitud_frec_value._get_text()

        data_dic['frec_init'] = self.init_frec_value._get_text()
        data_dic['frec_init_unit'] = self.init_frec_unit.get_unit()
        data_dic['frec_end'] = self.final_frec_value._get_text()
        data_dic['frec_end_unit'] = self.final_frec_unit.get_unit()
        data_dic['frec_number_point'] = self.puntos_frec_value._get_text()
        data_dic['frec_numer_points_unit'] = self.puntos_frec_unit.get_unit()

        return {self.get_my_name():data_dic}

    def set_configuration(self, config_dictionary):

        if self.get_my_name() in config_dictionary:
            config_dictionary_ = config_dictionary[self.get_my_name()]

            self.is_source_active = config_dictionary_['use_source']
            self.on_off_switch.active = self.is_source_active

            self.do_a_sweep = config_dictionary_['sweep']
            self.sweep_switch.active = self.do_a_sweep

            self.amplitud_frec_value.text = config_dictionary_['power']

            self.init_frec_value.text = config_dictionary_['frec_init']
            self.init_frec_unit.text = config_dictionary_['frec_init_unit']

            self.final_frec_value.text = config_dictionary_['frec_end']
            self.final_frec_unit.text = config_dictionary_['frec_end_unit']

            self.puntos_frec_value.text = config_dictionary_['frec_number_point']
            self.puntos_frec_unit.text = config_dictionary_['frec_numer_points_unit']