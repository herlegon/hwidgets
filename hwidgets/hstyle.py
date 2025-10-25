from dataclasses import dataclass
import os
from pathlib import Path
import sys
# from PySide6.QtCore import (
# )
from PySide6.QtGui import (
    QFont,
    QPainter,
    QPixmap,
    QColor,
    QImage,
)
from PySide6.QtWidgets import (
    QStyle,
    QStyledItemDelegate,
)
from hutils import parent_directory, path_basename



TITLE_BAR_ICON_PATH = os.path.join(parent_directory(__file__), "icons")

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


# def png_to_pixmap(filename: str, color: str, w: int = 24) -> QPixmap:
#     filepath = os.path.join(TITLE_BAR_ICON_PATH, filename)
#     if not os.path.exists(filepath):
#         raise ValueError(f"image {filepath} does not exist")
#     qimage: QImage = QImage(filepath)
#     color = QColor(color)

#     painter: QPainter = QPainter()
#     painter.begin(qimage)
#     painter.setRenderHint(QPainter.RenderHint.Antialiasing)
#     painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
#     painter.setBrush(color)
#     painter.setPen(color)
#     painter.drawRect(qimage.rect())
#     painter.end()
#     pixmap = QPixmap(qimage)
#     # if pixmap.width() != w:
#     #     return pixmap.scaled(
#     #             w,
#     #             w,
#     #             aspectMode=Qt.AspectRatioMode.KeepAspectRatio,
#     #             # mode=Qt.TransformationMode.SmoothTransformation
#     #         )
#     return pixmap



class BoldHoverDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        # Make font bold on hover or selection
        if option.state & QStyle.StateFlag.State_MouseOver or \
           option.state & QStyle.StateFlag.State_Selected:
            font = QFont(option.font)
            font.setBold(True)
            option.font = font
        super().paint(painter, option, index)



def load_qss(qss_fp: str, variant: str = "") -> str:
    variant = f"_{variant}" if variant else ""
    css_dir: Path = Path(__file__).parent / "css"

    common_fp = css_dir.joinpath(
        Path(f"{path_basename(qss_fp)}{variant}.qss")
    )
    if not common_fp.exists():
        raise FileNotFoundError(f"missing file: {common_fp}")
    with open(common_fp, 'r') as f:
        qss = f.read()

    platform_fp = css_dir.joinpath(
        Path(f"{path_basename(qss_fp)}{variant}_{sys.platform}.qss")
    )
    if platform_fp.exists():
        with open(platform_fp, 'r') as f:
            qss += "\n" + f.read()

    return qss





@dataclass(slots=True)
class HStyle:
    window_bgd: str = "#181819"

    # Combobox
    widget_bgd: str = "#4F4D53"
    text_color: str = "#d4d4d8"
    # selection_bgd: str = "#454546"
    # hover_bgd: str = "#66636D"
    hover_bgd: str ="#77f"
    selection_bgd: str = "#5545bd"

    selected_text: str = "#5545bd"


    border: str = "#505053" # same as hover

    checked: str = "#6a5bcc"


    # checkbox
    enabled = "#4B8DD8"
    disabled_bgd = "#313131"

    disabled_text = "#4E4E4E"
    checked_text = "#4632c7"

    divider: str = "#505053" # same as hover


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
COMBOBOX_RADIUS = 8
# COMBOBOX_PADDING = 10


RADIO_RADIUS = COMBOBOX_RADIUS # change to COMBOBOX_RADIUS ?
RADIO_BORDER_WIDTH = 2


# STATE_LAYER_SIZE: int = round(48/(2 * dp_to_px)) * 2
CHECKBOX_STATE_LAYER_SIZE = COMBOBOX_HEIGHT
# Icons are from Material website
CHECKBOX_ICON_SIZE: int = 16
# blank margin in Material icons -> real button size in icon is 18x18
CHECKBOX_BUTTON_SIZE: int = 18


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
# Note: Track outline width is currently not used
TRACK_OUTLINE_WIDTH = 0
HANDLE_RADIUS: int = 16
TRACK_MARGIN = (TRACK_HEIGHT - HANDLE_RADIUS) // 2
TRACK_HEIGHT = TRACK_MARGIN * 2 + HANDLE_RADIUS


TITLE_1_HEIGHT = COMBOBOX_HEIGHT
TITLE_1_FONT_SIZE = 14
TITLE_1_BOLD = True

SCROLLBAR_TRACK_WIDTH = 8
