from __future__ import annotations

import pygame as pg

from pysgui.styling import StylableMixin


class Widget(StylableMixin):

    def __init__(self, style_name: str = "Widget"):
        super().__init__(style_name)
        self._on_style_change = self._rebuild
        self._rect: pg.Rect = pg.Rect(0, 0, 0, 0)

    def draw(self, surface: pg.Surface, parent_pos: tuple[int, int] = (0, 0)):
        pass

    def handle_event(self, event: pg.Event, parent_pos: tuple[int, int] = (0, 0)) -> bool:
        return False

    @property
    def rect(self):
        return self._rect

    def _rebuild(self):
        pass
