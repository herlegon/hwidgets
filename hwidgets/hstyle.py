from dataclasses import dataclass
import os
from pathlib import Path
import sys
from typing import Final, Type
from PySide6.QtCore import (
    Qt,
)
from PySide6.QtGui import (
    QFont,
    QPainter,
    QColor,
    QPen,
)
from PySide6.QtWidgets import (
    QStyle,
    QStyledItemDelegate,
    QWidget,
)


DEBUG_GEOMETRY: bool = False

def draw_widget_rect(w: Type[QWidget], painter: QPainter):
    """Draw around a widget without clipping
    """
    painter.save()
    painter.setRenderHint(QPainter.RenderHint.Antialiasing, on=False)
    pen = QPen()
    pen.setWidth(1)
    pen.setColor(QColor("#d4d4d4"))
    painter.setPen(pen)
    painter.drawRect(0, 0, w.width() - 1, w.height() - 1)
    painter.restore()



class BoldHoverDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        # Make font bold on hover or selection
        if option.state & QStyle.StateFlag.State_MouseOver or \
           option.state & QStyle.StateFlag.State_Selected:
            font = QFont(option.font)
            font.setBold(True)
            option.font = font
        super().paint(painter, option, index)



@dataclass(slots=True)
class HStyle:
    window_bgd: str = "#252528"

    # Combobox
    widget_bgd: str = "#4F4D53"
    text_color: str = "#d4d4d8"
    # selection_bgd: str = "#454546"
    hover_bgd: str = "#66636D"

    # normal_button: str = "#5545bd"
    # hover_button: str = "#6a5bcc"
    # pressed_button: str = "#4539a0"
    # disabled_button: str = "#8b88c7"

    normal_button: str = "#5442bd"
    hover_button: str = "#7777FF"
    pressed_button: str = "#5555B3"
    disabled_button: str = "#A3A3D1"

    # hover_bgd: str ="#77f"
    selection_bgd: str = "#5545bd"

    selected_text: str = "#5545bd"


    border: str = "#505053" # same as hover

    checked: str = "#5442bd"

    selected: str = "#5442bd"


    # checkbox
    enabled = "#4B8DD8"
    disabled_bgd = "#313131"

    disabled_text = "#4E4E4E"
    checked_text = "#4632c7"

    divider: str = "#3B3B3B" # same as hover

    pressed: str = "#66636D" # same as hover

    title_text: str = "#5442bd"


    # Accent (hover)	"#4e83c2"	 # Slightly lighter for hover feedback
    # Accent (pressed)	"#345d8a"	# Darker variant for pressed/active states
    # Accent (disabled)	"#2e3c4f"	# Desaturated accent for disabled controls
    # Base background	"#1e1f22"	# Main window / panel background
    # Widget background	"#2a2c30"	# Lighter inner surfaces (e.g. combobox, buttons)
    # Hover background	"#34373d"	# Light hover elevation
    # Text (normal)	"#e6e6e6"	# Soft white for text, not full white
    # Text (disabled)	"#777"	# Dimmed gray
    # Border (neutral)	"#3a3d42"	# Subtle border for structure
    # Border (focus)	"#3d6ea8"	# Accent border when focused


# Checked / Active	#422ca1	Checkbox, radio, selected item
# Hover / Focused	#5948c4	Slightly brighter — gives visual lift
# Pressed	#352283	Darker tone for click feedback
# Disabled	#2d2b3e	Muted, low-contrast desaturation


COMBOBOX_HEIGHT = 24
COMBOBOX_RADIUS = 6
# COMBOBOX_PADDING = 10


RADIO_SIZE: int = 14
RADIO_RADIUS = COMBOBOX_RADIUS - 1
RADIO_BORDER_WIDTH = 2


CHECKBOX_SIZE: int = 14


LABEL_PADDING = COMBOBOX_RADIUS


GROUPBOX_HEIGHT = COMBOBOX_RADIUS * 2 + COMBOBOX_HEIGHT
GROUPBOX_TITLE_PADDING = COMBOBOX_RADIUS + 4
GROUPBOX_TITLE_HEIGHT = 10



SPINBOX_RADIUS = COMBOBOX_RADIUS
SPINBOX_PADDING = 12
SPINBOX_MIN_WIDTH = 50



DIVIDER_THICKNESS = 1
DIVIDER_MIN_LENGTH = 40
DIVIDER_PADDING = 16



# M3 material
# Track
#     Height  32dp
#     Width       52dp
#     Outline width       2dp
#     Shape       md.sys.shape.corner.full
# Handle
#     Height (unselected)     16dp
#     Height - with icon      24dp  <-
#     Height (selected)       24dp
#     Height (pressed)        28dp
#     Width (unselected)      16dp
#     Width - with icon       24dp
#     Width (selected)        24dp
#     Width (pressed)     28dp
#     Shape       md.sys.shape.corner.full
# State layer
#     Size    40dp
#     Shape       md.sys.shape.corner.full
# Target      Size    48dp
# Icon        Size (selected)     16dp
# Icon        Size (unselected)       16dp


TRACK_WIDTH: int = 40
TRACK_HEIGHT: int = COMBOBOX_HEIGHT
HANDLE_RADIUS: int = 16
TRACK_MARGIN = (TRACK_HEIGHT - HANDLE_RADIUS) // 2
TRACK_HEIGHT = TRACK_MARGIN * 2 + HANDLE_RADIUS


TITLE_1_HEIGHT = COMBOBOX_HEIGHT + COMBOBOX_RADIUS
TITLE_1_FONT_SIZE = 16
TITLE_1_BOLD = True

SCROLLBAR_TRACK_WIDTH = 8



TRACK_THICKNESS: Final[int] = 6
TRACK_MARGIN = TRACK_THICKNESS // 2
TRACK_Y: Final[int] = TRACK_THICKNESS // 2
CAP_OFFSET: Final[int] = TRACK_THICKNESS // 2




