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
        self.final_frec_value.disabled = not text
        self.delta_frec_value.disabled = not text
        self.puntos_frec_value.disabled = not text

    def on_off(self, spinner, text):
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
            instance.text = value[0:-1]
            popup = Popup(title='Error', content=Label(text='Mal valor,\nsolo numeros'),\
                          size_hint=(None, None), size=(120, 100))
            popup.open()

    def update_values(self, instance, value):
        self._check_input_number(instance, value)
        if self.sweep_switch.active:

            frec_initial = self.init_frec_value.text
            frec_final = self.final_frec_value.text

            if len(frec_final) == 0 or len(frec_initial) == 0:
                return

            frec_final = float(frec_final) * self.final_frec_unit.get_unit_norm()
            frec_initial = float(frec_initial) * self.init_frec_unit.get_unit_norm()

            points = self.puntos_frec_value.text
            delta = self.delta_frec_value.text

            if len(points) != 0 and points != '1':
                points = int(points)
                print (frec_final - frec_initial)/(int(points) - 1)
                aux_delta = str((frec_final - frec_initial)/(int(points) - 1))
                if len(aux_delta) > 9:
                    aux_delta = aux_delta[0:8]
                self.delta_frec_value.text = aux_delta
                return

            if len(delta) != 0:
                delta = float(delta)
                self.puntos_frec_value.text = str(int((frec_final - frec_initial)/delta) + 1)


        else:
            pass

    def change_delta_frec(self, instance, value):
        self._check_input_number(instance, value)

        frec_initial = self.init_frec_value.text
        frec_final = self.final_frec_value.text

        if len(frec_final) == 0 or len(frec_initial) == 0:
            return

        frec_final = float(frec_final) * self.final_frec_unit.get_unit_norm()
        frec_initial = float(frec_initial) * self.init_frec_unit.get_unit_norm()

        delta_frec = value * self.delta_frec_unit.get_unit_norm()

        number_of_points = str((frec_final - frec_initial) / (delta_frec))

        while( number_of_points < 1 or number_of_points > 999):
            break


    def change_points_number(self, instance, value):
        self._check_input_number(instance, value)
        pass
