from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.uix.switch import Switch
from kivy.uix.textinput import TextInput

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

    def get_my_ip(self):
        pass

    def get_my_port(self):
        pass

    def sweepe_or_not(self, spinner, text):
        self.do_a_sweep = text
        self.final_frec_value.disabled = not text
        self.delta_frec_value.disabled = not text
        self.puntos_frec_value.disabled = not text

    def on_off(self, spinner, text):
        self.is_source_active = text
        print self.is_source_active
        self.final_frec_value.disabled = not text
        self.delta_frec_value.disabled = not text
        self.puntos_frec_value.disabled = not text
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
        pass

    def change_delta_frec(self, instance, value):
        pass


    def change_points_number(self, instance, value):
        self._check_input_number(instance, value)
        pass

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
            data_dic['frec_init'] = float(self.init_frec_value._get_text())
            data_dic['frec_end'] = float(self.final_frec_value._get_text())
            data_dic['frec_number_point'] = int(self.puntos_frec_value._get_text())

        else:
            data_dic['frec'] = float(self.init_frec_value._get_text())

        return data_dic


