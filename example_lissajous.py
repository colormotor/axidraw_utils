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
from axidraw_client import AxiDrawClient


def lissajous(t, a, b, omega, delta):
    return np.vstack([a*np.cos(omega*t + delta),
                      b*np.sin(t)])

def lissajous_glyph():
    n = 200
    S = []
    
    t = np.linspace(0, np.pi*3.8, n)

    delta = np.random.uniform(-np.pi/2, np.pi/2)
    da = np.random.uniform(-np.pi/2, np.pi/2)
    db = np.random.uniform(-np.pi/2, np.pi/2)
    omega = 2.
    for o in np.linspace(0, 0.2, 5):
        a = np.sin(np.linspace(0, np.pi*2, n) + da + o*0.5)*100
        b = np.cos(np.linspace(0, np.pi*2, n) + db + o*1.0)*100  
        P = lissajous(t, a,
                         b,
                         omega,
                         delta)
        S.append(P)
    return S, delta, da, db

client = AxiDrawClient(address='localhost', port=9999)

# Generate
S, delta, da, db = lissajous_glyph()

# Send to axidraw
client.draw_paths(S, title='d=%.2f da=%.2f db=%.2f'%(delta, da, db))

# plot figure
plt.figure(figsize=(5,5))
for P in S:
    plt.plot(P[0,:], P[1,:], 'k', linewidth=0.5)
plt.axis('equal')
plt.axis('off')
plt.gca().invert_yaxis()
plt.show()





