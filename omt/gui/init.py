from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

from omt.controller.controller_starter import Coordinator
from omt.controller.source.source_thread_function import FailToConnectTelnet
from omt.gui.data_processing_panel.data_panel import DataPanel
from omt.gui.extract_data_panel.extract_panel import ExtractPanel
from omt.gui.sourcepanel.source_panel_class import SourcePanel


class RootWidget(BoxLayout):
    def __init__(self):
        super(RootWidget, self).__init__(orientation = 'vertical', size = (800,400))
        self.menu = BoxLayout(orientation='horizontal',size_hint=(1,None), size=(1,40))
        self.panels = BoxLayout(orientation='horizontal')

        button_start = Button(text='Start', font_size=14)
        button_start.bind(on_press=self.configure_and_turn_on_sources)

        button_stop = Button(text='Stop', font_size=14)
        button_stop.bind(on_press=self.turn_off)


        self.menu.add_widget(button_start)
        self.menu.add_widget(button_stop)

        self.proces = DataPanel()
        self.data = ExtractPanel()
        self.source = SourcePanel()

        self.panels.add_widget(self.proces,0)
        self.panels.add_widget(self.data,1)
        self.panels.add_widget(self.source,2)

        self.add_widget(self.menu)
        self.add_widget(self.panels)

        self.coordinator = []

    def configure_and_turn_on_sources(self, instance):
        source_dictionary = self.source.get_configurations()
        data_dictionary = self.data.get_configurations()
        # processing_dictionary = {}
        print data_dictionary

        try:
            self.coordinator = Coordinator(source_dictionary, data_dictionary)
        except FailToConnectTelnet:
            print 'No se puede connectar'

        # coordinator runs in a new thread
        # and launch some new ones
        # self.coordinator.start()

    def turn_off(self, instance):
        self.stop_the_sources()

    def stop_the_sources(self):
        self.coordinator.stop_the_process()

class GUIStart(App):
    def build(self):
        app = RootWidget()

        return app