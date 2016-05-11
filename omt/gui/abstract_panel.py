from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.spinner import Spinner
from kivy.uix.label import Label


class AbstractPanel(BoxLayout):

    def __init__(self, **kwargs):

        super(AbstractPanel, self).__init__(kwargs=kwargs, orientation='vertical')

        self.panels_to_choose = {}
        self.pannels_instants = []
        self.panel = ScreenManager()

        self.custom_config()
        text, values = self.loadClases()

        self.name_label = Label(text=self.get_name(),size_hint=(1, None), size = (1,44))

        self.spinner = Spinner(
            # default value shown
            text=text,
            # available values
            values=values,
            # just for positioning in our example
            size_hint=(1, None),
            size = (1,44)
        )

        self.spinner.bind(text=self.show_selected_value)

        self.add_widget(self.name_label)
        self.add_widget(self.spinner)
        self.add_widget(self.panel)

    def show_selected_value(self,spinner, text):
        self.panel.current = text

    def custom_config(self):
        pass

    def loadClases(self):
        '''this method use reflection to load the
        different source GUI'''

        package_path_dict = self.packagePath()

        objects_names = self.extract_object(package_path_dict)

        if len(objects_names) > 0:
            name = objects_names[0]
            a_list = objects_names
        else:
            name = 'Nothing'
            a_list = ()

        return name, a_list

    def packagePath(self):
        pass

    def my_import(self,name):
        components = name.split('.')

        mod = __import__(components[0])
        for comp in components[1:]:
            mod = getattr(mod, comp)
        return mod

    def extract_object(self, dictionary):

        obj_names = []
        for key in dictionary:
            path_to_class = dictionary[key]

            class_obj = __import__(path_to_class,fromlist=key)
            obj_names.append(key)
            custom_panel = getattr(class_obj, key)
            self.panels_to_choose[key] = custom_panel
            instat = custom_panel()
            instat.name = key
            self.pannels_instants.append(instat)
            self.panel.add_widget(instat)

        return obj_names

    def get_name(self):
        pass

    def get_configurations(self):
        pass