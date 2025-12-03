from typing import Type
from PySide6.QtGui import (
    QPainter,
    QColor,
    QPen,
)
from PySide6.QtWidgets import (
    QWidget,
)


DEBUG_GEOMETRY: bool = False

def draw_widget_rect(w: Type[QWidget], painter: QPainter, color: str = "#d4d4d4"):
    """Draw around a widget without clipping
    """
    painter.save()
    painter.setRenderHint(QPainter.RenderHint.Antialiasing, on=False)
    pen = QPen()
    pen.setWidth(1)
    pen.setColor(QColor(color))
    painter.setPen(pen)
    # painter.drawRect(w.x(), w.y(), w.width() - 1, w.height() - 1)
    painter.drawRect(0, 0, w.width() - 1, w.height() - 1)
    painter.restore()



