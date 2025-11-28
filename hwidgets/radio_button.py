from pprint import pprint
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
    QPointF,
    QRect,
)
from PySide6.QtGui import (
    QBrush,
    QColor,
    QMouseEvent,
    QPainter,
    QPen,
    QPaintEvent,
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
        self.rb_height = theme.default.height
        self._spacing: int = 8
        self._cached_size: QSize = None

        self.text_rect: QRect = QRect()
        self.circle_rect: QRectF = QRectF()
        self.inner_circle_rect: QRectF = QRectF()

        # Colors
        self.border = QColor(self.rb_style.border)

        self.pressed = QColor(self.rb_style.pressed)
        self.checked = QColor(self.rb_style.checked)
        self.disabled = QColor(self.rb_style.disabled)

        self.font_enabled = QColor(self.rb_style.font_color)
        self.font_pressed = self.pressed
        self.font_disabled = QColor(self.rb_style.font_color_disabled)

        self.setMinimumSize(self.sizeHint())


    def spacing(self) -> None:
        return self._spacing


    def setSpacing(self, spacing: int) -> None:
        self._spacing = spacing


    def _recalculate_size(self) -> None:
        rb_style = self.rb_style
        self.thickness = rb_style.circle_thickness

        top_margin = (self.rb_height - rb_style.circle_size) / 2
        self.outer_circle_box = QRectF(
            self.thickness - 1,
            top_margin,
            rb_style.circle_size,
            rb_style.circle_size
        )

        # use thickness to define space between outer circle and inner
        inner_radius = self.thickness / 2 + 1
        center: QPointF = self.outer_circle_box.center()
        self.inner_rect = QRectF(
            center.x() - inner_radius,
            center.y() - inner_radius,
            inner_radius * 2,
            inner_radius * 2
        )

        content_width = rb_style.circle_size + self.thickness
        text = self.text()
        self.text_rect = QRect()
        if text:
            text_width = self.fontMetrics().horizontalAdvance(text)
            text_spacing = self._spacing + text_width
            content_width += text_spacing

            if self.layoutDirection() == Qt.LayoutDirection.RightToLeft:
                self.text_rect = QRect(0, 0, text_width, self.rb_height)
                self.circle_rect.adjust(text_spacing, 0, text_spacing, 0)
            else:
                self.text_rect = QRect(
                    rb_style.circle_size + self._spacing, 0, text_width, self.rb_height
                )

        self._cached_size = QSize(content_width, self.rb_height)


    def sizeHint(self) -> QSize:
        if self._cached_size is None:
            self._recalculate_size()
        return self._cached_size


    def minimumSizeHint(self) -> QSize:
        """Return the same as sizeHint to prevent shrinking below desired size."""
        return self.sizeHint()


    def setText(self, text: str) -> None:
        super().setText(text)
        self._recalculate_size()
        self.setMinimumWidth(self.sizeHint().width())
        self.setFixedHeight(self._cached_size.height())


    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        if DEBUG_GEOMETRY:
            draw_widget_rect(self, painter)

        # Use this only to get current states (hover, pressed, checked)
        option = QStyleOptionButton()
        self.initStyleOption(option)
        pressed = bool(option.state & QStyle.StateFlag.State_Sunken)
        checked = bool(option.state & QStyle.StateFlag.State_On)
        enabled = bool(option.state & QStyle.StateFlag.State_Enabled)

        # Draw outer circle
        pen = QPen()
        pen.setWidth(2)
        if enabled:
            if pressed:
                pen.setColor(self.pressed)
            elif checked:
                pen.setColor(self.border)
            else:
                pen.setColor(self.border)
        else:
            pen.setColor(self.disabled)

        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawEllipse(self.outer_circle_box)

        # Inner circle
        if enabled:
            if pressed:
                pen.setColor(self.pressed)
            elif checked:
                pen.setColor(self.border)
            else:
                pen.setColor(self.border)
        else:
            pen.setColor(self.disabled)

        painter.setPen(pen)
        painter.drawEllipse(self.outer_circle_box)

        # Draw text
        if self.text():
            alignment = Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft
            if enabled:
                if pressed:
                    text_color = self.font_pressed
                else:
                    text_color = self.font_enabled
            else:
                text_color = self.font_disabled
            painter.setPen(text_color)
            painter.drawText(self.text_rect, alignment, self.text())

        painter.end()

