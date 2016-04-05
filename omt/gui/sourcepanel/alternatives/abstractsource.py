from omt.gui.empty import Empty


class AbstractSource(Empty):

    def do_swipe(self):
        return False

    def get_source_config(self):
        pass

    def save_config_dictionary(self):
        pass