from omt.gui.abstract_panel import AbstractPanel


class ExtractPanel(AbstractPanel):

    def __init__(self):
        super(ExtractPanel, self).__init__()

    def packagePath(self):
        """
        This file holds the link to the active panels.
        The structure is a dictionary, the key is the class name
        and the values is where the object is define.
        """
        altenatives = {
            'ROACHI':'omt.gui.extract_data_panel.alternatives.roach_v1',
            'ROACHII':'omt.gui.extract_data_panel.alternatives.roach_v2',
        }

        return altenatives

    def get_name(self):
        return "Extract Data"

    def get_configurations(self):
        return_dic = {}
        for roach_config in self.pannels_instants:
            print roach_config.name
            if roach_config.name == self.spinner.text:
                print roach_config.name, 'yes'
                return_dic['roach'] = roach_config.get_source_config()

        return return_dic


    def pass_source(self, sources):
        for data in self.pannels_instants:
            data.pass_source(sources)

    def activate_extract(self,f):
        for data in self.pannels_instants:
            data.activate_extract(f)
