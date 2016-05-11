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


class Agilent(CommonSource):

    def get_my_ip(self):
        return '192.168.1.34'

    def get_my_port(self):
        return '5023'

    def get_my_name(self):
        return 'Agilent'