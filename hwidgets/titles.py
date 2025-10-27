from pathlib import Path
from typing import Optional, overload
from PySide6.QtCore import (
    Qt,
    QRect,
    QPoint,
    QSize,
    QLocale,
)
from PySide6.QtGui import (
    QCursor,
    QFont,
    QIcon,
    QImage,
    QPalette,
    QRegion,
    QPixmap,
    QColor,
    QPainter,
)
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QSizePolicy,
    QWidget,
)
from .hstyle import (
    HStyle,
    TITLE_1_HEIGHT,
    TITLE_1_FONT_SIZE,
    TITLE_1_BOLD,
    load_png_icon,
)
# from .style_types import (
#     TextStyle,
#     textstyle_to_font,
# )
# from .utils import png_to_pixmap


import numpy as np


def transform_black_to_blue(pixmap: QPixmap, target_color: QColor = QColor(0, 100, 255)) -> QPixmap:
    """
    Transform black/dark pixels to a target color while preserving transparency using NumPy.

    Args:
        pixmap: Source QPixmap with transparent background
        target_color: The color to transform black into (default: blue)

    Returns:
        New QPixmap with transformed colors
    """
    img = pixmap.toImage()
    img = img.convertToFormat(QImage.Format.Format_ARGB32)
    width, height = img.width(), img.height()

    ptr = img.constBits()
    np_img = np.array(ptr).reshape((height, width, 4))
    bgr = np_img[:, :, :3].astype(np.float32)
    alpha = np_img[:, :, 3:4]

    luminosity_matrix = np.array([0.114, 0.587, 0.299])
    gray = bgr @ luminosity_matrix
    blackness = (255 - gray) / 255.0

    target_bgr = np.array(
        [
            target_color.blue(),
            target_color.green(),
            target_color.red()
        ], dtype=np.float32
    )

    result_bgr = (blackness[:, :, np.newaxis] * target_bgr).astype(np.uint8)
    result = np.concatenate([result_bgr, alpha], axis=2)

    return QPixmap.fromImage(
        QImage(result.data, width, height, width * 4, QImage.Format.Format_ARGB32)
    )




def colorize_pixmap(pixmap: QPixmap, color: QColor) -> QPixmap:
    """Return a colorized copy of a black→color pixmap, preserving shading and transparency."""
    image = pixmap.toImage().convertToFormat(QImage.Format_RGBA8888)

    # Get the pixel buffer as a numpy array
    ptr = image.bits()
    arr = (
        np.frombuffer(ptr, np.uint8)
        .reshape((image.height(), image.width(), 4))
        .astype(np.float32)
    )

    # Convert RGB to float for calculations
    rgb = arr[..., :3].astype(np.float32) / 255.
    a = arr[..., 3]  # keep alpha as uint8

    print(np.max(rgb))

    # Compute luminance
    lum = (0.299 * rgb[..., 0] + 0.587 * rgb[..., 1] + 0.114 * rgb[..., 2]) / 255.0
    inv = 1.0 - lum  # black=1, white=0

    # Target color as float
    cr, cg, cb = color.redF(), color.greenF(), color.blueF()

    # Apply color
    rgb[..., 0] = np.clip(inv * cr * 255, 0, 255)
    rgb[..., 1] = np.clip(inv * cg * 255, 0, 255)
    rgb[..., 2] = np.clip(inv * cb * 255, 0, 255)

    # Cast back to uint8
    arr[..., :3] = rgb.astype(np.uint8)
    arr[..., 3] = a  # preserve alpha

    # Return a new pixmap
    return QPixmap.fromImage(image)


