from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.button import Label
from kivy.uix.screenmanager import Screen


class Empty(Screen):

    def __init__(self,**kwargs):
         super(Empty, self).__init__(kwargs=kwargs)

    def is_active(self):
        return False
