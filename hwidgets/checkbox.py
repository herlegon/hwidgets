from pprint import pprint
from .styles import Theme
from typing import Type
from .hstyle import (
    DEBUG_GEOMETRY,
    draw_widget_rect,
)

from PySide6.QtCore import (
    QRectF,
    QSize,
    Qt,
    QSize,
    QPointF,
    QPoint,
)
from PySide6.QtGui import (
    QPolygonF,
    QBrush,
    QColor,
    QMouseEvent,
    QPainter,
    QPaintEvent,
    QPen,
)
from PySide6.QtWidgets import (
    QWidget,
    QCheckBox,
    QStyleOptionButton,
    QStyle,
)



class HCheckBox(QCheckBox):

    def __init__(
        self,
        /,
        parent: QWidget | None = None,
        *,
        theme: Type[Theme],
        tristate: bool | None = None,
    ) -> None:
        super().__init__(parent)
        self.theme = theme

        cb_style = theme.checkbox

        self._radius: int = 1
        thickness = 2

        self.cb_size = cb_style.size
        margin = (cb_style.size - cb_style.box_size) / 2

        self.box_rect = QRectF(
            margin, margin, cb_style.size - 2 * margin, cb_style.size - 2 * margin
        )

        self.inner_box_rect: QRectF = QRectF(
            margin + thickness - 1,
            margin + thickness - 1,
            cb_style.size - 2 * thickness,
            cb_style.size - 2 * thickness,
        )
        self.click_rect = QRectF(
            margin, margin, cb_style.size, cb_style.size,
        ).adjusted(-thickness, -thickness, thickness, thickness)

        self.tick_mark = QPolygonF([
            QPointF(self.box_rect.left() + self.box_rect.width() * 0.22, self.box_rect.top() + self.box_rect.height() * 0.52),
            QPointF(self.box_rect.left() + self.box_rect.width() * 0.45, self.box_rect.top() + self.box_rect.height() * 0.75),
            QPointF(self.box_rect.left() + self.box_rect.width() * 0.78, self.box_rect.top() + self.box_rect.height() * 0.28),
        ])

        self.setContentsMargins(0, 0, 0, 0)
        self.setMinimumSize(self.sizeHint())

        # Colors
        self.border = QColor(cb_style.border)
        self.border_pressed = QColor(cb_style.border)

        self.tick_color = QColor(theme.window_bgd)
        self.pressed = QColor(cb_style.pressed)
        self.checked = QColor(cb_style.checked)
        self.disabled = QColor(cb_style.disabled)

        self.tick_pen = QPen(
            self.tick_color,
            2,
            Qt.PenStyle.SolidLine,
            Qt.PenCapStyle.RoundCap,
            Qt.PenJoinStyle.RoundJoin
        )


    def sizeHint(self) -> QSize:
        """Return a fixed height, width = checkbox + margins"""
        return QSize(self.cb_size, self.cb_size)


    def mouseMoveEvent(self, event: QMouseEvent):
        # Change cursor only if inside the drawn checkbox
        if self.hitButton(event.pos()):
            self.setCursor(Qt.CursorShape.PointingHandCursor)
        else:
            self.unsetCursor()
        super().mouseMoveEvent(event)


    def hitButton(self, pos: QPoint) -> bool:
        """Only accept clicks inside the visible 16x16 box"""
        return self.click_rect.contains(pos)


    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        if DEBUG_GEOMETRY:
            draw_widget_rect(self, painter)

        # Use this only to get current states (hover, pressed, checked)
        option: QStyleOptionButton = QStyleOptionButton()
        self.initStyleOption(option)
        pressed = bool(option.state & QStyle.StateFlag.State_Sunken)
        checked = bool(option.state & QStyle.StateFlag.State_On)
        enabled = bool(option.state & QStyle.StateFlag.State_Enabled)

        # Checkbox itself

        # Draw box
        pen = QPen()
        pen.setWidth(2)
        if enabled:
            if pressed:
                pen.setColor(self.pressed)
            elif checked:
                pen.setColor(self.checked)
            else:
                pen.setColor(self.border)
        else:
            pen.setColor(self.disabled)

        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRoundedRect(self.box_rect, self._radius, self._radius)

        # Draw inner rect when pressed
        painter.setPen(Qt.PenStyle.NoPen)
        skip_draw = False
        if enabled:
            if checked:
                painter.setBrush(QBrush(self.checked))
            if pressed:
                painter.setBrush(QBrush(self.pressed))
            if checked and pressed:
                painter.setBrush(QBrush(self.pressed))
        else:
            if checked:
                painter.setBrush(QBrush(self.disabled))
            else:
                skip_draw = True
        if not skip_draw:
            painter.drawRect(self.inner_box_rect)

        # Check mark
        if checked:
            painter.setPen(self.tick_pen)
            painter.drawPolyline(self.tick_mark)

        painter.end()

