from __future__ import annotations
__all__ = ["Color", "COLORS", "ColorType", "StylableMixin", "Style", "Theme", "ThemeStore"]

from dataclasses import dataclass
import json
from typing import Callable

import pygame
from pygame import Color
from pygame.colordict import THECOLORS as COLORS


ColorType = str | Color | tuple[int, int, int, int] | tuple[int, int, int]


class StylableMixin:
    """
    A mixin for classes that can be styled.
    This mixin provides properties to access different styles based on the current theme and the state of the widget.
    Change the style of a widget by updating the style name or using the style property.

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

    def handle_event(self, event: pygame.Event) -> bool:
        if event.type == pygame.USEREVENT and event.user_type == "theme_change":
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


@dataclass
class Style:
    """
    A class for storing a variety of styles.
    """
    background_color: ColorType = (248, 248, 248, 255)
    border_bottom_left_radius: int | None = None
    border_bottom_right_radius: int | None = None
    border_color: ColorType = (0, 0, 0, 255)
    border_radius: int = 0
    border_top_left_radius: int | None = None
    border_top_right_radius: int | None = None
    border_width: int = 1
    caption_height: int = 30
    foreground_color: ColorType = (0, 0, 0, 255)
    font_name: str = "Arial"
    font_size: int = 14
    secondary_background_color: ColorType = (248, 248, 248, 255)
    secondary_border_color: ColorType = (0, 0, 0, 255)
    secondary_border_width: int = 1
    secondary_font_name: str = "Arial"
    secondary_font_size: int = 14
    secondary_foreground_color: ColorType = (0, 0, 0, 255)
    shadow_color: ColorType = (0, 0, 0, 100)
    shadow_offset: tuple[int, int] = (0, 0)

    def font(self, secondary: bool = False) -> pygame.Font:
        """
        Get the font name and size.
        :param secondary: If True, get the secondary font.
        :return: A tuple containing the font name and size.
        """
        def get_font(name: str, size: int) -> pygame.Font:
            if name in pygame.font.get_fonts():
                return pygame.font.SysFont(name, size)
            else:
                return pygame.font.Font(name, size)

        if secondary:
            return get_font(self.secondary_font_name, self.secondary_font_size)
        return get_font(self.font_name, self.font_size)

    def clone(self, **kwargs) -> Style:
        """
        Create a copy of the style with some attributes replaced.
        :param kwargs: Attributes to replace.
        :return: A new Style object with the replaced attributes.
        """
        return Style(**{**self.__dict__, **kwargs})


class Theme:

    def __init__(self, name: str, styles: dict[str, Style] = None, variables: dict = None, root_stylename: str = None):
        self.__name: str = name
        self.__styles: dict[str, Style] = styles or {}
        self.__variables: dict = variables or {}
        self.__root_stylename = root_stylename

    def get(self, name: str, default: Style | None = None) -> Style:
        """
        Get a style by name.
        :param name: Name of the style
        :param default: Default value to return if the style is not found
        :return: Style object
        """
        return self.__styles.get(name, default or self.__styles.get(self.__root_stylename))

    def get_variable(self, name: str, default=None):
        """
        Get a variable by name.
        :param name: Name of the variable
        :param default: Default value to return if the variable is not found
        :return: Variable value
        """
        return self.__variables.get(name, default)

    @property
    def name(self) -> str:
        return self.__name

    def set_style(self, name: str, style: Style) -> None:
        """
        Set a style by name.
        :param name: Name of the style
        :param style: Style object
        """
        self.styles[name] = style

    def set_variable(self, name: str, value) -> None:
        """
        Set a variable by name.
        :param name: Name of the variable
        :param value: Variable value
        """
        self.variables[name] = value

    @property
    def styles(self):
        return self.__styles

    @property
    def style_names(self):
        return list(self.__styles.keys())

    @property
    def variables(self):
        return self.__variables

    @property
    def variable_names(self):
        return list(self.__variables.keys())


class ThemeStore:
    __store: dict[str, Theme] = {}
    __current: Theme

    @staticmethod
    def add(theme: Theme) -> Theme:
        """
        Add a new theme.
        :param theme: Theme object to add
        :return: The new theme object
        """
        ThemeStore.__store[theme.name] = theme
        return theme

    @staticmethod
    def current() -> Theme:
        """
        Get the current theme.
        :return: The current theme
        """
        return ThemeStore.__current

    @staticmethod
    def get_current_name() -> str:
        """
        Get the name of the current theme.
        :return: Name of the current theme
        """
        return ThemeStore.__current.name

    @staticmethod
    def get(name: str, default: Theme = None) -> Theme:
        """
        Get a theme by name. If no name is provided, return the current theme.
        :param name: Name of the theme
        :param default: Default value to return if the theme is not found
        :return: Theme object
        :raises KeyError: If the theme is not found and no default value is provided
        """
        if default is None and name not in ThemeStore.__store:
            raise KeyError(f"Theme '{name}' not found.")

        return ThemeStore.__store.get(name, default)

    @staticmethod
    def get_theme_names() -> list[str]:
        """
        Get the names of all available themes.
        :return: List of theme names
        """
        return list(ThemeStore.__store.keys())

    @staticmethod
    def load_default_themes() -> None:
        """
        Load the default themes.
        """
        default_theme = ThemeStore.load_theme("assets/themes/light.json")
        ThemeStore.__current = ThemeStore.get(default_theme.name)

    @staticmethod
    def load_theme(path: str) -> Theme:
        """
        Load a theme from a file.
        :param path: Path to the theme file
        :return: The loaded theme
        """

        def resolve(value):
            """Resolve if the value is a variable."""
            if isinstance(value, str) and value.startswith("$"):
                var_name = value[1:]
                if var_name not in variables:
                    raise ValueError(f"Variable '{var_name}' not found in theme variables.")
                return variables[var_name]
            return value

        with open(path) as file:
            data = json.load(file)

        try:
            theme_name = data["name"]
            root_name = data.get("root", None)
            variables: dict = data.get("variables", dict())

            json_styles = data["styles"]
        except (KeyError, TypeError) as e:
            raise TypeError("Invalid theme file. A theme must have a name and one or several styles.") from e

        styles = dict()
        if root_name is not None and root_name not in json_styles:
            raise ValueError(f"Root style '{root_name}' not found in theme styles.")

        resolved_root = dict()

        if root_name:
            json_root = json_styles[root_name]
            del json_styles[root_name]
            resolved_root = {key: resolve(value) for key, value in json_root.items()}
            styles[root_name] = Style(**resolved_root)

        for name, style in json_styles.items():
            try:
                resolved_style = {key: resolve(value) for key, value in style.items()}
                styles[name] = Style(**{**resolved_root, **resolved_style})
            except (KeyError, TypeError) as e:
                raise TypeError(f"Invalid style '{name}' in theme '{theme_name}'.") from e

        return ThemeStore.add(Theme(theme_name, styles, variables, root_name))

    @staticmethod
    def remove(name: str) -> None:
        """
        Remove a theme.
        :param name: Name of the theme to remove
        :raises KeyError: If the theme is not found
        """
        del ThemeStore.__store[name]

    @staticmethod
    def use(name: str) -> None:
        """
        Set the current theme by name.
        :param name: Name of the theme to set as current
        :raises KeyError: If the theme is not found
        """
        ThemeStore.__current = ThemeStore.get(name)