class HTitle1(QWidget):
    def __init__(
        self,
        /,
        parent: QWidget | None = None,
        f: Qt.WindowType = None,
        *,
        hstyle: HStyle,
        text: str = "",
        icon: str | Path | None = None,

        modal: bool | None = None,
        windowModality: Qt.WindowModality | None = None,
        enabled: bool | None = None,
        geometry: QRect | None = None,
        frameGeometry: QRect | None = None,
        normalGeometry: QRect | None = None,
        x: int | None = None,
        y: int | None = None,
        pos: QPoint | None = None,
        frameSize: QSize | None = None,
        size: QSize | None = None,
        width: int | None = None,
        height: int | None = None,
        rect: QRect | None = None,
        childrenRect: QRect | None = None,
        childrenRegion: QRegion | None = None,
        sizePolicy: QSizePolicy | None = None,
        minimumSize: QSize | None = None,
        maximumSize: QSize | None = None,
        minimumWidth: int | None = None,
        minimumHeight: int | None = None,
        maximumWidth: int | None = None,
        maximumHeight: int | None = None,
        sizeIncrement: QSize | None = None,
        baseSize: QSize | None = None,
        palette: QPalette | None = None,
        font: QFont | None = None,
        cursor: QCursor | None = None,
        mouseTracking: bool | None = None,
        tabletTracking: bool | None = None,
        isActiveWindow: bool | None = None,
        focusPolicy: Qt.FocusPolicy | None = None,
        focus: bool | None = None,
        contextMenuPolicy: Qt.ContextMenuPolicy | None = None,
        updatesEnabled: bool | None = None,
        visible: bool | None = None,
        minimized: bool | None = None,
        maximized: bool | None = None,
        fullScreen: bool | None = None,
        sizeHint: QSize | None = None,
        minimumSizeHint: QSize | None = None,
        acceptDrops: bool | None = None,
        windowTitle: str | None = None,
        windowIcon: QIcon | None = None,
        windowIconText: str | None = None,
        windowOpacity: float | None = None,
        windowModified: bool | None = None,
        toolTip: str | None = None,
        toolTipDuration: int | None = None,
        statusTip: str | None = None,
        whatsThis: str | None = None,
        accessibleName: str | None = None,
        accessibleDescription: str | None = None,
        accessibleIdentifier: str | None = None,
        layoutDirection: Qt.LayoutDirection | None = None,
        autoFillBackground: bool | None = None,
        styleSheet: str | None = None,
        locale: QLocale | None = None,
        windowFilePath: str | None = None,
        inputMethodHints: Qt.InputMethodHint | None = None
    ) -> None:
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        self.setFixedHeight(TITLE_1_HEIGHT)
        self.hstyle = hstyle

        self._layout = QHBoxLayout()
        # M3 margins: https://m3.material.io/components/top-app-bar/specs
        # self._layout.setContentsMargins(16, 4, 12, 4)
        self._layout.setContentsMargins(12, 0, 12, 0)
        self._layout.setSpacing(8)
        self.setLayout(self._layout)

        self._icon: QLabel | None = None
        if icon is not None:
            icon_path = str(icon) if isinstance(icon, Path) else icon
            self._icon = QLabel(self)
            pixmap = load_png_icon(icon_path, hstyle.text_color)
            self._icon.setPixmap(pixmap)
            self._icon.setFixedSize(pixmap.size())
            self._layout.addWidget(self._icon)
        self._title = QLabel(text, self)
        self._layout.addWidget(
            self._title, 0, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        )

        font = QFont()
        font.setBold(TITLE_1_BOLD)
        font.setUnderline(False)
        font.setItalic(False)
        self._title.setFont(font)
        # self.setStyleSheet(
        #     """
        #         background-color: yellow; border: 1px solid white;
        #     """
        # )
        self._title.setStyleSheet(
            """
                QLabel{{
                    /* background-color: white; */
                    color: {color};
                    font-family: {font_family};
                    font-size: {font_size};
                    /* border: 1px solid red; */
                }}
            """.format(
                color=self.hstyle.text_color,
                font_family="\"Segoe UI\", \"Sans Serif\"",
                font_size=f"{TITLE_1_FONT_SIZE}pt",
            )
        )
        self._title.setSizePolicy(
            QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        )
        self._title.setFixedHeight(TITLE_1_HEIGHT)


    def setText(self, text: str) -> None:
        self._title.setText(text)


    def setIcon(self, icon: Optional[str | Path]):
        icon_path = str(icon) if isinstance(icon, Path) else icon
        if self._icon is None:
            self._icon = QLabel(self)
            self._layout.insertWidget(0, self._icon)
        pixmap: QPixmap = load_png_icon(icon_path, self.hstyle.selection_bgd)
        self._icon.setPixmap(pixmap)
        self._icon.setFixedSize(pixmap.size())


    def setPixmap(self, pixmap: QPixmap | QImage) -> None:
        if isinstance(pixmap, QImage):
            pixmap = QPixmap.fromImage(pixmap)
        pixmap = transform_black_to_blue(pixmap, QColor(self.hstyle.selection_bgd))

        if self._icon is None:
            self._icon: QLabel = QLabel(self)
            self._layout.insertWidget(0, self._icon)
        self._icon.setPixmap(pixmap)
        self._icon.setFixedSize(pixmap.size())

