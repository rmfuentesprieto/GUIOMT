from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup

from omt.controller.controller_starter import Coordinator
from omt.controller.data.fpga import MissingInformation
from omt.controller.source.source_thread_function import FailToConnectTelnet
from omt.controller.super_controller import SuperCoordinator
from omt.gui.data_processing_panel.data_panel import DataPanel
from omt.gui.extract_data_panel.extract_panel import ExtractPanel
from omt.gui.sourcepanel.source_panel_class import SourcePanel
from omt.gui.super_controller.super_controller_gui import SuperControllerGUI


class RootWidget(BoxLayout):

    def __init__(self):
        super(RootWidget, self).__init__(orientation = 'vertical', size = (800,400))
        self.menu = BoxLayout(orientation='horizontal',size_hint=(1,None), size=(1,40))
        self.panels = BoxLayout(orientation='horizontal')

        button_start = Button(text='Start', size_hint=(0.4,1) ,font_size=14)
        button_start.bind(on_press=self.configure_and_turn_on_sources)

        button_stop = Button(text='Stop', size_hint=(0.4,1), font_size=14)
        button_stop.bind(on_press=self.turn_off)

        button_super_controller = Button(text='Launch Multiple Rutines',size_hint=(0.8,1))
        button_super_controller.bind(on_press=self.super_controller)

        self.menu.add_widget(button_super_controller)
        self.menu.add_widget(button_start)
        self.menu.add_widget(button_stop)

        self.proces = DataPanel()
        self.data = ExtractPanel()
        self.source = SourcePanel()

        self.data.pass_source(self.source.pass_sources())

        self.panels.add_widget(self.proces,0)
        self.panels.add_widget(self.data,1)
        self.panels.add_widget(self.source,2)

        self.add_widget(self.menu)
        self.add_widget(self.panels)

        self.coordinator = None
        self.super_coordinator = None

        self.data.activate_extract(self.get_bram_dictionary)

    def configure_and_turn_on_sources(self, instance):
        source_dictionary = self.source.get_configurations()
        data_dictionary = self.data.get_configurations()
        function_dictionary = self.proces.get_configurations()
        # processing_dictionary = {}
        print data_dictionary

        if  not self.coordinator == None:
            self.coordinator.stop_the_process()
        try:
            self.coordinator = Coordinator(source_dictionary, data_dictionary,function_dictionary)
        except FailToConnectTelnet:
            print 'No se puede connectar'
            return

        # coordinator runs in a new thread
        # and launch some new ones
        self.coordinator.start()

    def configure_super_controller(self, configuration_list):
        """this methos gets the configuratio to run
        multiple routines."""
        print 'super controller starter'

        keys = configuration_list.keys()
        keys.sort()

        full_dictionary = []

        for path_key in keys:
            path = configuration_list[path_key]

            self.data.load_data(path)

            source_dictionary = self.source.get_configurations()
            data_dictionary = self.data.get_configurations()
            function_dictionary = self.proces.get_configurations()

            full_dictionary.append((source_dictionary, data_dictionary, function_dictionary))

        self.super_coordinator = SuperCoordinator(full_dictionary)
        self.super_coordinator.start()

    def turn_off(self, instance):
        self.stop_the_sources()

    def stop_the_sources(self):
        self.stop_coordinator()
        self.stop_super_coordinator()

    def stop_super_coordinator(self):
        if self.super_coordinator == None:
            return
        self.super_coordinator.stop_the_process()

    def stop_coordinator(self):
        if self.coordinator == None:
            return
        self.coordinator.stop_the_process()

    def get_bram_dictionary(self):
        free_run = self.data.get_configurations()['roach']['bram']
        self.proces.update_free_run_dictionary(free_run)

    def super_controller(self, instance):
        pannel = SuperControllerGUI(self)
        popup = Popup(title='Choose Rutines', content=pannel,
              auto_dismiss=False, size_hint=(None, None),size=(400, 400))
        pannel.add_popup(popup)

        popup.open()

class GUIStart(App):
    def build(self):
        app = RootWidget()

        return app