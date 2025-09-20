import pygame as pg

from pysgui import Widget


class Layout:
    """
    Base class for layouts. Layouts are used to arrange widgets in a container, using apply_layout.
    They only define the layout algorithm, not the container itself.
    """
    def apply_layout(self, widgets: list[Widget], area: pg.Rect) -> None:
        """
        Apply the layout to the given widgets within the specified area.
        :param widgets: widgets to arrange
        :param area: area to arrange the widgets in
        :return:
        """
        raise NotImplementedError("Subclasses should implement this method.")
