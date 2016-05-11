from omt.controller.abstract_parallel_proces import Process


class BeamScannerController(Process):

    def __init__(self, config_dic):
        self.ip = ''
        self.port = 9988

