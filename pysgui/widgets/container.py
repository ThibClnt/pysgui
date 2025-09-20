import pygame as pg

from .widget import Widget
from pysgui.layout import FixedLayout, Layout
from pysgui.util import Constraints


class Container(Widget):

    def __init__(self, layout: Layout = FixedLayout, pos: tuple[int, int] | None = None, size: tuple[int, int] = None,
                 constraints: Constraints | None = None, style_name: str = "Container"):
        super().__init__(pos, size, constraints, style_name)

        self._children: list[Widget] = []
        self._layout = layout

        def on_size_change(_1: tuple[int, int], _2: tuple[int, int]):
            self.apply_layout()
            self.rebuild()

        self._on_size_change = on_size_change
        self._on_style_change = self.rebuild

        self.apply_layout()

    def add(self, widget: Widget) -> Widget:
        """
        Add a widget to the container.
        :param widget: widget to add.
        :return: the added widget.
        """
        self._children.append(widget)
        self.apply_layout()
        return widget

    def apply_layout(self):
        self._layout.apply_layout(self._children, self._rect)

    @property
    def children(self):
        return self._children

    def draw(self, surface: pg.Surface, parent_pos: tuple[int, int] = (0, 0)):
        x = self.rect.x + parent_pos[0]
        y = self.rect.y + parent_pos[1]

        for widget in self._children:
            widget.draw(surface, (x, y))

    def handle_event(self, event: pg.Event) -> bool:
        if event.pos:
            event.pos = (event.pos[0] - self._rect.x, event.pos[1] - self._rect.y)

        handled = False
        for widget in self._children:
            handled = handled or widget.handle_event(event)

        return handled

    @property
    def layout(self):
        return self._layout

    @layout.setter
    def layout(self, value: Layout):
        self._layout = value
        self.apply_layout()

    def set_geometry(self, rect: pg.Rect):
        super().set_geometry(rect)
        self.apply_layout()
