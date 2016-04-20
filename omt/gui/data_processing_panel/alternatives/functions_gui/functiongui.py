
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput


class FunctionGui(BoxLayout):

    def __init__(self, module_name, function_name, args_name,export_names):
        super(FunctionGui, self).__init__(orientation='vertical',size_hint=(1,None), size = (1, 30*(1+len(args_name))))
        self.hight_component = 30
        self.module_name = module_name
        self.function_name = function_name

        name_label = Label(text=module_name + '-' + function_name, size_hint=(1,None), size=(1,self.hight_component))
        self.delte_button = Button(text='-', size_hint=(None,None), size=(self.hight_component,self.hight_component))

        title_layot = BoxLayout(orientation='horizontal', size_hint=(1,None), size=(1,self.hight_component))
        title_layot.add_widget(name_label)
        title_layot.add_widget(self.delte_button)

        self.args_layouts = []

        for arg in args_name:
            self.args_layouts.append(ArgsGUI(arg, export_names))



        self.add_widget(title_layot)
        for arg_l in self.args_layouts:
            self.add_widget(arg_l)

    def get_config(self):
        return_dic = {}

        return_dic['module_name'] = self.module_name
        return_dic['function_name'] = self.function_name

        for arg in self.args_layouts:
            return_dic[arg.arg_name] = arg.get_config()

        return  return_dic


class ArgsGUI(BoxLayout):

    def __init__(self, arg, export_names):
        self.hight_component = 30
        super(ArgsGUI, self).__init__(orientation='horizontal', size_hint=(1,None), size=(1,self.hight_component))

        self.arg_name = arg
        arg_name = Label(text=arg,size_hint=(0.4,None), size=(1,self.hight_component))

        self.spinner_options = ('from roach', 'free input')
        self.arg_type = Spinner(
                # default value shown
                text=self.spinner_options[0],
                # available values
                values=self.spinner_options,
                # just for positioning in our example
                size_hint=(0.3, None),
                size = (1,self.hight_component)
            )
        self.arg_type.bind(text=self.change_input)


        self.arg_roach_spinner = Spinner(
                # default value shown
                text=export_names[0],
                # available values
                values=export_names,
                # just for positioning in our example
                size_hint=(0.4, None),
                size = (1,self.hight_component)
            )
        self.roach_input = True
        self.free_input = TextInput(size_hint=(0.4,None), size=(1,self.hight_component))

        self.add_widget(arg_name)
        self.add_widget(self.arg_type)
        self.add_widget(self.arg_roach_spinner)

    def change_input(self,instance, text):

        if self.spinner_options[0] == text and self.roach_input or self.spinner_options[1] == text and not self.roach_input:
            print 'nope'
            return
        if self.spinner_options[1] == text and self.roach_input:# delete roach input and put free
            self.remove_widget(self.arg_roach_spinner)
            self.add_widget(self.free_input)
            self.roach_input = False
            print 'lol'
        if self.spinner_options[0] == text and not self.roach_input:
            self.remove_widget(self.free_input)
            self.add_widget(self.arg_roach_spinner)
            self.roach_input = True
            print 'jaja'

    def get_config(self):
        return_dic = {}

        return_dic['arg_name'] = self.arg_name
        return_dic['from_roach'] = self.roach_input

        if self.roach_input:
            return_dic['value'] = self.arg_roach_spinner.text
        else:
            return_dic['value'] = self.free_input.text

        return return_dic

