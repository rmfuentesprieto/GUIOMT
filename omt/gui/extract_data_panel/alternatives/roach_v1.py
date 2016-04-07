from omt.controller.data.roach_1 import Roach_I_Controller
from omt.gui.extract_data_panel.alternatives.roach import ROACH


class ROACHI(ROACH):

    def get_controller_fpga_insctance(self):
        return Roach_I_Controller