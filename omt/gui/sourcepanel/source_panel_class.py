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
            'AbstractSource':'omt.gui.sourcepanel.alternatives.abstract_source',
            'lll':'omt.gui.sourcepanel.alternatives.ss',
        }

        return altenatives

    def get_name(self):
        return "Fuentes"