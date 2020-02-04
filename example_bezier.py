#%%
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 23 00:22:09 2019
Simple bezier curve example
@author: Daniel Berio
"""

import numpy as np
import matplotlib.pyplot as plt
from axidraw_client import AxiDrawClient


# Alternative version
# def cubic_bezier(t, P):
#     X = (1.0-t)**3 * P[0] + 3*(1.0-t)**2 * t * P[1] + 3*(1.0-t)* t**2 * P[2] + t**3 * P[3]
#     return X

def cubic_bezier(t, P):
    B = np.vstack([(1.0-t)**3, 
                    3*(1.0-t)**2 * t,
                    3*(1.0-t)* t**2,
                    t**3])
    return P @ B


S = []
# Draw many random cubic bezier segments
for i in range(140):
    P = np.random.normal(size=(2,4))
    t = np.linspace(0, 1, 200)
    X = cubic_bezier(t, P) #np.vstack([bezier(t, P[0,:]), bezier(t, P[1,:])])
    S.append(X)

# Send to axidraw
#client = AxiDrawClient(address='localhost', port=9999)
#client.draw_paths(S, title='d=%.2f da=%.2f db=%.2f'%(delta, da, db))

# plot figure
plt.figure(figsize=(10,10))
for X in S:
    plt.plot(X[0,:], X[1,:], linewidth=0.5)
plt.axis('equal')
plt.axis('off')
plt.gca().invert_yaxis()
plt.show()







# %%
