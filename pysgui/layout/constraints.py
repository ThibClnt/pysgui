from dataclasses import dataclass
from typing import Literal

ALIGN = Literal['start', 'center', 'end']
POLICY = Literal['fixed', 'expand', 'shrink']


@dataclass
class Constraints:
    """A class representing layout constraints for GUI elements.
    """

    min_w: int = 0
    min_h: int = 0
    max_w: int = float('inf')
    max_h: int = float('inf')
    pref_w: int = 0
    pref_h: int = 0
    halign: ALIGN = 'start'
    valign: ALIGN = 'start'
    hpolicy: POLICY = 'fixed'
    vpolicy: POLICY = 'fixed'
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
