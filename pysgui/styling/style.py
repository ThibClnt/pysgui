from __future__ import annotations
from dataclasses import dataclass

import pygame as pg

from .colors import ColorType


@dataclass(frozen=True)
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

    def font(self, secondary: bool = False) -> pg.Font:
        """
        Get the font name and size.
        :param secondary: If True, get the secondary font.
        :return: A tuple containing the font name and size.
        """
        def get_font(name: str, size: int) -> pg.Font:
            if name in pg.font.get_fonts():
                return pg.font.SysFont(name, size)
            else:
                return pg.font.Font(name, size)

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