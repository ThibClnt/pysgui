from dataclasses import dataclass
from enum import Enum


class Align(Enum):
    START = 'start'
    CENTER = 'center'
    END = 'end'


class Policy(Enum):
    FIXED = 'fixed'
    EXPAND = 'expand'
    SHRINK = 'shrink'


@dataclass
class Constraints:
    """A class representing layout constraints for GUI elements.
    """

    min_w: int = 0
    min_h: int = 0
    max_w: int = float('inf')
    max_h: int = float('inf')
    pref_w: int | None = None
    pref_h: int | None = None
    halign: Align = Align.START
    valign: Align = Align.START
    hpolicy: Policy = Policy.FIXED
    vpolicy: Policy = Policy.FIXED
    hstretch: float = 1.0
    vstretch: float = 1.0
    margin_top: int = 0
    margin_bottom: int = 0
    margin_left: int = 0
    margin_right: int = 0
    padding_top: int = 0
    padding_bottom: int = 0
    padding_left: int = 0
    padding_right: int = 0
