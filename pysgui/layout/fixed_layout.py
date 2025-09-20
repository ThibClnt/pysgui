import pygame as pg

from .layout import Layout
from pysgui.widgets import Widget


class FixedLayout(Layout):
    """
    A layout that does not change the position or size of its children.
    """

    def apply_layout(self, widgets: list[Widget], area: pg.Rect) -> None:
        pass
