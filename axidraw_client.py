import socket
import numpy as np


def path_to_str(P):
    ''' Convert a path to a (num_points, point sequence) tuple
        if P is a numpy array, it assumes points are columns on a 2xN matrix'''
    if type(P) == np.ndarray:
        P = P.T
    return len(P), ' '.join(['%f %f'%(p[0], p[1]) for p in P])


class AxiDrawClient:
    def __init__(self, address='localhost', port=9999):
        self.address = address
        self.port = port
        self.socket_open = False
        #self.open(address, port)

    def open(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (self.address, self.port)
        print('connecting to %s port %s'%server_address)
        self.sock.connect(server_address)
        self.socket_open = True

    def close(self):
        self.sock.close()
        self.socket_open = False

    def send(self, msg):
        auto_open = False
        if not self.socket_open:
            self.open()
            auto_open = True
        self.sock.sendall(msg.encode('utf-8'))
        if auto_open:
            self.close()

    def sendln(self, msg):
        self.send(msg + '\n')

    def drawing_start(self):
        self.open()
        self.sendln('PATHCMD drawing_start')
    
    def drawing_end(self, raw=False):
        if raw:
            self.drawing_end_raw()
            return

        self.sendln('PATHCMD drawing_end')
        self.close()

    def drawing_end_raw(self):
        self.sendln('PATHCMD drawing_end_raw')
        self.close()


    def draw_paths(self, S, raw=False):
        self.drawing_start()
        for P in S:
            self.add_path(P)
        self.drawing_end(raw)

    def add_path(self, P):
        self.sendln('PATHCMD stroke %d %s'%path_to_str(P))

    def pen_up(self):
        self.sendln('PATHCMD pen_up')

    def pen_down(self):
        self.sendln('PATHCMD pen_down')

    def home(self):
        self.sendln('PATHCMD home')