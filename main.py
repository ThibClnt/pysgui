import pygame as pg

from pysgui import Application, PopupWindow

app = Application("My First PySGUI Application", (600, 600), flags=pg.RESIZABLE)

popup = app.add_window(PopupWindow(pg.Rect(50, 50, 200, 200), "Popup 1"))
popup_2 = app.add_window(PopupWindow(pg.Rect(200, 200, 200, 200), "Popup 2"))

popup.style = popup.style.clone(background_color=(200, 100, 100))
app.windows_manager.bring_to_front(popup_2)

app.run()
