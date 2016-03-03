from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button


from omt.gui.data_processing_panel.data_panel import DataPanel
from omt.gui.extract_data_panel.extract_panel import ExtractPanel
from omt.gui.sourcepanel.source_panel_class import SourcePanel


class RootWidget(BoxLayout):
    def __init__(self):
        super(RootWidget, self).__init__(orientation = 'vertical')
        self.menu = BoxLayout(orientation='horizontal',size_hint=(1,None), size=(1,40))
        self.panels = BoxLayout(orientation='horizontal')
        button = Button(text='Start', font_size=14)
        button.bind(on_press=self.configure_and_turn_on_sources)

        self.menu.add_widget(button)

        self.proces = DataPanel()
        self.data = ExtractPanel()
        self.source = SourcePanel()

        self.panels.add_widget(self.proces,0)
        self.panels.add_widget(self.data,1)
        self.panels.add_widget(self.source,2)

        self.add_widget(self.menu)
        self.add_widget(self.panels)

    def configure_and_turn_on_sources(self, instance):
        print 'pre'



class GUIStart(App):
    def build(self):
        app = RootWidget()
        return app