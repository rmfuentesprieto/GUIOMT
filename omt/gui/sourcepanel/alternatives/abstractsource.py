from omt.gui.empty import Empty


class AbstractSource(Empty):

    def do_sweep(self):
        return False

    def get_source_config(self):
        pass

    def save_config_dictionary(self):
        return {}

    def set_configuration(self, config_dictionary):
        raise Exception('Missing implementation')