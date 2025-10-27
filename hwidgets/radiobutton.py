from .logger import hlogger
from .hstyle import (
    COMBOBOX_HEIGHT,
    DEBUG_GEOMETRY,
    RADIO_BORDER_WIDTH,
    RADIO_RADIUS,
    RADIO_SIZE,
    HStyle,
    draw_widget_rect,
)

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
        hstyle: HStyle,
    ) -> None:
        super().__init__(parent)

        self._margin = (COMBOBOX_HEIGHT - RADIO_SIZE) / 2
        self._radius = RADIO_RADIUS
        self.border_width = RADIO_BORDER_WIDTH

        self.hstyle = hstyle


    def sizeHint(self) -> QSize:
        return QSize(COMBOBOX_HEIGHT, COMBOBOX_HEIGHT)


    def mouseMoveEvent(self, event: QMouseEvent):
        if self.hitButton(event.pos()):
            self.setCursor(Qt.CursorShape.PointingHandCursor)
        else:
            self.unsetCursor()
        super().mouseMoveEvent(event)


    def hitButton(self, pos: QPoint) -> bool:
        """Only accept clicks inside the visible 16x16 box"""
        click_rect = QRectF(
            self._margin, self._margin, RADIO_SIZE, RADIO_SIZE,
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

        if not enabled:
            outer_line_color = self.hstyle.disabled_bgd
            brush = self.hstyle.disabled_bgd
        elif checked:
            outer_line_color = self.hstyle.checked
            brush = self.hstyle.checked
        elif pressed:
            outer_line_color = self.hstyle.hover_bgd
            brush = self.hstyle.hover_bgd
        else:
            outer_line_color = self.hstyle.widget_bgd
            brush = self.hstyle.widget_bgd

        # Draw the outer circle
        box = QRectF(self._margin, self._margin, RADIO_SIZE, RADIO_SIZE)

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



