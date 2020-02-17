import socket, sys
import numpy as np
import time

def path_to_str(P):
    ''' Convert a path to a (num_points, point sequence) tuple
        if P is a numpy array, it assumes points are columns on a 2xN matrix'''
    if type(P) == np.ndarray:
        P = P.T
    return len(P), ' '.join(['%f %f'%(p[0], p[1]) for p in P])

def recv_line(sock):
    s = ''
    while True:
        off = s.find("\n")
        if -1 != off: break
        #print("reading more from connection")
        buf = sock.recv(1024)
        if not buf: return ''
        if buf[0] == 0xff: return ''
        if buf == '': return ''
        buf = buf.decode("utf-8")   
        s += buf
    ret = s[0:off]
    ret = ret.rstrip()
    print('received ' + ret)
    return ret


class AxiDrawClient:
    def __init__(self, address='localhost', port=9999): #, blocking=False):
        self.address = address
        self.port = port
        self.socket_open = False
        #self.blocking = blocking

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


    def drawing_start(self, title=''):
        self.open()
        if title:
            self.sendln('PATHCMD title ' + title)
        self.sendln('PATHCMD drawing_start')


    def drawing_end(self, raw=False, close=False):
        if raw:
            self.drawing_end_raw()
            return

        self.sendln('PATHCMD drawing_end')
        if close:
            self.close()


    def drawing_end_raw(self):
        self.sendln('PATHCMD drawing_end_raw')
        self.close()

    def draw_paths(self, S, raw=False, title='', close=False):
        try:
            self.drawing_start(title)
            for P in S:
                self.add_path(P)
            self.drawing_end(raw, close)
            
        except ConnectionRefusedError as e: 
            print('could not connect to network')
            print(e)

    def drawing(self, drawing, raw=False, title=''):
        try:
            self.drawing_start(title)
            for P in drawing.paths:
                self.add_path(P)
            self.drawing_end(raw)
        except ConnectionRefusedError as e: 
            print('could not connect to network')
            print(e)
            
    def visualize_drawing(self, drawing, title='', close=False, figsize=(7,7), axis=False):
        import matplotlib.pyplot as plt
        plt.figure(figsize=figsize)
        if title:
            plt.title(title)
        for P in drawing.paths:
            plt.plot([p[0] for p in P],
                     [p[1] for p in P], 'k', linewidth=0.5)
        plt.axis('equal')
        if not axis:
            plt.axis('off')
        plt.gca().invert_yaxis()
        plt.show()

    def visualize_paths(self, S, title='', close=False, figsize=(7,7), axis=False):
        import matplotlib.pyplot as plt
        plt.figure(figsize=figsize)
        if title:
            plt.title(title)
        if type(S) != list:
            S = [S]
        for P in S:
            if type(P) == np.ndarray:
                P = list(P.T)
            if close:
                P = P + [P[0]]
            plt.plot([p[0] for p in P],
                     [p[1] for p in P], 'k', linewidth=0.5)
        plt.axis('equal')
        if not axis:
            plt.axis('off')
        plt.gca().invert_yaxis()
        plt.show()

    def wait(self):
        print('waiting')
        self.sendln('wait')
        rep = recv_line(self.sock)
        if rep == 'done':
            print('Finished waiting')
            return True
        return False

    def add_path(self, P):
        self.sendln('PATHCMD stroke %d %s'%path_to_str(P))


    def pen_up(self):
        self.sendln('PATHCMD pen_up')


    def pen_down(self):
        self.sendln('PATHCMD pen_down')


    def home(self):
        self.sendln('PATHCMD home')
