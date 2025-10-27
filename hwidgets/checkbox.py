from hutils import (
    blue, lightcyan, lightgreen, lightgrey, orange, parent_directory, purple, yellow
)
from .hstyle import (
    CHECKBOX_SIZE,
    COMBOBOX_HEIGHT,
    DEBUG_GEOMETRY,
    HStyle,
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
        hstyle: HStyle,
        tristate: bool | None = None,
    ) -> None:
        super().__init__(parent)

        self._margin = (COMBOBOX_HEIGHT - CHECKBOX_SIZE) / 2
        self._radius: int = 1
        self._border_width = 2

        # Colors (QColor objects for speed)
        self.checked = QColor(hstyle.selected)
        self._border = QColor(hstyle.widget_bgd)
        self._disabled = QColor(hstyle.disabled_bgd)
        self._hover = False
        self._pressed = False
        self.hstyle = hstyle
        self._hover_enabled: bool = True

        self.setContentsMargins(0, 0, 0, 0)
        self.setMinimumSize(self.sizeHint())


    def sizeHint(self) -> QSize:
        """Return a fixed height, width = checkbox + margins"""
        return QSize(COMBOBOX_HEIGHT, COMBOBOX_HEIGHT)


    def mouseMoveEvent(self, event):
        # Change cursor only if inside the drawn checkbox
        if self.hitButton(event.pos()):
            self.setCursor(Qt.PointingHandCursor)
        else:
            self.unsetCursor()
        super().mouseMoveEvent(event)


    def hitButton(self, pos: QPoint) -> bool:
        """Only accept clicks inside the visible 16x16 box"""
        click_rect = QRectF(
            self._margin, self._margin, CHECKBOX_SIZE, CHECKBOX_SIZE,
        )
        click_rect = click_rect.adjusted(-2, -2, 2, 2)
        return click_rect.contains(pos)


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
        box = QRectF(self._margin, self._margin, CHECKBOX_SIZE, CHECKBOX_SIZE)

        # Draw box
        pen = QPen()
        pen.setWidth(2)
        box_line_color = (
            self.hstyle.hover_bgd if pressed else self.hstyle.widget_bgd
        )
        pen.setColor(QColor(box_line_color))
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRoundedRect(box, self._radius, self._radius)

        pen = QPen()
        pen.setWidth(2)
        pen.setColor(QColor(box_line_color))
        painter.setPen(pen)
        painter.drawRoundedRect(box, self._radius, self._radius)

        # Draw inner rect when pressed
        if pressed:
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QBrush(QColor(self.hstyle.widget_bgd)))
            painter.drawRoundedRect(
                self._margin + self._border_width - 1,
                self._margin + self._border_width - 1,
                CHECKBOX_SIZE - self._border_width,
                CHECKBOX_SIZE - self._border_width,
                self._radius, self._radius
            )

        # Check mark
        if checked:
            tick_color = self.checked if self.isEnabled() else self.checked.darker(140)

            painter.setPen(QPen(
                tick_color,
                2,
                Qt.PenStyle.SolidLine,
                Qt.PenCapStyle.RoundCap,
                Qt.PenJoinStyle.RoundJoin
            ))
            p1 = QPointF(box.left() + box.width() * 0.22, box.top() + box.height() * 0.52)
            p2 = QPointF(box.left() + box.width() * 0.45, box.top() + box.height() * 0.75)
            p3 = QPointF(box.left() + box.width() * 0.78, box.top() + box.height() * 0.28)
            painter.drawPolyline(QPolygonF([p1, p2, p3]))

        painter.end()

