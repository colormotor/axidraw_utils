# AxiDraw TCP/IP client and server

Utilties for setting up a TCP/IP connection with the AxiDraw V3 plotter.

## Installation requirements
Requires installing the [Axi](https://github.com/fogleman/axi) Python package, by Michael Fogleman, used to control the plotter. Clone the repository and follow instructions to install.

## Server
The server code is in Python and is a slightly modified version of [this one](https://lurkertech.com/axiserver/) developed by Chris Pirazzi and Paul Haeberli. The code here provides addition options for plotting a title to each plot, and support for command line options.

To start the server run the python script from the command line
```
python axidraw_server.py
```
The server defaults to port 80, but you can set that with other paramters when running the script
```
python axidraw_server.py --port=7777
```

#### Page size and subdivision
By default the server fits the paths sent to it within a default work area of 8 inches square. The size of the work area can be varied by using a paramter `--size`, e.g. 
```
python axidraw_server.py --size=9
```
changes the work area to 9x9 inches.

The area can be subdivided into a grid, so each new path, or list of paths, is sequentially added to a cell of the grid.
To change the subdivision use `--nx` and `--ny`, e.g.
```
python axidraw_server.py --nx=3 --ny=4
```
Creates a 3X4 grid

## Clients
The repository contains two simple clients, one for Python 3 and one for Matlab (probably Octave also but haven't tested it yet). The clients are easy to use and brief usage examples are given in the example files.

#### Matlab interface
Matlab integration relies on the function `axi` defined in `axi.m`.
The syntax is 
```
axi(command_str, data, port, address)
```
where port is the port number on which the server is running, and address is the server IP address (use `'127.0.0.1'` if the server is running on the same machine).
Port and address default to `80` and `'127.0.0.1'` (localhost) respectively.
These will be omitted in the next examples.

```
axi('draw', S)
```
Draws a list of paths contained in S, with each path of N defined as a 2xN matrix.
Note that the server, will rescale the drawing to fit the specified work area size or subdivision, which is handy if one does not want to worry about the coordinate system in which the drawing is being generated. This can be overridden, by using
```
axi('draw_raw', S)
```
In which case the coordinates must be specified in inches.
```
axi('title', 'my title')
```
Draws a title string ("my title") in the bottom left of the work area.


#### Python, sending paths to AxiDraw.
Python integration relies on the the class ```AxiDrawClient``` defined in ```axidraw_client.py```

Initialize the client, for example with, 
```
client = AxiDrawClient(address='127.0.0.1', port=80)
```
to run the client on port 80 and localhost.


```
client.draw_paths(S, title='TEST') 
```

Draws a list `S` of paths, with each path of N defined as a 2xN numpy array or a Nx2 list. Note that the server, will rescale the drawing to fit the specified work area size or subdivision, which is handy if one does not want to worry about the coordinate system in which the drawing is being generated. This can be overridden, by setting the `raw=True` flag
```
client.draw_paths(S, raw=True, title='TEST') 
```
In which case the coordinates must be specified in inches.

Note that currently this requires [Numpy](https://numpy.org) to be installed.


