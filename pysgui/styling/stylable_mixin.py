from typing import Callable

import pygame as pg

from .style import Style
from .theme_store import ThemeStore


class StylableMixin:
    """
    A mixin for classes that can be styled.
    This mixin provides properties to access different styles based on the current theme and the state of the widget.
    Change the style of a widget by updating the style name or using the style property.

    Registers to listen for style changes by setting the on_style_change callback.
    Use the handle_event method to handle theme change events.

    Example::

        class MyWidget(StylableMixin):
            def __init__(self):
                StylableMixin.__init__(self, "my_widget")

            def draw(self, surface):
                pygame.draw.rect(surface, self.style.background_color, self.rect)

        widget = MyWidget()

        # Use a custom style defined in the current theme
        widget.style_name = "custom_widget"

        # Override the current style with a custom style
        widget.style = Style(background_color=(255, 0, 0))

        # Revert to the style defined in the current theme
        widget.style = None
    """

    def __init__(self, style_name: "str", on_style_change: Callable[[], None] = (lambda: None)):
        self.__style_name: str = style_name
        self.__style: Style | None = None
        self._on_style_change = on_style_change

    @property
    def active_style(self):
        return self.__get_with_state("active")

    @property
    def disabled_style(self):
        return self.__get_with_state("disabled")

    @property
    def focus_style(self):
        return self.__get_with_state("focus")

    def handle_event(self, event: pg.Event) -> bool:
        if event.type == pg.USEREVENT and event.user_type == "theme_change":
            self._on_style_change()
            return True
        return False

    @property
    def hover_style(self):
        return self.__get_with_state("hover")

    @property
    def on_style_change(self):
        return self._on_style_change

    @property
    def style(self):
        return self.__style or ThemeStore.current().get(self.style_name)

    @style.setter
    def style(self, value: Style | None):
        self.__style = value
        self._on_style_change()

    @property
    def style_name(self):
        return self.__style_name

    @style_name.setter
    def style_name(self, value: str):
        self.__style_name = value
        self._on_style_change()

    def __get_with_state(self, state: str) -> Style:
        return ThemeStore.current().get(f"{self.style_name}:{state}", self.style)
