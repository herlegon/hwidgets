from typing import Type
from PySide6.QtGui import (
    QPainter,
    QColor,
    QPen,
)
from PySide6.QtWidgets import (
    QWidget,
)


DEBUG_GEOMETRY: bool = True

def draw_widget_rect(w: Type[QWidget], painter: QPainter):
    """Draw around a widget without clipping
    """
    painter.save()
    painter.setRenderHint(QPainter.RenderHint.Antialiasing, on=False)
    pen = QPen()
    pen.setWidth(1)
    pen.setColor(QColor("#d4d4d4"))
    painter.setPen(pen)
    # painter.drawRect(w.x(), w.y(), w.width() - 1, w.height() - 1)
    painter.drawRect(0, 0, w.width() - 1, w.height() - 1)
    painter.restore()



