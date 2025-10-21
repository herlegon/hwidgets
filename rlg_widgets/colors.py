from copy import copy
from dataclasses import dataclass
import re
from PySide6.QtGui import (
    QColor,
)


@dataclass
class ScrollbarColor:
    bgd_color="#424242"
    color="#1565C0"
    thickness=10
    handle_color="#1565C0"
    handle_color_hover="#1565C0"
    disabled = "#424242"


OPACITY_DISABLED = 97
OPACITY_READ_ONLY = 97


MATERIAL2_COLORS: dict = {
    'yellow800': "#F9A825",
    'deep_orange800': "#D84315",
    'green800': "#2E7D32",
    'green600': "#43A047",
    'green700': "#388E3C",
    'green900': "#1B5E20",

    'grey400': "#BDBDBD",
    'grey500': "#9E9E9E",
    'grey600': "#757575",
    'grey800': "#616161",

    'grey': "#909090",

}


Color = str | tuple[int]
def tuple_to_css(color: tuple[int]) -> str:
    # Limitation HSL is not supported
    if isinstance(color, str):
        return color
    return "#{color}".format(color=''.join(map(lambda x: f"{x:02x}", color)))


def css_to_tuple(color: str | list | tuple) -> tuple[int]:
    if isinstance(color, list):
        return tuple(color)

    if isinstance(color, tuple):
        return color

    if color.startswith('rgb'):
        return tuple(map(lambda c: int(c), re.findall(re.compile(r"\d+"), color)))

    if color.startswith('#'):
        color = color[1:]
        if len(color) in (3, 4):
            return tuple(map(lambda c: int(c, 16), list(color)))
        if len(color) in (6, 8):
            return tuple(
                map(lambda c: int(c, 16), tuple(re.findall(re.compile(r".."), color)))
            )

    return (0, 0, 0, 255)


def get_opac_color(color: str | list | tuple | QColor, opacity: int) -> QColor:
    if isinstance(color, QColor):
        qc: QColor = copy(color)
    else:
        qc: QColor = QColor(color)
    qc.setAlpha(opacity)
    return qc

