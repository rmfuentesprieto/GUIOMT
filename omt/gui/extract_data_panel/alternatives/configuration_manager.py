import os
import pickle


class LoadSaveConfig(object):

    def __init__(self, file_path):

        self.file_path = file_path


    def store_dictionary(self, dictionary):

        directory = self.file_path + '/' + dictionary['name']
        if not os.path.exists(directory):
            os.makedirs(directory)

        with open(directory + '/ROACH.pkl', 'wb') as f:
            pickle.dump(dictionary, f, pickle.HIGHEST_PROTOCOL)

    def load_dictionary(self, name):

        directory = name
        with open(directory, 'rb') as f:
            return pickle.load(f)
        return {}

    def copy_bof_to_folder(self,path, name):

        directory = self.file_path + '/' + name
        if not os.path.exists(directory):
            os.makedirs(directory)

        sudoPassword = 'roach'

        command = 'cp %s %s' %(path, os.path.dirname(os.path.realpath(__file__)) + '/roach_configurations/' \
                               + name + '/' + name + '.bof' )
        os.system('echo %s |sudo -S %s' % (sudoPassword, command))
        command = 'chmod 777 %s' % (os.path.dirname(os.path.realpath(__file__)) + '/roach_configurations/' + name + '/' + name + '.bof')
        os.system('echo %s |sudo -S %s' % (sudoPassword, command))

        return os.path.dirname(os.path.realpath(__file__)) + '/roach_configurations/' \
                               + name + '/' + name + '.bof'


