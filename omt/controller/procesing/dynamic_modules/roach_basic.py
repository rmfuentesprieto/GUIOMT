from cmath import phase


def extract_data_sweep(save_dic, current_channel, initial_spec, step, spectrum):
    spectrum = spectrum[0]
    function_name = 'extract_data_sweep'
    if current_channel == 0:
        save_dic[function_name] = [spectrum[initial_spec]]
        return

    channel = initial_spec + current_channel*step

    if channel >= len(spectrum):
        raise Exception('Asking for a channel thats out of possible range.')

    save_dic[function_name].append(spectrum[channel])

def fase_difference_amplitudes(save_dic, current_channel, initial_spec, step, spectrum, spectrum_ref):
    spectrum = spectrum[0]
    spectrum_ref = spectrum_ref[0]
    function_name = 'fase_difference_amplitudes'
    if current_channel == 0:
        a1 = abs(spectrum[initial_spec])
        a2 = abs(spectrum_ref[initial_spec])
        angle = phase(a1*a2.conjugate())

        save_dic[function_name] = [(a1,a2,angle)]
        return

    channel = initial_spec + current_channel*step

    if channel >= len(spectrum):
        raise Exception('Asking for a channel thats out of possible range.')

    channel = initial_spec + current_channel*step

    a1 = abs(spectrum[channel])
    a2 = abs(spectrum_ref[channel])
    angle = phase(a1*a2.conjugate())

    save_dic[function_name].append((a1,a2,angle))

def fase_difference_amplitudes_ratio(save_dic, current_channel, initial_spec, step, spectrum, spectrum_ref):
    spectrum = spectrum[0]
    spectrum_ref = spectrum_ref[0]
    function_name = 'fase_difference_amplitudes'
    if current_channel == 0:
        a1 = abs(spectrum[initial_spec])
        a2 = abs(spectrum_ref[initial_spec])
        ratio = 0 if a2==0 else a1/a2
        angle = phase(a1*a2.conjugate())

        save_dic[function_name] = [(ratio,angle)]
        return

    channel = initial_spec + current_channel*step

    if channel >= len(spectrum):
        raise Exception('Asking for a channel thats out of possible range.')

    channel = initial_spec + current_channel*step

    a1 = abs(spectrum[initial_spec])
    a2 = abs(spectrum_ref[initial_spec])
    ratio = 0 if a2==0 else a1/a2
    angle = phase(a1*a2.conjugate())

    save_dic[function_name].append((ratio,angle))