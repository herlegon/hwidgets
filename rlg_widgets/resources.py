
import os
from pathlib import Path
from PySide6.QtGui import (
    QPainter,
    QColor,
    QImage,
    QPixmap,
)

ICONS_PATH = str(Path.resolve(Path(os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    "icons"
))))

# This class will store every pixmap for each type of widget
# This permit to reduce memory footprint and time to generate each pixmap
# from each image
#

# Currently not implemented, to evaluate. icon for a checkbox widget:
# 24x24x4 x6 (states) = 14kB (8bpp)
# 24x24x4*4 x6 (states) = 56kB (32bpp)


# !!!! USE QPixmapCache

# class PixmapLib:
#     def __init__(self) -> None:
#         self.pixmaps: dict = {}
#         self.image_filename: dict = {}

#         # pixmaps[object_type][color]


#     def get_pixmap(self, object_type, color: str, state: str) -> QPixmap:
#         pixmap = None
#         try:
#             pixmap = self.pixmaps[object_type][color]
#         except Exception as _:
#             pass
#         if pixmap is None:
#             self._generate_pixmap(image_filename[object_type][state])
#         return QPixmap()


#     def _generate_pixmap(self, filename: str, color: str) -> QPixmap:
#         filepath = os.path.join(ICONS_PATH, filename)
#         if not os.path.exists(filepath):
#             raise ValueError(f"image {filepath} does not exist")
#         qimage: QImage = QImage(filepath)
#         color = QColor(color)

#         painter: QPainter = QPainter()
#         painter.begin(qimage)
#         painter.setRenderHint(QPainter.RenderHint.Antialiasing)
#         painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
#         painter.setBrush(color)
#         painter.setPen(color)
#         painter.drawRect(qimage.rect())
#         painter.end()
#         return QPixmap(qimage)
