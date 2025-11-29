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
    QRect,
)
from PySide6.QtGui import (
    QPolygonF,
    QBrush,
    QColor,
    QMouseEvent,
    QPainter,
    QPaintEvent,
    QPen,
    QFont,
    QFontMetrics,
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
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self.cb_style = theme.checkbox
        self.cb_height = theme.default.height
        self._spacing: int = 8
        self._cached_size: QSize = None

        self.text_rect: QRect = QRect()
        self.box_rect: QRectF = QRectF()
        self.inner_box_rect: QRectF = QRectF()
        self.tick_mark: QPolygonF = None

        # Colors
        self.border = QColor(self.cb_style.border)

        self.pressed = QColor(self.cb_style.pressed)
        self.checked = QColor(self.cb_style.checked)
        self.disabled = QColor(self.cb_style.disabled)

        self.font_enabled = QColor(self.cb_style.font_color)
        self.font_pressed = self.pressed
        self.font_disabled = QColor(self.cb_style.font_color_disabled)

        self.tick_pen = QPen(
            self.checked,
            2,
            Qt.PenStyle.SolidLine,
            Qt.PenCapStyle.RoundCap,
            Qt.PenJoinStyle.RoundJoin
        )

        self.setFont(self.cb_style.font.make_font())
        self.setMinimumSize(self.sizeHint())


    def spacing(self) -> None:
        return self._spacing


    def setSpacing(self, spacing: int) -> None:
        self._spacing = spacing


    def _recalculate_size(self) -> None:
        cb_style = self.cb_style
        self.radius: int = 1
        thickness = 2

        top_margin = (self.cb_height - cb_style.box_size) / 2
        self.box_rect = QRectF(
            thickness - 1,
            top_margin,
            cb_style.box_size,
            cb_style.box_size
        )

        content_width = cb_style.box_size + thickness
        text = self.text()
        self.text_rect = QRect()
        if text:
            text_width = self.fontMetrics().horizontalAdvance(text)
            text_spacing = self._spacing + text_width
            content_width += text_spacing

            if self.layoutDirection() == Qt.LayoutDirection.RightToLeft:
                self.text_rect = QRect(0, 0, text_width, self.cb_height)
                self.box_rect.adjust(text_spacing, 0, text_spacing, 0)
            else:
                self.text_rect = QRect(
                    cb_style.box_size + self._spacing, 0, text_width, self.cb_height
                )

        self.tick_mark = QPolygonF([
            QPointF(self.box_rect.left() + self.box_rect.width() * 0.22, self.box_rect.top() + self.box_rect.height() * 0.52),
            QPointF(self.box_rect.left() + self.box_rect.width() * 0.45, self.box_rect.top() + self.box_rect.height() * 0.75),
            QPointF(self.box_rect.left() + self.box_rect.width() * 0.78, self.box_rect.top() + self.box_rect.height() * 0.28),
        ])

        self._cached_size = QSize(content_width, self.cb_height)


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


    # def mouseMoveEvent(self, event: QMouseEvent):
    #     # Change cursor only if inside the drawn checkbox
    #     if self.hitButton(event.pos()):
    #         self.setCursor(Qt.CursorShape.PointingHandCursor)
    #     else:
    #         self.unsetCursor()
    #     super().mouseMoveEvent(event)


    # def hitButton(self, pos: QPoint) -> bool:
    #     """Only accept clicks inside the visible 16x16 box"""
    #     return self.click_rect.contains(pos)



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

        # Draw box
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
        painter.drawRoundedRect(self.box_rect, self.radius, self.radius)

        # Draw inner rect when pressed
        # painter.setPen(Qt.PenStyle.NoPen)
        # skip_draw = False
        # if enabled:
        #     if checked:
        #         painter.setBrush(QBrush(self.checked))
        #     if pressed:
        #         painter.setBrush(QBrush(self.pressed))
        #     if checked and pressed:
        #         painter.setBrush(QBrush(self.pressed))
        # else:
        #     if checked:
        #         painter.setBrush(QBrush(self.disabled))
        #     else:
        #         skip_draw = True
        # if not skip_draw:
        #     painter.drawRect(self.inner_box_rect)

        # Check mark
        if checked:
            self.tick_pen.setColor(self.checked if enabled else self.disabled)
            painter.setPen(self.tick_pen)
            painter.drawPolyline(self.tick_mark)

        # Draw text
        if self.text():
            alignment = Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft
            if enabled:
                # if pressed:
                #     text_color = self.font_pressed
                # else:
                #     text_color = self.font_enabled
                text_color = self.font_enabled
            else:
                text_color = self.font_disabled
            painter.setPen(text_color)
            painter.drawText(self.text_rect, alignment, self.text())

        painter.end()

