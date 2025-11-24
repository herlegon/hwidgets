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

        self._radius: int = 1
        margin = (theme.checkbox.size - theme.checkbox.box_thickness) / 2
        self.box_rect = QRectF(
            margin, margin, theme.checkbox.size, theme.checkbox.size
        )
        self.inner_box_rect: QRectF = QRectF(
            margin + theme.checkbox.box_thickness - 1,
            margin + theme.checkbox.box_thickness - 1,
            theme.checkbox.size - theme.checkbox.box_thickness,
            theme.checkbox.size - theme.checkbox.box_thickness,
        )
        self.click_rect = QRectF(
            margin, margin, theme.checkbox.size, theme.checkbox.size,
        ).adjusted(-2, -2, 2, 2)

        self.tick_mark = QPolygonF([
            QPointF(self.box_rect.left() + self.box_rect.width() * 0.22, self.box_rect.top() + self.box_rect.height() * 0.52),
            QPointF(self.box_rect.left() + self.box_rect.width() * 0.45, self.box_rect.top() + self.box_rect.height() * 0.75),
            QPointF(self.box_rect.left() + self.box_rect.width() * 0.78, self.box_rect.top() + self.box_rect.height() * 0.28),
        ])
        self.tick_pen = QPen(
            theme.checkbox.normal,
            2,
            Qt.PenStyle.SolidLine,
            Qt.PenCapStyle.RoundCap,
            Qt.PenJoinStyle.RoundJoin
        )

        # Colors (QColor objects for speed)
        self.checked = QColor(theme.checkbox.checked)
        self._disabled = QColor(theme.checkbox.disabled)
        self._hover = False
        self._pressed = False
        self._hover_enabled: bool = True

        self.setContentsMargins(0, 0, 0, 0)
        self.setMinimumSize(self.sizeHint())


    def sizeHint(self) -> QSize:
        """Return a fixed height, width = checkbox + margins"""
        return QSize(self.theme.size, self.theme.size)


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

        # Checkbox itself

        # Draw box
        pen = QPen()
        pen.setWidth(2)
        box_line_color = (
            self.theme.checkbox.hover if pressed else self.theme.checkbox.normal
        )
        pen.setColor(QColor(box_line_color))
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRoundedRect(self.box_rect, self._radius, self._radius)

        # Draw inner rect when pressed
        if pressed:
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QBrush(QColor(self.theme.common.bgd)))
            painter.drawRoundedRect(self.inner_box_rect, self._radius, self._radius)

        # Check mark
        if checked:
            tick_color = self.checked if self.isEnabled() else self.checked.darker(140)
            self.tick_pen.setColor(tick_color)
            painter.setPen(self.tick_pen)
            painter.drawPolyline(self.tick_mark)

        painter.end()

