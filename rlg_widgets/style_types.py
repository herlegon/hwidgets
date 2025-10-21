from dataclasses import dataclass
from PySide6.QtGui import (
    QFont,
)


@dataclass(slots=True, frozen=True)
class ButtonStyle:
    border_radius: int
    border_color: str
    border: int
    color: str
    bgd_color: str
    color_hover: str
    bgd_color_hover: str
    color_pressed: str
    bgd_color_pressed: str
    color_checked: str
    bgd_color_checked: str
    color_disabled: str
    bgd_color_disabled: str




@dataclass(slots=True, frozen=True)
class TextStyle:
    font: str
    point: int
    color: str | tuple
    height: int
    bold: bool = False
    italic: bool = False
    underline: bool = False


def textstyle_to_font(style: TextStyle) -> QFont:
    font = QFont(
        # style.font,
        ['sans-serif', 'Noto Sans', 'Segoe UI', 'SF Pro'],
        pointSize=style.point,
        italic=style.italic
    )
    font.setBold(style.bold)
    font.setUnderline(style.underline)
    # print(f"textstyle_to_font: {font.family()}")
    return font


# Resources:
# https://m3.material.io/foundations/interaction/states/applying-states
