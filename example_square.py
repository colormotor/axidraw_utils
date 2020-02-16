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

square = np.array([[0.0, 0.0], [1.0, 0.0], [1.0,1.0], [0.,1.0]]).T
S = [square]
close = True
#######################################
# Send to axidraw
# Comment this block out to just plot the output
server_addr = 'localhost'

client = AxiDrawClient(address=server_addr, port=80)
# Simple send a list of paths and close connection
client.draw_paths(S, title='TEST', close=close) #'d=%.2f da=%.2f db=%.2f'%(delta, da, db))


# Alternative, send paths and block until all paths have been drawn
# This can be useful for external interactions with the plotter
# client.draw_paths(S, title='TEST', close=False) #'d=%.2f da=%.2f db=%.2f'%(delta, da, db))
# res = client.wait()
# print('done plotting')
# client.close()

#######################################

# plot figure
plt.figure(figsize=(5,5))
for P in S:
    plt.plot(P[0,:], P[1,:], 'k', linewidth=0.5)
plt.axis('equal')
plt.axis('off')
plt.gca().invert_yaxis()
plt.show()





# %%
