import threading


class Process(threading.Thread):

    def __init__(self, init_monitor, end_monitor):
        
        super(Process, self).__init__()
        self.initialize_monitor = init_monitor
        self.end_monitor = end_monitor

    def get_next_iteraration_initializer_monitor(self):
        return self.initialize_monitor

    def get_end_iteration_alert_monitor(self):
        return self.end_monitor

    def close_process(self):
        pass
