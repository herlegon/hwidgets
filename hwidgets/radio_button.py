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
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self.rb_style = theme.radio_button
        self.size_hint = QSize(theme.common.height, theme.common.height)

        self.margin = (theme.common.height - self.rb_style.size) / 2
        self.radius = self.rb_style.radius
        self.border_width = self.rb_style.border_thickness

        self.outer_circle_box = QRectF(
            self.margin, self.margin, self.rb_style.size, self.rb_style.size
        )
        self.inner_radius = self.radius / 2 + 1
        self.inner_rect = QRectF(
            self.outer_circle_box.center().x() - self.inner_radius,
            self.outer_circle_box.center().y() - self.inner_radius,
            self.inner_radius * 2,
            self.inner_radius * 2
        )


    def sizeHint(self) -> QSize:
        return self.size_hint


    def mouseMoveEvent(self, event: QMouseEvent):
        if self.hitButton(event.pos()):
            self.setCursor(Qt.CursorShape.PointingHandCursor)
        else:
            self.unsetCursor()
        super().mouseMoveEvent(event)


    def hitButton(self, pos: QPoint) -> bool:
        """Only accept clicks inside the visible 16x16 box"""
        click_rect = QRectF(
            self.margin,
            self.margin,
            self.rb_style.size,
            self.rb_style.size,
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

        rb_style = self.rb_style
        if not enabled:
            outer_line_color = rb_style.disabled
            brush = rb_style.disabled

        elif checked:
            outer_line_color = rb_style.checked
            brush = rb_style.checked

        elif pressed:
            outer_line_color = rb_style.pressed
            brush = rb_style.pressed

        else:
            outer_line_color = rb_style.unchecked
            brush = rb_style.unchecked

        # Draw the outer circle
        pen = QPen()
        pen.setWidth(self.border_width)
        pen.setColor(QColor(outer_line_color))
        painter.setPen(pen)
        painter.drawEllipse(self.outer_circle_box)

        # Draw inner cercle when pressed, checked
        draw_inner: bool = enabled or (not enabled and checked)
        if draw_inner:
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QBrush(QColor(brush)))
            painter.drawEllipse(self.inner_rect)

        painter.end()



