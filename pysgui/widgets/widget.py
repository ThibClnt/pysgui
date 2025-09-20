from __future__ import annotations

from typing import Callable

import pygame as pg

from pysgui.styling import StylableMixin
from pysgui.util import Constraints


class Widget(StylableMixin):
    """
    Base class for all widgets. Inherit from this class to create custom widgets.
    """

    def __init__(self, pos: tuple[int, int] | None = None, size: tuple[int, int] = None,
                 constraints: Constraints | None = None, style_name: str = "Widget"):
        """
        Initialize the widget.
        :param pos: position of the widget. If None, the position will be set by the layout manager.
        :param size: size of the widget. If None, the size will be set by the layout manager or constraints.
        :param constraints: constraints are used by the layout manager to determine the size of the widget.
        :param style_name: name of the style to use for this widget. see :class:`StylableMixin` for details.
        """
        super().__init__(style_name)
        self._on_style_change = self._rebuild
        self._on_size_change: Callable[[tuple[int, int], tuple[int, int]], None] = lambda _1, _2: self._rebuild()

        _pos = pos or (0, 0)
        _size = size

        if size is None:
            if constraints is None:
                _size = (0, 0)
            else:
                w = constraints.pref_w or constraints.min_w
                h = constraints.pref_h or constraints.min_h
                _size = (w, h)

        self._initrect = None if pos is None or size is None else pg.Rect(pos, size)
        self._rect: pg.Rect = pg.Rect(_pos, _size)
        self._constraints = constraints or Constraints()

    def draw(self, surface: pg.Surface, parent_pos: tuple[int, int] = (0, 0)):
        """
        Draw the widget on the given surface.
        :param surface: Surface to draw the widget on.
        :param parent_pos: Position of the parent widget, used for nested widgets.
        :return:
        """
        pass

    def handle_event(self, event: pg.Event, parent_pos: tuple[int, int] = (0, 0)) -> bool:
        """
        Handle an event. Return True if the event was handled, False otherwise.
        :param event: Event to handle.
        :param parent_pos: Position of the parent widget, used for nested widgets.
        :return:
        """
        super().handle_event(event)
        return False

    @property
    def on_size_change(self) -> Callable[[tuple[int, int], tuple[int, int]], None]:
        return self._on_size_change

    def set_geometry(self, rect: pg.Rect):
        """
        Set the position and size of the widget. This is usually called by the layout manager.
        :param rect: The new rectangle defining the position and size of the widget.
        :return:
        """
        if self._initrect and self._initrect != rect:
            print("Warning: Widget initial rect is overridden by layout manager.")
            self._initrect = None

        old_size = self._rect.size
        self._rect = rect

        if old_size != self._rect.size:
            self._on_size_change(old_size, self._rect.size)

    @property
    def rect(self):
        return self._rect

    def _rebuild(self):
        """
        Rebuild the widget, for example when the style or the size changes.
        :return:
        """
        pass
