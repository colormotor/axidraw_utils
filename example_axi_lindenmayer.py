#%%
# Code from  the axi (https://github.com/fogleman/axi) example  by Michael Fogleman
import axi
from axidraw_client import AxiDrawClient

def main():
    system = axi.LSystem({
        'A': 'A-B--B+A++AA+B-',
        'B': '+A-BB--B-A++A+B',
    })
    d = system.run('A', 3, 60)
    # system = axi.LSystem({
    #     'X': 'F-[[X]+X]+F[+FX]-X',
    #     'F': 'FF',
    # })
    # d = system.run('X', 6, 20)
    d = d.rotate_and_scale_to_fit(12, 8.5, step=90)
    # d = d.sort_paths()
    # d = d.join_paths(0.015)

    # NB: The following needs Cairo to work
    # d.render(bounds=axi.V3_BOUNDS).write_to_png('out.png')

    client = AxiDrawClient(address='localhost', port=80)
    # Comment the following if plotter is disconnected
    client.drawing(d)
    
    client.visualize_drawing(d, title='TEST')
    
if __name__ == '__main__':
    main()


# %%
