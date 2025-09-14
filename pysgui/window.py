import pygame as pg
from typing import Iterable


class Window:

    def __init__(self, name: str = "Window", rect: pg.Rect = None, fullscreen: bool = False, visible: bool = True):
        self.name = name
        self._rect: pg.Rect = rect if rect else pg.Rect(0, 0, 0, 0)
        self._fullscreen = fullscreen
        self.visible = visible

    def add_widget(self, widget):
        pass

    def draw(self, surface: pg.Surface):
        pass

    def handle_events(self, events: Iterable[pg.event.Event]):
        pass

    @property
    def fullscreen(self):
        return self._fullscreen

    @property
    def rect(self):
        return self._rect

    def resize(self, size: tuple[int, int]):
        pass

    def update(self, dt: float):
        pass
