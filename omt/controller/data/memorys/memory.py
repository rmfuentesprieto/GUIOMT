
class Memory(object):

    def does_write(self):
        return False

    def interact_roach(self, fpga):
        pass

    def has_acc_len(self):
        return False

    def get_acc_len_reg_name(self):
        return ''

    def get_value_name(self):
        pass

    def get_value(self):
        pass

    def set_acc_count(self, count):
        pass