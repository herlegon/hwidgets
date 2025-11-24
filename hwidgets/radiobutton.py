from typing import Type
from .logger import hlogger
from .hstyle import (
    DEBUG_GEOMETRY,
    draw_widget_rect,
)
from .style_manager import Theme

from PySide6.QtCore import (
    QRectF,
    QSize,
    Qt,
    QSize,
    QEvent,
    QPoint,
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
    QStyleOptionButton,
    QStyle,
)



class HRadioButton(QRadioButton):
    def __init__(
        self,
        text: str,
        /,
        parent: QWidget | None = None,
        *,
        theme: Type[Theme],
    ) -> None:
        super().__init__(parent)

        self._margin = (theme.common.radius - theme.radio_button.size) / 2
        self._radius = theme.radio_button.radius
        self.border_width = theme.radio_button.border_thickness

        self.theme = theme


    def sizeHint(self) -> QSize:
        return QSize(self.theme.common.height, self.theme.common.height)


    def mouseMoveEvent(self, event: QMouseEvent):
        if self.hitButton(event.pos()):
            self.setCursor(Qt.CursorShape.PointingHandCursor)
        else:
            self.unsetCursor()
        super().mouseMoveEvent(event)


    def hitButton(self, pos: QPoint) -> bool:
        """Only accept clicks inside the visible 16x16 box"""
        click_rect = QRectF(
            self._margin,
            self._margin,
            self.theme.radio_button.size,
            self.theme.radio_button.size,
        )
        return click_rect.contains(pos)


    def paintEvent(self, event: QEvent):
        painter = QPainter(self)
        if DEBUG_GEOMETRY:
            draw_widget_rect(self, painter)

        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        option: QStyleOptionButton = QStyleOptionButton()
        self.initStyleOption(option)
        enabled = bool(option.state & QStyle.StateFlag.State_Enabled)
        pressed = bool(option.state & QStyle.StateFlag.State_Sunken)
        checked = bool(option.state & QStyle.StateFlag.State_On)

        radio_theme = self.theme.radio_button
        if not enabled:
            outer_line_color = radio_theme.disabled
            brush = radio_theme.disabled
        elif checked:
            outer_line_color = radio_theme.checked
            brush = radio_theme.checked
        elif pressed:
            outer_line_color = radio_theme.hover
            brush = radio_theme.hover
        else:
            outer_line_color = self.theme.common.bgd
            brush = self.theme.common.bgd

        # Draw the outer circle
        box = QRectF(self._margin, self._margin, radio_theme.size, radio_theme.size)

        pen = QPen()
        pen.setWidth(self.border_width)
        pen.setColor(QColor(outer_line_color))
        painter.setPen(pen)
        painter.drawEllipse(box)

        # Draw inner cercle when pressed, checked
        draw_inner: bool = enabled or (not enabled and checked)
        if draw_inner:
            inner_radius = self._radius / 2 + 1
            inner_rect = QRectF(
                box.center().x() - inner_radius,
                box.center().y() - inner_radius,
                inner_radius * 2,
                inner_radius * 2
            )

            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QBrush(QColor(brush)))
            painter.drawEllipse(inner_rect)

        painter.end()



