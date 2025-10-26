from .hstyle import (
    HANDLE_RADIUS,
    TRACK_HEIGHT,
    TRACK_MARGIN,
    TRACK_WIDTH,
    HStyle,
)

from PySide6.QtCore import (
    QEasingCurve,
    QPropertyAnimation,
    Qt,
    QPoint,
    QRect,
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
        hstyle: HStyle,
    ) -> None:
        super().__init__(parent)

        self.setCursor(Qt.CursorShape.ArrowCursor)

        self._hovered: bool = False

        track_width = TRACK_WIDTH
        self.track_height = TRACK_HEIGHT - 4
        self.track_radius = self.track_height // 2
        self.handle_radius = HANDLE_RADIUS
        self.margin = TRACK_MARGIN - 1

        self.setFixedSize(track_width, self.track_height)
        self.handle_position_off = self.margin
        self.handle_position_on = TRACK_WIDTH - HANDLE_RADIUS - self.margin
        self.handle_position = self.margin

        self.unchecked_track = QColor(hstyle.widget_bgd)
        self.unchecked_handle = QColor(hstyle.disabled_bgd)

        self.unchecked_hover_handle = QColor(hstyle.hover_bgd)

        self.checked_track = QColor(hstyle.widget_bgd)
        self.checked_handle = QColor(hstyle.checked)

        self.disabled_track = QColor(hstyle.disabled_bgd)
        self.disabled_handle = QColor(hstyle.disabled_text)

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
        self._hovered = True
        self.update()
        super().enterEvent(event)


    def leaveEvent(self, event):
        self._hovered = False
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
                    if self._hovered
                    else self.unchecked_handle
                )
        else:
            track_brush = self.disabled_track
            handle_brush = self.disabled_handle

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(track_brush)
        painter.drawRoundedRect(
            0, 0, self.width(), self.height(),
            self.track_radius, self.track_radius
        )
        painter.setBrush(QColor(handle_brush))
        painter.drawEllipse(
            self.handle_position,
            self.margin,
            self.handle_radius,
            self.handle_radius
        )
        painter.end()
