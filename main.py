import pygame as pg

from pysgui import Application, PopupWindow, Window

app = Application("My First PySGUI Application", (600, 600), flags=pg.RESIZABLE)
app.add_window(Window())
app.add_window(PopupWindow(pg.Rect(200, 200, 200, 200), "Window"))
app.run()
