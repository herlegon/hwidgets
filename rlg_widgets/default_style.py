

from .style_types import (
    ButtonStyle,
    TextStyle,
)


BACKGROUND_COLOR = "rgb(32, 32, 32)"
BACKGROUND_HOVER_COLOR = "rgb(42, 42, 42)"
BACKGROUND_DISABLED_COLOR = "rgba(32, 32, 32, 30)"  # poc
TEXT_COLOR = "rgb(200, 200, 200)"
TITLE_TEXT_COLOR = "#3366CC"

BORDER_RADIUS: int = 12
BORDER_COLOR = "rgb(80,80,80)"


LABEL_STYLE: TextStyle = TextStyle(
    font="",
    point=11,
    color=TEXT_COLOR,
    height=22,
    bold=False
)

BUTTON_STYLE = ButtonStyle = ButtonStyle(
    border_radius=8,
    border=1,
    border_color=BORDER_COLOR,
    color=TEXT_COLOR,
    # bgd_color=BACKGROUND_COLOR,
    bgd_color="rgb(42, 42, 42)",
    color_hover=TEXT_COLOR,
    bgd_color_hover="rgb(52, 52, 52)",
    color_pressed=TEXT_COLOR,   # poc
    bgd_color_pressed=BACKGROUND_HOVER_COLOR,   # poc
    color_checked=TEXT_COLOR,   # poc
    bgd_color_checked="#424242",   # poc
    color_disabled=TEXT_COLOR,   # poc
    bgd_color_disabled="#424242",   # poc
)



TITLE_1_STYLE: TextStyle = TextStyle(
    font="",
    point=14,
    color=TITLE_TEXT_COLOR,
    height=32,
    bold=True
)
