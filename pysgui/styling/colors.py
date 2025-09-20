from pygame import Color
from pygame.colordict import THECOLORS as COLORS


ColorType = str | Color | tuple[int, int, int, int] | tuple[int, int, int]


def parse_color(value: ColorType) -> Color:
    """
    Parse a color from a string, tuple, or pygame Color object.
    Supports hex strings, RGB tuples, RGBA tuples, and color names.
    :param value: The color to parse.
    :return: A pygame Color object.
    """
    if isinstance(value, Color):
        return value
    elif isinstance(value, str):
        value = value.strip()
        if value.startswith("#"):
            # Hex string
            hex_value = value.lstrip("#")
            if len(hex_value) == 6:
                r = int(hex_value[0:2], 16)
                g = int(hex_value[2:4], 16)
                b = int(hex_value[4:6], 16)
                return Color(r, g, b)
            elif len(hex_value) == 8:
                r = int(hex_value[0:2], 16)
                g = int(hex_value[2:4], 16)
                b = int(hex_value[4:6], 16)
                a = int(hex_value[6:8], 16)
                return Color(r, g, b, a)
            else:
                raise ValueError(f"Invalid hex color string: {value}")
        elif value.lower() in COLORS:
            # Named color
            return COLORS[value.lower()]
        else:
            raise ValueError(f"Unknown color name: {value}")
    elif isinstance(value, tuple):
        if len(value) == 3 or len(value) == 4:
            return Color(*value)
        else:
            raise ValueError(f"Invalid color tuple length: {len(value)}")
    else:
        raise TypeError(f"Unsupported color type: {type(value)}")
