from omt.controller.abstract_parallel_proces import Process


class ProccesThread(Process):

    def __init__(self, data_dic):
        self.data_dic = data_dic

    def run_execute_functions(self, roach_arguments):
        pass