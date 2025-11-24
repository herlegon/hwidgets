from typing import Type
from .hstyle import (
    DEBUG_GEOMETRY,
    draw_widget_rect,
)
from .style_manager import Theme

from PySide6.QtCore import (
    QEasingCurve,
    QPropertyAnimation,
    Qt,
    QPoint,
    QRect,
    QRectF,
    QSize,
    Property
)
from PySide6.QtGui import (
    QPaintEvent,
    QPainter,
    QColor,
)
from PySide6.QtWidgets import (
    QCheckBox,
    QWidget,
)


class HSwitch(QCheckBox):
    def __init__(
        self,
        /,
        parent: QWidget | None = None,
        *,
        theme: Type[Theme],
    ) -> None:
        super().__init__(parent)
        self._hover: bool = False

        sw_style = theme.switch
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self.setFixedSize(sw_style.track_width, sw_style.track_height)
        track_height = sw_style.track_height - 4

        # handle radius
        self.handle_radius = sw_style.handle_radius

        # margin is the space between the border and the handle.
        self.margin = (sw_style.track_height - sw_style.handle_radius) // 2

        # handle coordinates
        self.handle_position_off = self.margin
        self.handle_position_on = (
            sw_style.track_width - self.handle_radius - self.margin
        )
        self.handle_position = self.margin

        # Track rounded rect
        self.track_rect = (
            QRectF(0, 0, sw_style.track_width, sw_style.track_height)
            .adjusted(1,1,-1,-1)
        )
        self.track_radius = track_height // 2

        # Colors
        self.track_on = QColor(sw_style.track_on)
        self.track_off = QColor(sw_style.track_off)

        self.handle_on = QColor(sw_style.handle_on)
        self.handle_off = QColor(sw_style.handle_off)

        self.track_disabled = QColor(sw_style.track_disabled)
        self.handle_disabled = QColor(sw_style.handle_disabled)

        # Animation
        curve: QEasingCurve.Type = QEasingCurve.Type.InOutQuad
        self.animation = QPropertyAnimation(self, b"position")
        self.animation.setEasingCurve(curve)
        self.animation.setDuration(200)
        self.stateChanged.connect(self.state_changed_event)


    def sizeHint(self):
        return self.size()


    @Property(float)
    def position(self) -> int:
        return self.handle_position


    @position.setter
    def position(self, pos: int) -> None:
        self.handle_position = pos
        self.update()


    def setChecked(self, checked: bool) -> None:
        self.blockSignals(True)
        super().setChecked(checked)
        self.handle_position = (
            self.handle_position_on if checked else self.handle_position_off
        )
        self.blockSignals(False)


    def state_changed_event(self, checked: bool) -> None:
        self.animation.stop()
        self.animation.setEndValue(
            self.handle_position_on if checked else self.handle_position_off)
        self.animation.start()


    def hitButton(self, pos: QPoint):
        return self.contentsRect().contains(pos)


    def enterEvent(self, event):
        self._hover = True
        self.update()
        super().enterEvent(event)


    def leaveEvent(self, event):
        self._hover = False
        self.update()
        super().leaveEvent(event)


    def paintEvent(self, event: QPaintEvent) -> None:
        if self.isEnabled():
            if self.isChecked():
                track_brush = self.track_on
                handle_brush = self.handle_on
            else:
                track_brush = self.track_off
                handle_brush = self.handle_off
        else:
            track_brush = self.track_disabled
            handle_brush = self.handle_disabled

        painter = QPainter(self)
        if DEBUG_GEOMETRY:
            draw_widget_rect(self, painter)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(track_brush)
        painter.drawRoundedRect(self.track_rect, self.track_radius, self.track_radius)
        painter.setBrush(QColor(handle_brush))
        painter.drawEllipse(
            self.handle_position,
            self.margin,
            self.handle_radius,
            self.handle_radius
        )
        painter.end()

