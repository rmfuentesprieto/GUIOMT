from omt.controller.data.roach_2 import Roach_II_Controller
from omt.gui.extract_data_panel.alternatives.roach import ROACH


class ROACHII(ROACH):

    def get_controller_fpga_insctance(self):
        return Roach_II_Controller
