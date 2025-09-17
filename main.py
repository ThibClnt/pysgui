import pygame as pg

from pysgui import Application, PopupWindow, Window

app = Application("My First PySGUI Application", (600, 600), flags=pg.RESIZABLE)
app.add_window(Window())

popup = PopupWindow(pg.Rect(50, 50, 200, 200), "Popup 1")
popup.style = popup.style.clone(background_color=(200, 100, 100))
app.add_window(popup)
app.add_window(PopupWindow(pg.Rect(200, 200, 200, 200), "Popup 2"))
app.run()
