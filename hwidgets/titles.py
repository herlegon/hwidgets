from pprint import pprint
from string import Template
import numpy as np
from pathlib import Path
from typing import Optional, Type
from PySide6.QtCore import (
    Qt,
    QRect,
    QPoint,
    QSize,
    QLocale,
    Property,
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
    QPaintEvent,
)
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QSizePolicy,
    QWidget,
)
from .style_manager import Theme
from .debug import (
    DEBUG_GEOMETRY,
    draw_widget_rect,
)
from .utils import load_png_icon, load_qss



def transform_black_to_blue(pixmap: QPixmap, target_color: QColor = QColor(0, 100, 255)) -> QPixmap:
    """
    Transform black/dark pixels to a target color while preserving transparency using NumPy.

    Args:
        pixmap: Source QPixmap with transparent background
        target_color: The color to transform black into (default: blue)

    Returns:
        New QPixmap with transformed colors
    """
    if pixmap.isNull():
        return pixmap

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
    image = pixmap.toImage().convertToFormat(QImage.Format.Format_RGBA8888)

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



class HTitle(QWidget):
    def __init__(
        self,
        /,
        parent: QWidget | None = None,
        f: Qt.WindowType = None,
        *,
        theme: Type[Theme],
        text: str = "",
        icon: str | Path | None = None,
    ) -> None:
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        self.setFixedHeight(theme.title.height)
        self.setSizePolicy(
            QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        )
        self.theme = theme
        self.title_style = self.theme.title


        self._layout = QHBoxLayout()
        # M3 margins: https://m3.material.io/components/top-app-bar/specs
        # self._layout.setContentsMargins(16, 4, 12, 4)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)
        self.setLayout(self._layout)

        self._icon: QLabel | None = None
        if icon is not None:
            icon_path = str(icon) if isinstance(icon, Path) else icon
            self._icon = QLabel(self)
            pixmap = load_png_icon(icon_path, self.title_style.font_color)
            self._icon.setPixmap(pixmap)
            self._icon.setFixedSize(pixmap.size())
            self._layout.addWidget(self._icon)
            self._layout.setSpacing(8)

        self._title = QLabel(text, self)
        self._layout.addWidget(
            self._title, 1, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        )
        self._update_style()

        self._title.setSizePolicy(
            QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        )
        self._title.setFixedHeight(self.title_style.height)


    def update_style(self):
        style = self.style()
        style.unpolish(self)
        style.polish(self)
        # Force geometry recalculation
        self.updateGeometry()
        self.update()


    def _update_style(self) -> None:
        qss_template = Template(load_qss("label.css"))
        qss = qss_template.substitute(
            font_color=f"{self.title_style.font_color}",
            font_color_disabled=f"{self.title_style.font_color_disabled}",
        )
        qss += " padding-bottom: 10px;"
        self.setStyleSheet(qss)
        self.setFont(self.title_style.font.make_font())
        self._title.setFont(self.title_style.font.make_font())
        self.update_style()


    def setText(self, text: str) -> None:
        self._title.setText(text)


    def text(self) -> str:
        return self._title.text()

    text = Property(str, text, setText)


    def setIcon(self, icon: Optional[str | Path]):
        icon_path = str(icon) if isinstance(icon, Path) else icon
        if self._icon is None:
            self._icon = QLabel(self)
            self._layout.insertWidget(0, self._icon)
        pixmap: QPixmap = load_png_icon(icon_path, self.title_style.font_color)
        self._icon.setPixmap(pixmap)
        self._icon.setFixedSize(pixmap.size())
        self._layout.setSpacing(8)


    def setPixmap(self, pixmap: QPixmap | QImage) -> None:
        if isinstance(pixmap, QImage):
            pixmap = QPixmap.fromImage(pixmap)
        pixmap = transform_black_to_blue(pixmap, QColor(self.title_style.font_color))

        if self._icon is None:
            self._icon: QLabel = QLabel(self)
            self._layout.insertWidget(0, self._icon)
        self._icon.setPixmap(pixmap)
        self._icon.setFixedSize(pixmap.size())
        self._layout.setSpacing(8)


    def paintEvent(self, event: QPaintEvent) -> None:
        super().paintEvent(event)
        painter = QPainter(self)
        if DEBUG_GEOMETRY:
            draw_widget_rect(self, painter)
        painter.end()

