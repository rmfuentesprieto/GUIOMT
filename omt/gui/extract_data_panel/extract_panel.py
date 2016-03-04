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

        }

        return altenatives

    def get_name(self):
        return "Obtener Datos"
