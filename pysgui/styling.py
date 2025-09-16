from __future__ import annotations
__all__ = ["Color", "COLORS", "ColorType", "StylableMixin", "Style", "Theme", "ThemeStore"]

from dataclasses import dataclass
import json

import pygame
from pygame import Color
from pygame.colordict import THECOLORS as COLORS


ColorType = str | Color | tuple[int, int, int, int] | tuple[int, int, int]


class StylableMixin:
    """
    A mixin for classes that can be styled.
    """

    def __init__(self, style_name: "str"):
        self.style_name: str = style_name

    @property
    def active_style(self):
        return self.__get_with_state("active")

    @property
    def disabled_style(self):
        return self.__get_with_state("disabled")

    @property
    def focus_style(self):
        return self.__get_with_state("focus")

    @property
    def hover_style(self):
        return self.__get_with_state("hover")

    @property
    def style(self):
        return ThemeStore.current().get(self.style_name)

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


class Theme:

    def __init__(self, name: str, styles: dict[str, Style] = None, variables: dict = None):
        self.__name: str = name
        self.__styles: dict[str, Style] = styles or {}
        self.__variables: dict = variables or {}

    def get(self, name: str, default: Style = Style()) -> Style:
        """
        Get a style by name.
        :param name: Name of the style
        :return: Style object
        """
        return self.__styles.get(name, default)

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
    def add(name: str, styles: dict[str, Style] = None, variables: dict = None) -> Theme:
        """
        Add a new theme.
        :param name: Name of the new theme
        :param styles: Styles composing the theme
        :param variables: Variables defined in the theme
        :return: The new theme object
        """
        theme = Theme(name, styles, variables)
        ThemeStore.__store[name] = theme
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
            variables: dict = data.get("variables", dict())
            json_styles = data["styles"]
        except (KeyError, TypeError) as e:
            raise TypeError("Invalid theme file. A theme must have a name and one or several styles.") from e

        styles = dict()
        for name, style in json_styles.items():
            try:
                resolved_style = {key: resolve(value) for key, value in style.items()}
                styles[name] = Style(**resolved_style)
            except (KeyError, TypeError) as e:
                raise TypeError(f"Invalid style '{name}' in theme '{theme_name}'.") from e

        return ThemeStore.add(theme_name, styles, variables)

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
