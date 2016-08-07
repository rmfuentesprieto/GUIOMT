from omt.controller.data.memorys.memory import Memory


class RegisterRead(Memory):

    def __init__(self, reg_name):
        self.reg_name = reg_name
        self.value = None

    def does_write(self):
        return False

    def interact_roach(self, fpga):
        self.value = fpga.read_int(self.reg_name)

    def has_acc_len(self):
        return False

    def get_acc_len_reg_name(self):
        return ''

    def get_value_name(self):
        return self.reg_name

    def get_value(self):
        return  self.value

class RegisterWrite(Memory):

    def __init__(self, reg_name, value):
        self.reg_name = reg_name
        self.value = value

    def does_write(self):
        return True

    def interact_roach(self, fpga):
        fpga.write_int(self.reg_name, self.value )

    def has_acc_len(self):
        return False

    def get_acc_len_reg_name(self):
        return ''

    def get_value_name(self):
        return self.reg_name

    def get_value(self):
        return  self.value