from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserIconView, FileChooserListView


class BofFileChooserIconView(BoxLayout):

    def __init__(self,return_selection_path, path=None, filter=[]):
        super(BofFileChooserIconView, self).__init__(orientation='vertical', size_hint=(1,1))
        self.return_to = return_selection_path
        self.popup = None

        self.fc = FileChooserListView(title="Choose Bof",size_hint=(1,0.8),rootpath=path, filter=filter)

        ok_button = Button(text='Ok',  size_hint=(1,0.2))
        ok_button.bind(on_press=self.pree_m)


        self.add_widget(self.fc)
        self.add_widget(ok_button)

    def pree_m(self, instance):
        if len(self.fc.selection) > 0:
            self.return_to(self.fc.selection[0])
        self.popup.dismiss()

    def run(self, instance):
        super(BofFileChooserIconView, self).run()

    def set_popup(self,popup):
        self.popup = popup
