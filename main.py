import pygame as pg

from pysgui import Application, PopupWindow, Window


app = Application("My First PySGUI Application", (0, 0), flags=pg.FULLSCREEN | pg.RESIZABLE)
app.add_window(PopupWindow(pg.Rect(200, 200, 200, 200), "Window"))
app.run()
