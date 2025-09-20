import pygame as pg

from pysgui.styling import StylableMixin
from .widget import Widget


class Window(StylableMixin):
    """
    A window is a container for widgets. It can be fullscreen or a fixed size.
    Inherit from this class to create custom windows.
    """

    def __init__(self, fullscreen: bool = True, rect: pg.Rect = None, visible: bool = True):
        """
        Initialize the window.
        :param fullscreen: If True, the window will take the full size of the application window.
        :param rect: The rectangle defining the position and size of the window. Ignored if fullscreen is True.
        :param visible: If False, the window will not be drawn or receive events.
        """
        StylableMixin.__init__(self, "window")
        self._on_style_change = self._build_surfaces

        self._rect: pg.Rect = rect if rect else pg.Rect(0, 0, 0, 0)
        self._fullscreen = fullscreen
        self.visible = visible
        self.widgets: list[Widget] = []

        self._surface = pg.Surface(self.rect.size, pg.SRCALPHA)

    def add_widget(self, widget: Widget):
        self.widgets.append(widget)

    def draw(self, surface: pg.Surface):
        if not self.visible:
            return

        self.draw_window(surface)

        for widget in reversed(self.widgets):
            widget.draw(surface)

    def draw_window(self, surface: pg.Surface):
        self._surface.fill(self.style.background_color)
        surface.blit(self._surface, self.rect.topleft)

    @property
    def fullscreen(self):
        return self._fullscreen

    def handle_event(self, event: pg.Event) -> bool:
        # handle style change
        StylableMixin.handle_event(self, event)

        if not self.visible:
            return False

        for widget in reversed(self.widgets):
            if widget.handle_event(event):
                return True
        return False

    def move(self, pos: tuple[int, int]):
        self._rect.update(pos, self._rect.size)

    @property
    def rect(self):
        return self._rect

    @rect.setter
    def rect(self, value: pg.Rect):
        self._rect = value
        self._build_surfaces()

    def resize(self, size: tuple[int, int]):
        self._rect.update(self._rect.topleft, size)
        self._build_surfaces()

    def update(self, dt: float):
        pass

    def _build_surfaces(self):
        self._surface = pg.Surface(self.rect.size, pg.SRCALPHA)
