from kivy.uix.screenmanager import Screen


class Empty(Screen):

    def __init__(self,**kwargs):
         super(Empty, self).__init__(kwargs=kwargs)

    def is_active(self):
        return False

    def get_source_config(self):
        return {}

    def save_config_dictionary(self):
        return {}

    def set_configuration(self, dic):
        pass