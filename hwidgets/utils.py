
from dataclasses import dataclass
from hutils import parent_directory, path_basename
import os
from pathlib import Path
import sys
from PySide6.QtCore import (
    Qt,
)
from PySide6.QtGui import (
    QPainter,
    QPixmap,
    QColor,
    QImage,
)


TITLE_BAR_ICON_PATH = os.path.join(parent_directory(__file__), "icons")


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


def load_png_image(filename: str, h: int = -1) -> QPixmap:
    filepath = os.path.join(TITLE_BAR_ICON_PATH, filename)
    if not os.path.exists(filepath):
        raise ValueError(f"image {filepath} does not exist")
    qimage: QImage = QImage(filepath)

    painter: QPainter = QPainter()
    painter.begin(qimage)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setCompositionMode(
        QPainter.CompositionMode.CompositionMode_SourceIn
    )
    painter.drawRect(qimage.rect())
    painter.end()
    pixmap = QPixmap(qimage)
    if h != -1 and pixmap.height() != h:
        return pixmap.scaled(
                pixmap.width(),
                h,
                aspectMode=Qt.AspectRatioMode.KeepAspectRatio,
                # mode=Qt.TransformationMode.SmoothTransformation
            )
    return pixmap


def make_tinted_pixmap(
    pixmap: QPixmap,
    color: QColor | str
) -> QPixmap:
    tinted_pixmap = QPixmap(pixmap.size())
    tinted_pixmap.fill(Qt.GlobalColor.transparent)

    painter = QPainter(tinted_pixmap)
    painter.drawPixmap(0, 0, pixmap)
    painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
    painter.fillRect(pixmap.rect(), color)
    painter.end()

    return tinted_pixmap


# def load_dd_icon(self, icon: str | Path, color: str = "#E1E1E1") -> None:
#     filepath = os.path.join(TITLE_BAR_ICON_PATH, icon)
#     try:
#         self.dd_pixmap = load_png_icon(filepath, color)
#     except:
#         raise ValueError(f"{filepath} not found")

#     if self.dd_pixmap.size() != self.dd_size:
#         warn(f"{self.__class__} resize pixmap")
#         self.dd_pixmap = self.dd_pixmap.scaled(
#             self.dd_size,
#             aspectMode=Qt.AspectRatioMode.KeepAspectRatio
#         )
