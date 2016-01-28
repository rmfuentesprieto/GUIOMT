from omt.gui.empty import Vacio


class AbstractSource(Vacio):

    def do_swipe(self):
        return False

    def get_source_config(self):
        pass