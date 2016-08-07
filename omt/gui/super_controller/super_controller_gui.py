import os
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView

from omt.gui.extract_data_panel.alternatives.BofFileChooser import BofFileChooserIconView


class SuperControllerGUI(BoxLayout):

    def __init__(self, root_class):
        super(SuperControllerGUI, self).__init__(orientation='vertical')

        self.add_button = Button(text='Add New Rutine', size_hint=(1,None), size=(1,40))
        self.add_button.bind(on_press=self.add_routine)

        self.ok_button = Button(text='OK', size_hint=(1, None), size=(1, 40))
        self.ok_button.bind(on_press=self.ok_opoup)

        self.cancel_button = Button(text='Cancel', size_hint=(1, None), size=(1, 40))
        self.cancel_button.bind(on_press=self.close_opoup)

        self.path_container = GridLayout(cols=1, spacing=0, size_hint_y=None)  # row_default_height=30)
        self.path_container.bind(minimum_height=self.path_container.setter('height'))

        scroll_root = ScrollView(size_hint=(1, 1))
        scroll_root.add_widget(self.path_container)

        self.buttons_layout = BoxLayout(orientation='horizontal', size_hint=(1,None), size=(1,40))
        self.buttons_layout.add_widget(self.ok_button)
        self.buttons_layout.add_widget(self.cancel_button)

        self.add_widget(self.add_button)
        self.add_widget(scroll_root)
        self.add_widget(self.buttons_layout)

        self.config_path = {}
        self.config_cont = 0

        self.control_gui = root_class

    def add_popup(self, opopup):
        self.popup = opopup

    def close_opoup(self, instance):
        self.popup.dismiss()

    def add_routine(self, instance):
        file_dir = os.path.dirname(os.path.realpath(__file__))
        file_dir = file_dir.replace('super_controller','extract_data_panel/alternatives/roach_configurations')
        fc_conf = BofFileChooserIconView(self.load_data,
                                         path=file_dir,
                                         filter=['*.pkl'])
        self.file_roch_popup = Popup(title='Choose Configuration', auto_dismiss=False, content=fc_conf, \
                                     size_hint=(None, None), size=(400, 400))
        fc_conf.set_popup(self.file_roch_popup)
        self.file_roch_popup.open()

    def load_data(self, path):

        self.config_path[str(self.config_cont)] = path

        name= path.split('/')[-2]
        path_button = Button(text=name, size_hint=(1, None), size=(1, 40))
        key = self.config_cont
        path_button.bind(on_press=lambda instance: self.del_path(str(key), path_button))
        self.config_cont += 1

        self.path_container.add_widget(path_button)

    def del_path(self, key, button):
        del self.config_path[key]
        self.path_container.remove_widget(button)

    def ok_opoup(self, instance):
        self.control_gui.configure_super_controller(self.config_path)
        self.popup.dismiss()