import os
import threading
import types
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
from xml.dom import minidom
from xml.etree.ElementTree import Element, Comment, SubElement, tostring as xmltostring, fromstring as xmlfromstring

from omt.controller.data.roach_2 import BofSelector
from omt.gui.data_processing_panel.alternatives.functions_gui.functiongui import FunctionGui
from omt.gui.empty import Empty
from omt.gui.extract_data_panel.alternatives.BofFileChooser import BofFileChooserIconView


class LoadDynamic(Empty):

    def __init__(self, **kwargs):

        super(LoadDynamic, self).__init__(kwargs=kwargs)

        self.path_modules_and_xml = os.path.dirname(__file__) .replace\
            ('/gui/data_processing_panel/alternatives','/controller/procesing/dynamic_modules')

        self.function_dictionary = self.load_xml()

        self.add_function = Button(text="add new")
        self.add_function.bind(on_press=self.create_function)
        self.import_function = Button(text='import function')
        self.import_function.bind(on_press=self.copy_function)

        top_layot = BoxLayout(orientation='horizontal',  size_hint=(1,None), size=(1,30))
        top_layot.add_widget(self.import_function)
        top_layot.add_widget(self.add_function)

        ####
        self.func_container = GridLayout(cols=1, spacing=0)#row_default_height=30)
        self.func_container.bind(minimum_height=self.func_container.setter('height'))

        scroll_root = ScrollView()
        scroll_root.add_widget(self.func_container)

        ###

        padding_layout = BoxLayout(size_hint=(1,1))
        big_one = BoxLayout(orientation='vertical')
        big_one.add_widget(top_layot)
        big_one.add_widget(scroll_root)
        #big_one.add_widget(padding_layout)

        self.add_widget(big_one)

        self.modules_function_loaded = {}
        self.free_run_variable_dictionary = {}

    def load_xml(self):
        FILE = open(self.path_modules_and_xml + "/setup.xml", 'r')
        modules = xmlfromstring(FILE.read())

        dic_return = {}

        for module in modules._children:
            module_name = module.attrib['name']
            module_dict = {}
            for functions in module._children:
                function_name = functions.attrib['name']
                args_name = []
                for args in functions._children:
                    args_name.append(args.attrib['name'])
                module_dict[function_name] = args_name
            dic_return[module_name] = module_dict

        return dic_return

    def create_function(self, instance):
        function_list = self.get_function_list()
        threading.Thread(target=self.create_function_thread, args=(function_list,)).start()

    def create_function_thread(self, function_list):
        content = FunctionSelector( function_list)

        a_popup = Popup(title='Choose Bof', auto_dismiss=False, content=content, size_hint=(None, None), size=(400,400))
        content.set_popup(a_popup)
        a_popup.open()

        while content.continues:
            pass

        keys = content.choosen_name.split('.')
        if content.is_default():
            return

        new_widget = FunctionGui( keys[0],keys[1],self.function_dictionary[keys[0]][keys[1]], self.delete_one_function)
        new_widget.update_free_run_dictionary(self.free_run_variable_dictionary)

        self.func_container.add_widget(new_widget)

        if not new_widget.module_name in self.modules_function_loaded:
            self.modules_function_loaded[new_widget.module_name] = {}

        self.modules_function_loaded[new_widget.module_name][new_widget.function_name + new_widget.special_name] = new_widget
        #self.func_container.add_widget(Button(text=content.choosen_name + ' ' + str(self.function_dictionary[keys[0]][keys[1]]),size_hint=(1,None), size=(1,30)))

    def delete_one_function(self, module_name, function_name):
        print self.modules_function_loaded

        module_dic = self.modules_function_loaded[module_name]
        del_function = module_dic[function_name]
        del module_dic[function_name]

        self.func_container.remove_widget(del_function)

        print self.modules_function_loaded

    def get_function_list(self):
        function_list_return = []

        for module in self.function_dictionary:
            module_dic = self.function_dictionary[module]

            for function in module_dic:
                function_list_return.append(module + '.' + function)

        return function_list_return

    def copy_function(self, instance):
        content = BofFileChooserIconView(return_selection_path=self.copy_function_copy_file )
        a_popup = Popup(title='Choose Bof', auto_dismiss=False, content=content, size_hint=(None, None), size=(400,400))
        content.set_popup(a_popup)
        a_popup.open()

    def copy_function_copy_file(self, path):
        path = path[0]
        module_name = path.split("/")[-1]
        module_name = str(module_name.replace('.py',''))
        print 'name',module_name, type(module_name)

        command = "cp %s %s" %(path, self.path_modules_and_xml)

        print command
        os.system(command)

        dynamic_module = __import__('omt.controller.procesing.dynamic_modules' , globals(), locals(), [module_name,],-1)
        dynamic_module = getattr(dynamic_module, module_name)
        posible_fucntion_list = dir(dynamic_module)

        actual_functions = []
        #extract the created function
        for a_funtion in posible_fucntion_list:
            function_aux = getattr(dynamic_module,a_funtion)
            if types.FunctionType == type(function_aux) and a_funtion.replace('__','',1) == a_funtion:
                actual_functions.append(a_funtion)

        print actual_functions

        module_function_list = {}
        for a_function in actual_functions:

            funct_reference = getattr(dynamic_module, a_function)
            #function_dic['args_name'] = funct_reference.__code__.co_varnames
            module_function_list[a_function] = funct_reference.__code__.co_varnames[:funct_reference.__code__.co_argcount]
            #module_function_list[a_function + "_instance"] = funct_reference

        if not module_name in self.function_dictionary:
            print 'add info to dic'
            self.function_dictionary[module_name] = module_function_list
        else:
            Popup(title='Module Error', content=Label(text="Repeated module name,\nplease change yours")\
                  , size_hint=(None, None), size=(200,200)).open()
            return

        print self.function_dictionary

        self.save_xml()

    def save_xml(self, ):
        module_dict_xml = Element('dynamic_modules')
        comment = Comment('Modules info')
        module_dict_xml.append(comment)

        for aKey in self.function_dictionary:
            module_dic = self.function_dictionary[aKey]

            module_xml = SubElement(module_dict_xml,'module',attrib={'name':aKey})

            for aFunctionKey in module_dic:
                aFunction = module_dic[aFunctionKey]
                function_xml = SubElement(module_xml,'function', name=aFunctionKey)

                for args in aFunction:
                    arg_xml = SubElement(function_xml,'arg', name=args)

        rough_string = xmltostring(module_dict_xml, 'utf-8')
        reparsed = minidom.parseString(rough_string)

        string_xml = reparsed.toprettyxml(indent="  ")

        FILE = open(self.path_modules_and_xml + "/setup.xml", "w")
        FILE.write(string_xml)
        FILE.close()

    def update_free_run_dictionary(self, data_dic):
        self.free_run_variable_dictionary = data_dic
        for m_key in self.modules_function_loaded:
            module_dic = self.modules_function_loaded[m_key]
            for f_key in module_dic:
                function = module_dic[f_key]
                function.update_free_run_dictionary(data_dic)

    def get_source_config(self):
        return_dic = {}
        for element in self.modules_function_loaded:
            module = self.modules_function_loaded[element]
            for key in module:
                widget = module[key]
                return_dic[widget.special_name] = widget.get_source_config()
        return return_dic

class FunctionSelector(BoxLayout):

    def __init__(self, value_):
        super(FunctionSelector, self).__init__(orientation='vertical', size_hint=(1,1))
        print 'hi'
        top_padding = BoxLayout(size_hint=(1,1))
        self.default = "choose one"
        self.bof_spinner = Spinner(text=self.default, values=value_, size_hint=(1,None), size=(1,30))
        bottom_padding = BoxLayout(size_hint=(1,1))
        ok_button = Button(text='Ok',  size_hint=(1,0.2))
        ok_button.bind(on_press=self.selection_made)

        self.add_widget(top_padding)
        self.add_widget(self.bof_spinner)
        self.add_widget(bottom_padding)
        self.add_widget(ok_button)

        self.choosen_name = ''
        self.popup = None

        self.continues = True

    def set_popup(self, popup_):
        self.popup = popup_

    def selection_made(self, instance):
        self.choosen_name = self.bof_spinner.text
        self.popup.dismiss()
        self.continues = False

    def is_default(self):
        return self.choosen_name == self.default
