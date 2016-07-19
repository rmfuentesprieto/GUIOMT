from omt.gui.sourcepanel.alternatives.tipical_source import CommonSource


class RodeSchwartz(CommonSource):

    def get_my_ip(self):
        return '192.168.1.33'

    def get_my_port(self):
        return '5025'

    def get_my_name(self):
        return 'RodeSchwartz'