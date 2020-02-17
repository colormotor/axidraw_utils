#%%
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 23 00:22:09 2019
Generating simple calligraphic like glyphs with Lissajous curves
@author: Daniel Berio
"""

import numpy as np
import matplotlib.pyplot as plt
from importlib import reload
import axidraw_client
reload(axidraw_client)

from axidraw_client import AxiDrawClient


def lissajous(t, a, b, omega, delta):
    return np.vstack([a*np.cos(omega*t + delta),
                      b*np.sin(t)])

def lissajous_glyph():
    n = 200
    S = []
    
    #t = np.linspace(0, np.pi*3.8, n)
    t = np.linspace(0, np.pi*3.8, n)

    delta = np.random.uniform(-np.pi/2, np.pi/2)
    da = np.random.uniform(-np.pi/2, np.pi/2)
    db = np.random.uniform(-np.pi/2, np.pi/2)
    omega = 2.
    for o in np.linspace(0, 0.2, 2):
        a = np.sin(np.linspace(0, np.pi*2, n) + da + o*0.5)*100
        b = np.cos(np.linspace(0, np.pi*2, n) + db + o*1.0)*100  
        P = lissajous(t, a,
                         b,
                         omega,
                         delta)
        S.append(P)
    return S, delta, da, db


# Generate
S, delta, da, db = lissajous_glyph()

#######################################
# Send to axidraw
# Comment this block out to just plot the output
server_addr = '192.168.153.23'
server_addr = 'localhost'

client = AxiDrawClient(address=server_addr, port=80)
# Simple send a list of paths and close connection
client.draw_paths(S, title='TEST') #'d=%.2f da=%.2f db=%.2f'%(delta, da, db))

# Use the following to draw a set of paths with matplotlib
client.visualize_paths(S, title='TEST')






# %%
