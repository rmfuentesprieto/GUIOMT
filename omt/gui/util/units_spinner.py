from kivy.uix.spinner import Spinner


class UnitSpinner(Spinner):

    hz = 'hz'
    db = 'dB'
    simple = 'simple'

    def __init__(self, units):

        units_dict = {}

        if units == 'hz':
            units_dict = {'Hz' : 1, 'KHz' : 10**3, 'MHz' : 10**6, 'GHz' : 10**9, 'THz' : 10**12}
        elif units == 'dB':
            units_dict = {'dBm': 'algo', 'dB':'nop'}
        elif units == 'simple':
            units_dict = {' ' : 1, 'K' : 10**3, 'M' : 10**6, 'G' : 10**9, 'T' : 10**12}
        values = units_dict.keys()

        super(UnitSpinner, self).__init__(text=values[0], values=values, size_hint=(None, None), size = (35,44))