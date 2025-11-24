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

        self.setCursor(Qt.CursorShape.ArrowCursor)

        self._hover: bool = False

        sw_style = theme.switch

        track_width = sw_style.track_width

        self.track_height = sw_style.track_height - 4
        self.track_radius = self.track_height // 2
        self.handle_radius = sw_style.handle_radius
        self.margin = (sw_style.track_height - sw_style.handle_radius) // 2 - 1

        self.setFixedSize(track_width, self.track_height)
        self.handle_position_off = self.margin
        self.handle_position_on = track_width - self.handle_radius - self.margin
        self.handle_position = self.margin

        self.track_rect = QRectF(0, 0, sw_style.track_width, sw_style.track_height)

        # Colors
        self.unchecked_track = QColor(theme.common.bgd)
        self.unchecked_handle = QColor(sw_style.unchecked)

        self.unchecked_hover_handle = QColor(sw_style.hover)

        self.checked_track = QColor(theme.common.bgd)
        self.checked_handle = QColor(sw_style.checked)

        self.disabled_track = QColor(sw_style.disabled)
        self.disabled_handle = QColor(sw_style.handle_disabled)

        # Animation
        curve: QEasingCurve.Type = QEasingCurve.Type.InOutQuad
        self.animation = QPropertyAnimation(self, b"position")
        self.animation.setEasingCurve(curve)
        self.animation.setDuration(200)
        self.stateChanged.connect(self.state_changed_event)


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
                track_brush = self.checked_track
                handle_brush = self.checked_handle
            else:
                track_brush = self.unchecked_track
                handle_brush = (
                    self.unchecked_hover_handle
                    if self._hover
                    else self.unchecked_handle
                )
        else:
            track_brush = self.disabled_track
            handle_brush = self.disabled_handle

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
