from kivy.uix.popup import Popup

from omt.controller.data.fpga import MissingInformation
from omt.controller.data.roach_1 import Roach_I_Controller
from omt.gui.extract_data_panel.alternatives.roach import ROACH, RoachWarningBox


class ROACHI(ROACH):

    def get_controller_fpga_insctance(self):
        return Roach_I_Controller

    def which_roach(self):
        return 'ROACHI'