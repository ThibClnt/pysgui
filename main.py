import pygame as pg
from pysgui import Application


app = Application("My First PySGUI Application", (0, 0), flags=pg.FULLSCREEN | pg.RESIZABLE)
app.run()
