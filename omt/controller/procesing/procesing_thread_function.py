from omt.controller.abstract_parallel_proces import Process
import sys, traceback

class ProccesThread(Process):
    dynamic_load_location = 'omt.controller.procesing.dynamic_modules'

    def __init__(self, data_dic):
        self.data_dic = data_dic['LoadDynamic']
        print data_dic

    def run_execute_functions(self, roach_arguments):

        for key in self.data_dic:
            function_info =  self.data_dic[key]

            function_module = function_info['module_name']
            function_name = function_info['function_name']

            function_args = {}
            for possible_arg in function_info:
                arg_dic = function_info[possible_arg]
                if 'arg_name' in arg_dic:
                    arg_name = arg_dic['arg_name']

                    if arg_dic['from_roach']:
                        function_args[arg_name] = roach_arguments[arg_dic['value']]
                    else:
                        function_args[arg_name] = arg_dic['value']

            print function_module, function_name, function_args

            dynamic_module = __import__(ProccesThread.dynamic_load_location + '.' + function_module , globals(), locals(), [function_name,],-1)
            dynamic_function = getattr(dynamic_module, function_name)

            try:
                dynamic_function(**function_args)
            except Exception as e:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                print traceback.extract_tb(exc_traceback)
                raise Exception(e.message + '\n in function %s from module %s' %(function_name,function_module))

