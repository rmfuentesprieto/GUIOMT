from omt.gui.abstract_panel import AbstractPanel


class SourcePanel(AbstractPanel):

    def __init__(self):
        super(SourcePanel, self).__init__()

    def packagePath(self):
        """
        This file holds the link to the active panels.
        The structure is a dictionary, the key is the class name
        and the values is where the object is define.
        """
        altenatives = {
            'Agilent':'omt.gui.sourcepanel.alternatives.agilent',
            'RodeSchwartz':'omt.gui.sourcepanel.alternatives.rodeschwartz',
        }

        return altenatives

    def get_name(self):
        return "Fuentes"

    def get_configurations(self):
        return_dic = {'tone':[]}
        for source in self.pannels_instants:
            if source.is_active():
                if source.do_sweep():
                    if 'sweep' in return_dic:
                        raise Exception('Only one sweep')
                    return_dic['sweep'] = source.get_source_config()
                else:
                    return_dic['tone'].append(source.get_source_config())

        return return_dic
