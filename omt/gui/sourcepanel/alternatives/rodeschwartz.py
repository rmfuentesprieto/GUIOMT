from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.uix.switch import Switch
from kivy.uix.textinput import TextInput

from omt.gui.sourcepanel.alternatives.abstractsource import AbstractSource
from omt.gui.sourcepanel.alternatives.tipical_source import CommonSource
from omt.gui.util.units_spinner import UnitSpinner


class RodeSchwartz(CommonSource):

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
