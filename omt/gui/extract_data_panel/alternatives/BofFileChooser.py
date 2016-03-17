from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserIconView


class BofFileChooserIconView(App):

    def __init__(self,return_selection_path):
        super(BofFileChooserIconView, self).__init__()
        self.return_to = return_selection_path

    def build(self):
        base = BoxLayout(orientation='vertical')
        self.fc = FileChooserIconView(title="Choose Bof")

        ok_button = Button(text='Ok',  size_hint=(1,None),size=(100,40))
        ok_button.bind(on_press=self.pree_m)

        base.add_widget(self.fc)
        base.add_widget(ok_button)

        return base

    def pree_m(self, instance):
        self.return_to(self.fc.selection)
        self.stop()
        
    def run(self, instance):
        super(BofFileChooserIconView, self).run()