from omt.controller.abstract_parallel_proces import Process
import sys, traceback

class ProccesThread(Process):
    dynamic_load_location = 'omt.controller.procesing.dynamic_modules'

    def __init__(self, data_dic):
        self.data_dic = data_dic['LoadDynamic']

        self.passing_variables = {}
        self.big_dic = {}

    def run_execute_functions(self, roach_arguments):



        for key in self.data_dic:

            function_info =  self.data_dic[key]
            if not function_info['function_name_special'] in self.passing_variables:
                self.passing_variables[function_info['function_name_special']] = {}

            roach_arguments['save_data'] = self.passing_variables[function_info['function_name_special']]
            roach_arguments['global_data'] = self.big_dic

            function_module = function_info['module_name']
            function_name = function_info['function_name']

            function_args = {}

            dynamic_module = __import__(ProccesThread.dynamic_load_location +
                                        '.' + function_module , globals(), locals(), [function_name,],-1)
            reload(dynamic_module)
            dynamic_function = getattr(dynamic_module, function_name)
            args = dynamic_function.__code__.co_varnames[:dynamic_function.__code__.co_argcount]

            for possible_arg in args:
                arg_dic = function_info[possible_arg]
                if 'arg_name' in arg_dic:

                    arg_name = arg_dic['arg_name']

                    if arg_dic['from_roach']:
                        function_args[arg_name] = roach_arguments[arg_dic['value']]
                    else:
                        value = arg_dic['value']
                        try:
                            if str(int(value)) == value:
                                value = int(value)
                        except:
                            value = arg_dic['value']

                        try:
                            if str(float(value)) == value:
                                value = float(value)
                        except:
                            value = arg_dic['value']
                        function_args[arg_name] = value
            #try:
            dynamic_function(**function_args)
            #except Exception as e:
                #exc_type, exc_value, exc_traceback = sys.exc_info()
                #info =  traceback.extract_tb(exc_traceback)
                #raise Exception(e.message + '\n in function {} from module {} in line {:d}'.format(
                    #function_name, function_module, info[-1][1]))

