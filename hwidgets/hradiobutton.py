
from dataclasses import dataclass
import os
from pathlib import Path
from pprint import pprint
import sys
import time
from typing import Any, Literal, Optional, Sequence
from PySide6.QtCore import (
    QCoreApplication,
    QDate,
    QDateTime,
    QLocale,
    QMetaObject,
    QObject,
    QPoint,
    QRect,
    QRectF,
    Signal,
    QSize,
    QTime,
    QUrl,
    QObject,
    Qt,
    QAbstractItemModel,
    QPersistentModelIndex,
    QSize,
    QEvent,
    QTimer,

)
from PySide6.QtGui import (
    QBrush,
    QColor,
    QMouseEvent,
    QPainter,
    QPen,
)
from PySide6.QtWidgets import (
    QWidget,
    QRadioButton,
)
from string import Template

from hutils import blue, lightcyan, lightgreen, lightgrey, orange, parent_directory, purple, yellow
from .logger import hlogger
from .hstyle import RADIO_BORDER_WIDTH, RADIO_RADIUS, HStyle


class HRadioButton(QRadioButton):
    def __init__(
        self,
        text: str,
        /,
        parent: QWidget | None = None,
        *,
        hstyle: HStyle,
    ) -> None:

        super().__init__(parent)
        self.setCursor(Qt.CursorShape.ArrowCursor)
        self._hover = False
        self.setMouseTracking(True)

        # Colors
        self.brush_default: QBrush = QBrush(hstyle.widget_bgd)
        self.border_color = QColor(hstyle.widget_bgd)

        self.brush_hover: QBrush = QBrush(hstyle.hover_bgd)

        self.disabled_color = QColor(hstyle.disabled)
        self.brush_disabled: QBrush = QBrush(hstyle.disabled)

        self.checked_color = QColor(hstyle.selection_bgd)

        # Dimensions
        self.radius = RADIO_RADIUS
        self.border_width = RADIO_BORDER_WIDTH


    def sizeHint(self):
        # Only the circle size matters
        return QSize(
            self.radius*2 + self.border_width*2,
            self.radius*2 + self.border_width*2
        )


    def leaveEvent(self, event: QEvent):
        hlogger.debug(f"{self.__class__}: leave")
        self._hover = False
        self.update()
        super().leaveEvent(event)


    def enterEvent(self, event: QEvent):
        hlogger.debug(f"{self.__class__}: over")
        self._hover = True
        self.update()
        super().enterEvent(event)


    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        hlogger.debug(f"{self.__class__}: clicked")
        if self._hover:
            self.click()
        return super().mouseReleaseEvent(event)


    # To use if we want to detect mouse inside the circle and not the outer rect
    #  might have a speed impact and "frustrating" with small radio buttons
    #
    # def hitButton(self, pos):
    #     """Only toggle if click is inside the circle.
    #     The probleme is that the hover is done when in the rectangle. If hovered,
    #     with this method, the mouse click button doesn't work
    #     """
    #     center = self.rect().center()
    #     radius = self.radio_radius + self.border_width / 2
    #     dx = pos.x() - center.x()
    #     dy = pos.y() - center.y()
    #     return dx*dx + dy*dy <= radius*radius
    #
    #
    # def _is_inside_circle(self, x, y):
    #     """Check if point (x, y) is inside the circular area of the button."""
    #     radius = min(self.width(), self.height()) / 2
    #     dx = x - self.width() / 2
    #     dy = y - self.height() / 2
    #     return dx*dx + dy*dy <= radius*radius
    #
    #
    # def leaveEvent(self, event: QEvent):
    #     hlogger.debug(f"{self.__class__}: leave")
    #     pos = self.mapFromGlobal(self.cursor().pos())
    #     if not self._is_inside_circle(pos.x(), pos.y()):
    #         self._hover = True
    #         self.update()
    #     super().leaveEvent(event)
    #
    #
    # def enterEvent(self, event: QEnterEvent):
    #     pos = self.mapFromGlobal(self.cursor().pos())
    #     if self._is_inside_circle(pos.x(), pos.y()):
    #         self._hover = True
    #         self.update()
    #     super().enterEvent(event)
    #
    #
    # def mouseMoveEvent(self, event: QMouseEvent):
    #     inside = self._is_inside_circle(event.position().x(), event.position().y())
    #     if inside != self._hover:
    #         self._hover = inside
    #         self.update()
    #     super().mouseMoveEvent(event)


    def paintEvent(self, event: QEvent):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Determine border color
        if not self.isEnabled():
            border_color = self.disabled_color
        else:
            border_color = self.border_color

        # Draw the outer circle
        outer_rect = QRectF(
            1,
            (self.height() - self.radius*2)/2,
            self.radius*2,
            self.radius*2
        )
        pen = QPen(border_color, self.border_width)
        painter.setPen(pen)
        brush = self.brush_default
        if self.isEnabled() and not self.isChecked() and self._hover:
            brush = self.brush_hover
        else:
            brush = self.brush_disabled
        painter.setBrush(brush)
        painter.drawEllipse(outer_rect)

        # Inner circle
        if self.isChecked():
            inner_radius = self.radius / 2 + 1
            inner_rect = QRectF(
                outer_rect.center().x() - inner_radius,
                outer_rect.center().y() - inner_radius,
                inner_radius*2,
                inner_radius*2
            )
            painter.setBrush(QBrush(self.checked_color if self.isEnabled() else self.disabled_color))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(inner_rect)

        painter.end()



