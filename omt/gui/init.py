from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button


from omt.gui.data_processing_panel.data_panel import DataPanel
from omt.gui.extract_data_panel.extract_panel import ExtractPanel
from omt.gui.sourcepanel.source_panel_class import SourcePanel


class RootWidget(BoxLayout):
    def __init__(self):
        super(RootWidget, self).__init__(orientation = 'horizontal')

        self.add_widget(DataPanel(),0)
        self.add_widget(ExtractPanel(),1)
        self.add_widget(SourcePanel(),2)



class GUIStart(App):
    def build(self):
        app = RootWidget()
        return app