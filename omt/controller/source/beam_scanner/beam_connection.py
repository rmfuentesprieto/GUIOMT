import socket

import time


class BeamConnection(object):

    def __init__(self, ip, port):

        self.address = (ip,port)
        self.connectionSocket = None

    def start_connection(self, command_id):
        self.connectionSocket = s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connectionSocket.connect(self.address)

        self.connectionSocket.sendall(command_id)
        txt_return = self.recieve_data()
        print txt_return
        if not txt_return == 'ok':
            raise Exception('fail to connect')

    def close_connection(self):
        self.send_command('close_all')
        self.connectionSocket.close()

    def send_command(self, command):
        send_bit = 0
        print command
        command += '\n'
        try:
            while 1:
                send_now = self.connectionSocket.send(command[send_bit:])
                send_bit += send_now

                if send_bit == len(command):
                    return True
        except Exception as e:
            print e.message

        return False

    def recieve_data(self):
        msg = ''
        try:
            while 1:
                line = self.connectionSocket.recv(2048)
                msg += line
                if '\n' in msg:
                    return msg[0:len(msg)-5]
                if len(line) == 0:
                    break
        except:
            raise
        return False
