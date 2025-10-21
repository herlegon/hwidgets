from copy import copy
from dataclasses import dataclass
import os
from pathlib import Path
import re
from typing import NamedTuple
from PySide6.QtCore import (
    Qt,
)
from PySide6.QtGui import (
    QPixmap,
    QImage,
    QColor,
    QPainter,
)


# 1080p
dp_to_px = 1.6
# 1440p
# dp_to_px = 1.2

BORDER_RADIUS: int = 12

# Grip width
GRIP_BORDER_SIZE: int = BORDER_RADIUS

# Window shadow
SHADOW_RADIUS = 0
SHADOW_ALPHA = 150

# Toolbar
CONTROL_BUTTON_HEIGHT: int = 32
CONTROL_BUTTON_WIDTH: int = 46


EDGE_TO_CURSOR_SHAPE = {
    Qt.Edge.TopEdge | Qt.Edge.LeftEdge: Qt.CursorShape.SizeFDiagCursor,
    Qt.Edge.TopEdge: Qt.CursorShape.SizeVerCursor,
    Qt.Edge.TopEdge | Qt.Edge.RightEdge: Qt.CursorShape.SizeBDiagCursor,
    Qt.Edge.RightEdge: Qt.CursorShape.SizeHorCursor,
    Qt.Edge.BottomEdge | Qt.Edge.RightEdge: Qt.CursorShape.SizeFDiagCursor,
    Qt.Edge.BottomEdge: Qt.CursorShape.SizeVerCursor,
    Qt.Edge.BottomEdge | Qt.Edge.LeftEdge: Qt.CursorShape.SizeBDiagCursor,
    Qt.Edge.LeftEdge: Qt.CursorShape.SizeHorCursor,
}


# Not used anymore, keep it?
class WindowPropertyFlag(NamedTuple):
    WINDOWED = 0x1
    MAXIMIZED = 0x2
    FULLSCREEN = 0x4
    ACTIVE = 0x10
    INACTIVE = 0x20
    ACTIVE_MASK = 0xF0
    MODE_MASK = 0x0F

WINDOW_PROPERTY: dict[WindowPropertyFlag, str] = {
    WindowPropertyFlag.WINDOWED: "",
    WindowPropertyFlag.WINDOWED | WindowPropertyFlag.ACTIVE: "windowed_inactive",
    WindowPropertyFlag.WINDOWED | WindowPropertyFlag.INACTIVE: "windowed_inactive",

    WindowPropertyFlag.MAXIMIZED: "maximized",
    WindowPropertyFlag.MAXIMIZED | WindowPropertyFlag.ACTIVE: "maximized",
    WindowPropertyFlag.MAXIMIZED | WindowPropertyFlag.INACTIVE: "maximized_inactive",

    WindowPropertyFlag.FULLSCREEN: "fullscreen",
    WindowPropertyFlag.FULLSCREEN | WindowPropertyFlag.ACTIVE: "fullscreen",
    WindowPropertyFlag.FULLSCREEN | WindowPropertyFlag.INACTIVE: "fullscreen",

    WindowPropertyFlag.ACTIVE: "",
    WindowPropertyFlag.INACTIVE: "windowed_inactive",
}

TITLE_BAR_ICON_PATH = str(Path.resolve(Path(os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    "icons"
))))

def load_png_icon(filename: str, color: str) -> QPixmap:
    filepath = os.path.join(TITLE_BAR_ICON_PATH, filename)
    if not os.path.exists(filepath):
        raise ValueError(f"image {filepath} does not exist")
    qimage: QImage = QImage(filepath)
    color = QColor(color)

    painter: QPainter = QPainter()
    painter.begin(qimage)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
    painter.setBrush(color)
    painter.setPen(color)
    painter.drawRect(qimage.rect())
    painter.end()
    return QPixmap(qimage)


def png_to_pixmap(filename: str, color: str, w: int = 24) -> QPixmap:
    filepath = os.path.join(TITLE_BAR_ICON_PATH, filename)
    if not os.path.exists(filepath):
        raise ValueError(f"image {filepath} does not exist")
    qimage: QImage = QImage(filepath)
    color = QColor(color)

    painter: QPainter = QPainter()
    painter.begin(qimage)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
    painter.setBrush(color)
    painter.setPen(color)
    painter.drawRect(qimage.rect())
    painter.end()
    pixmap = QPixmap(qimage)
    # if pixmap.width() != w:
    #     return pixmap.scaled(
    #             w,
    #             w,
    #             aspectMode=Qt.AspectRatioMode.KeepAspectRatio,
    #             # mode=Qt.TransformationMode.SmoothTransformation
    #         )
    return pixmap




@dataclass
class TitleBarStyle:
    text: str = "#9E9E9E"
    text_inactive: str ="#141414"
    bgd: str = "#424242"
    bgd_hover: str = "#757575"
    bgd_inactive: str = "#BDBDBD"
    border_color: str = "#424242"
    border_width: int = 0


# @dataclass
# class DefaultWidgetColorStyle:
#     text: str = "#9E9E9E"
#     text_inactive: str ="#141414",
#     bgd: str = "#424242"
#     bgd_hover: str = "#757575"
#     bgd_inactive: str = "#BDBDBD"
#     border_color: str = "#424242"
#     border: int = 0


@dataclass
class DefaultSwitchColorStyle:
    track_color_on = "#1565C0"
    track_color_off = "#757575"
    # track outline color = handle_color
    handle_color_on = "#1A237E"
    handle_color_off = "#424242"


@dataclass(slots=True, frozen=True)
class CheckboxColor:
    enabled = "#1565C0"
    disabled = "#424242"


